from flask import Flask, render_template, request, send_from_directory
import yt_dlp
import os

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    error_message = None
    video_title = None
    filename = None

    if request.method == "POST":
        url = request.form.get("url")
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
                    "preferredquality": "192",
                }
            ],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_title = info.get("title", "Tundmatu pealkiri")
                original_filename = ydl.prepare_filename(info)

            filename = os.path.basename(
                original_filename.rsplit(".", 1)[0] + ".mp3"
)
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
    video_title=video_title
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