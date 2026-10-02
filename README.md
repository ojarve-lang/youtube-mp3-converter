# 🎵 YouTube → MP3 Converter

Lihtne Flaskil põhinev veebirakendus, millega saab teisendada ühe video heliriba MP3-failiks.

Projekt on loodud Pythoniga ning kasutab video töötlemiseks `yt-dlp` ja `FFmpeg` tööriistu.

## ✨ Funktsioonid

- 🎧 Video heliriba teisendamine MP3-failiks
- 🎵 MP3 kvaliteet 192 kbps
- ⬇️ Valmis MP3-faili allalaadimine
- 🚫 Playlistide automaatse allalaadimise vältimine
- ⏳ Konverteerimise ajal laadimisanimatsioon
- 🏷️ Video pealkirja kuvamine
- ❌ Vigase või mittetöötava lingi korral veateade
- 🎨 Bootstrap 5 ja kohandatud CSS-kujundus
- 📱 Kohanduv veebivaade

> **Märkus:** rakendus on mõeldud enda või muu sellise sisu töötlemiseks, mille allalaadimiseks on kasutajal õigus või luba.

## 🛠️ Kasutatud tehnoloogiad

- **Python** – rakenduse põhiloogika
- **Flask** – veebirakenduse raamistik
- **yt-dlp** – video helivoo allalaadimine
- **FFmpeg** – heli teisendamine MP3-vormingusse
- **HTML5** – veebilehe struktuur
- **CSS3** – kohandatud kujundus
- **Bootstrap 5** – kasutajaliidese komponendid ja paigutus
- **JavaScript** – laadimisanimatsiooni ja nupu oleku juhtimine
- **Jinja2** – Pythoni andmete kuvamine HTML-mallis

## 🚀 Paigaldamine ja käivitamine

### 1. Laadi projekt alla

Klooni projekt GitHubist või laadi see ZIP-failina alla.

```bash
git clone https://github.com/ojarve-lang/youtube-mp3-converter.git
cd youtube-mp3-converter
```

### 2. Loo virtuaalkeskkond

Windows PowerShellis:

```powershell
python -m venv venv
```

Aktiveeri virtuaalkeskkond:

```powershell
.\venv\Scripts\Activate.ps1
```

Kui PowerShell ei luba skripti käivitada, võib aktiivse terminaliseansi jaoks kasutada:

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

Seejärel aktiveeri virtuaalkeskkond uuesti.

### 3. Paigalda Pythoni paketid

```powershell
pip install -r requirements.txt
```

### 4. Paigalda FFmpeg

Rakendus vajab MP3-failide loomiseks FFmpeg-i.

Windowsis saab selle paigaldada näiteks käsuga:

```powershell
winget install --id Gyan.FFmpeg -e
```

Pärast paigaldamist võib olla vajalik terminal või VS Code uuesti käivitada.

Kontrollimiseks:

```powershell
ffmpeg -version
```

### 5. Käivita rakendus

```powershell
python app.py
```

Seejärel ava veebibrauseris:

```text
http://127.0.0.1:5000
```
