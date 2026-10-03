from flask import Flask, render_template, request, send_from_directory
import yt_dlp
import os

app = Flask(__name__)


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
        url = request.form.get("url")
        audio_quality = request.form.get("quality", "192")
          # Get selected audio quality
        print("Sisestatud URL:", url)

        ydl_opts = {
            "format": "bestaudio/best",
            "noplaylist": True,
            "playlist_items": "1",
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


@app.route("/download/<path:filename>")
def download_file(filename):
    return send_from_directory(
        "downloads",
        filename,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)