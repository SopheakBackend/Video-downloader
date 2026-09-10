import os
import traceback
import threading
from django.shortcuts import render, redirect
import yt_dlp
from django.http import FileResponse, Http404
from django.contrib import messages

def downloader_home(request):
    if request.method == "POST":
        video_url = request.POST.get('video_url')
        if not video_url:
            messages.error(request, 'Please enter a valid link address')
            return render(request, 'downloader_home.html')

        ydl_opts = {
            'skip_download': True,
            'noplaylist': True,
            'extractor_re_compile': False,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)

                if not info:
                    raise Exception("YouTube client payload returned empty data.")

                formats = info.get('formats', [])
                unique_heights = set()
                resolutions = []

                for f in formats:
                    height = f.get('height')
                    vcodec = f.get('vcodec')
                    if height and vcodec and vcodec != 'none' and height not in unique_heights:
                        unique_heights.add(height)
                        resolutions.append({'height': height, 'ext': 'mp4'})

                if not resolutions:
                    raise Exception("No valid video resolution profiles found for this URL.")

                resolutions.sort(key=lambda x: x['height'], reverse=True)

                templateContext = {
                    'title': info.get('title'),
                    'thumbnail': info.get('thumbnail'),
                    'video_url': video_url,
                    'resolutions': resolutions,
                }
                return render(request, 'download.html', templateContext)

        except Exception as e:
            print("Extraction Error Details:")
            traceback.print_exc()
            messages.error(request, 'Could not read the video metadata. Please try again or use a different URL.')

    return render(request, 'downloader_home.html')


def processing_download(request):
    video_url = request.GET.get('url')
    height = request.GET.get('height')

    if not video_url or not height:
        messages.error(request, 'Failed to download: invalid link')
        return redirect('downloader_home')

    media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'download_cache')
    os.makedirs(media_dir, exist_ok=True)

    ydl_opts = {
        'format': f'bestvideo[height={height}][ext=mp4]+bestaudio[ext=m4a]/best[height={height}][ext=mp4]/best[height={height}]/best',
        'outtmpl': os.path.join(media_dir, '%(title)s_%(height)sp.%(ext)s'),
        'merge_output_format': 'mp4',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            target_file = ydl.prepare_filename(info)

            if not os.path.exists(target_file):
                base, _ = os.path.splitext(target_file)
                target_file = base + '.mp4'

        if not os.path.exists(target_file):
            raise FileNotFoundError(f"Target download asset vanished from file path map: {target_file}")

        file_to_stream = open(target_file, 'rb')
        response = FileResponse(file_to_stream, as_attachment=True, filename=os.path.basename(target_file))

        def clean_file():
            try:
                file_to_stream.close()
            except Exception:
                pass
            if os.path.exists(target_file):
                try:
                    os.remove(target_file)
                    print('Successfully removed user downloaded file.')
                except PermissionError:
                    pass  
                except Exception as cleanup_err:
                    print(f'Cleanup failed: {cleanup_err}')

        response.close = clean_file

        # FALLBACK: the dev server (wsgiref, threaded) can sometimes fail to invoke
        # response.close() after streaming a large file, leaving the file undeleted.
        # Large files can still be mid-transfer to the browser well past a fixed
        # delay, so instead of one deadline, retry periodically until the OS lock
        # clears (or we give up after a generous window).
        def delayed_cleanup():
            max_attempts = 20      # ~20 * 30s = 10 minutes total
            wait_seconds = 30
            for attempt in range(max_attempts):
                if not os.path.exists(target_file):
                    return  # already cleaned up (response.close() succeeded)
                # Force-close the handle ourselves: response.close() may never
                # fire on the dev server, in which case file_to_stream stays
                # open forever and no amount of retrying os.remove() will help.
                try:
                    if not file_to_stream.closed:
                        file_to_stream.close()
                except Exception:
                    pass
                try:
                    os.remove(target_file)
                    print('Fallback cleanup removed leftover file:', target_file)
                    return
                except PermissionError:
                    # Still locked (client still downloading, or ffmpeg still
                    # holding a handle) - wait and retry rather than erroring out.
                    threading.Event().wait(wait_seconds)
                except Exception as cleanup_err:
                    print(f'Fallback cleanup failed: {cleanup_err}')
                    return
            print('Fallback cleanup gave up after repeated lock conflicts:', target_file)

        threading.Timer(90.0, delayed_cleanup).start()

        return response

    except Exception as e:
        print("Download Error Details:")
        traceback.print_exc()
        messages.error(request, 'Video download failed, please use a valid link.')
        return redirect('downloader_home')
