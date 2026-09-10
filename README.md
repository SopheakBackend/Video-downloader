# Video Downloader

A simple Django app for downloading YouTube and X/Twitter videos at a chosen resolution, powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp) and `ffmpeg`.

## Requirements

- Python 3.10+
- [ffmpeg](https://ffmpeg.org/download.html) (required for merging separate video/audio streams into a single MP4, needed for anything above the lowest resolution)
- Git

## 1. Clone the repository

```bash
git clone https://github.com/SopheakBackend/Video-downloader.git
cd Video-downloader
```

## 2. Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

This installs Django, `yt-dlp`, `python-decouple`, and everything else the project needs.

## 4. Install ffmpeg

`yt-dlp` needs `ffmpeg` on your system PATH to merge video and audio streams for any resolution above the lowest available option.

- **Windows:** Download a build from [ffmpeg.org](https://ffmpeg.org/download.html) (or `choco install ffmpeg` if you use Chocolatey), then add the `bin` folder to your PATH.
- **macOS:** `brew install ffmpeg`
- **Linux:** `sudo apt install ffmpeg` (Debian/Ubuntu) or your distro's equivalent.

Verify it's installed correctly:
```bash
ffmpeg -version
```

## 5. Set up environment variables

This project uses [`python-decouple`](https://github.com/HBNetwork/python-decouple) to keep the Django secret key (and any other sensitive settings) out of source control.

Create a `.env` file in the project root (same folder as `manage.py`):

```env
SECRET_KEY=your-generated-secret-key-here
DEBUG=True
```

**Generate a secret key:**

Run this once to generate a fresh key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output into `SECRET_KEY` in your `.env` file. Never commit `.env` to version control — make sure it's listed in `.gitignore`.

## 6. Run migrations

```bash
python manage.py migrate
```

## 7. Start the development server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser, paste a YouTube or X/Twitter video URL, and choose a resolution to download.


