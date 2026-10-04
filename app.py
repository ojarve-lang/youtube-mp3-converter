from flask import Flask, render_template, request, send_from_directory, jsonify
import yt_dlp
import os
import re


class file_name:
    def __init__(self, raw_name):
        self.raw_name = raw_name or "download.mp3"

    def sanitize(self):
        safe_name = os.path.basename(self.raw_name).replace("\\", "/")
        safe_name = safe_name.split("/")[-1]
        safe_name = re.sub(r"[^A-Za-z0-9_. -]", "_", safe_name)
        safe_name = safe_name.strip()
        return safe_name if safe_name else "download.mp3"

    def full_path(self):
        return os.path.join("downloads", self.sanitize())

    def __str__(self):
        return self.sanitize()


app = Flask(__name__)


progress_data = {
    "percent": 0,
    "status": "Ootan..."
}  
def progress_hook(data):
    if data["status"] == "downloading":
        downloaded = data.get("downloaded_bytes", 0)
        total = data.get("total_bytes") or data.get("total_bytes_estimate")

        if total:
            percent = int(downloaded / total * 100)

            progress_data["percent"] = percent
            progress_data["status"] = "Laadin heli alla..."

    elif data["status"] == "finished":
        progress_data["percent"] = 100
        progress_data["status"] = "Allalaadimine valmis, teisendan MP3-ks..."


@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    error_message = None
    video_title = None
    video_thumbnail = None
    video_duration = None
    file_size = None
    filename = None
    audio_quality = "192"  # Default audio quality

    if request.method == "POST":
        progress_data["percent"] = 0
        progress_data["status"] = "Valmistun..."


        url = request.form.get("url")
        audio_quality = request.form.get("quality", "192")
          # Get selected audio quality
        print("Sisestatud URL:", url)

        ydl_opts = {
            "format": "bestaudio/best",
            "noplaylist": True,
            "playlist_items": "1",
            "progress_hooks": [progress_hook],
            "outtmpl": "downloads/%(title)s.%(ext)s",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality":audio_quality
                }
            ],
        }

        try:

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_title = info.get("title", "Tundmatu pealkiri")
                video_thumbnail = info.get("thumbnail", None)
                duration_seconds = info.get("duration")
                if duration_seconds is not None:
                    minutes = duration_seconds // 60
                    seconds = duration_seconds % 60
                    video_duration = f"{minutes}:{seconds:02d}"

                original_filename = ydl.prepare_filename(info)

            filename = os.path.basename(
                original_filename.rsplit(".", 1)[0] + ".mp3"
            )
            file_path = os.path.join("downloads", filename)
            file_size = os.path.getsize(file_path) / (1024 * 1024)
            file_size = f"{file_size:.1f} MB"
            print("Konverteerimine õnnestus!")
            message = "MP3 on edukalt valmis! 🎵"
        except Exception as error:
            print("Tekkis viga:", error)

            error_message = "Tekkis viga konverteerimisel. Palun proovi uuesti."

    return render_template(
        "index.html",
        message=message,
        error_message=error_message,
        filename=filename,
        video_title=video_title,
        video_thumbnail=video_thumbnail,
        video_duration=video_duration,
        file_size=file_size,
        audio_quality=audio_quality
    )


@app.route("/download/<path:download_name>")
def download_file(download_name):
    safe_file = file_name(download_name)

    return send_from_directory(
        "downloads",
        filename=safe_file.sanitize(),
        as_attachment=True
    )


@app.route("/progress")
def progress():
    return jsonify(progress_data)

if __name__ == "__main__":
    app.run(debug=True)