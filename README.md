# Video Downloader 🚀

A simple Django app for downloading YouTube and X/Twitter videos powered by `yt-dlp` and `ffmpeg`.

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd Video-downloader
   ```

2. **Create and activate a virtual environment:**
   - **Windows:** `python -m venv venv` then `.\venv\Scripts\Activate.ps1`
   - **macOS/Linux:** `python3 -m venv venv` then `source venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install `ffmpeg` and `deno`:**
   - **Windows:** `winget install Gyan.FFmpeg` and `winget install DenoLand.Deno`
   - **macOS:** `brew install ffmpeg deno`
   - **Linux:** `sudo apt install ffmpeg` and install Deno via their official script.

5. **Generate a `SECRET_KEY` and configure `.env`:**
   Generate a key using Python:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   Add the generated key and `DEBUG=True` into a new `.env` file.

6. **Run migrations and start the server:**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```
