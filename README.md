# 🐍 Small Python Projects

A collection of small, practical Python projects built to learn Python programming, automation, file processing, multimedia handling, system utilities, and more.

This repository contains **18 standalone Python projects**, ranging from simple utilities and generators to audio/video processing tools.

> 🚀 Built as a personal Python learning and experimentation repository.

---

## 📚 Projects

| #  | Project                    | Category         | Description                                               |
| -- | -------------------------- | ---------------- | --------------------------------------------------------- |
| 01 | 🎵 Audio Cutter            | Audio            | Cut a selected portion from an audio file                 |
| 02 | 🎚️ Audio Mixer            | Audio            | Combine multiple audio files with transitions and effects |
| 03 | 🏷️ Barcode Generator      | Utility          | Generate barcodes from text or numbers                    |
| 04 | 🖼️ Image Compressor       | Image            | Reduce image file size                                    |
| 05 | 📄 Image → PDF             | Converter        | Convert images into PDF documents                         |
| 06 | 🧾 Invoice Generator       | Utility          | Generate professional invoices in PDF format              |
| 07 | 🔐 PDF Locker              | PDF              | Protect PDF files with a password                         |
| 08 | 🔑 Password Generator      | Security Utility | Generate random passwords                                 |
| 09 | 📱 QR Generator            | Utility          | Generate QR codes                                         |
| 10 | 💻 System Information      | System Utility   | Display information about the computer                    |
| 11 | 🧹 Temporary Files Cleaner | System Utility   | Clean temporary files                                     |
| 12 | 🔊 Text → Speech           | Audio / TTS      | Convert text into spoken audio                            |
| 13 | 🐢 Turtle Graphics         | Graphics         | Create graphics and animations using Turtle               |
| 14 | ⌨️ Typing Speed Test       | Game / Utility   | Test typing speed and accuracy                            |
| 15 | 🎬 Video → Audio           | Converter        | Extract audio from video files                            |
| 16 | 🎞️ Video → GIF            | Converter        | Convert video clips into GIFs                             |
| 17 | 🎤 Vocal Extractor         | Audio / AI       | Separate vocals and instrumental audio                    |
| 18 | ▶️ YouTube Downloader      | Downloader       | Download YouTube media from the terminal                  |

---

# 🚀 Getting Started

## Prerequisites

Before running the projects, make sure you have:

* **Python 3.10+**
* **pip**
* **FFmpeg** — required by several multimedia projects
* A terminal such as PowerShell, Command Prompt, or Windows Terminal

Check Python:

```bash
python --version
```

Check pip:

```bash
pip --version
```

Check FFmpeg:

```bash
ffmpeg -version
```

---

# 📥 Installation

Clone the repository:

```bash
git clone https://github.com/Prashamjn/Small-Python-Projects.git
```

Enter the repository:

```bash
cd Small-Python-Projects
```

Each project is independent, so you only need to install the dependencies required by the project you want to use.

---

# 📂 Project Details

## 01. 🎵 Audio Cutter

### Description

A terminal-based audio cutting utility that allows you to select a start and end time and create a new audio clip.

### Features

* Enter an audio file path
* Specify start time
* Specify end time
* Automatically creates an output folder
* Preserves the original audio format
* Uses FFmpeg for processing

### Requirements

* Python
* FFmpeg

### Run

```bash
cd AudioCutter
python AudioCutter.py
```

### Example

```text
Enter audio path: song.mp3
Start time (HH:MM:SS): 00:01:00
End time (HH:MM:SS): 00:02:30
```

The processed audio is saved in:

```text
AudioCutter/cut_audio/
```

---

## 02. 🎚️ Audio Mixer

### Description

A more advanced terminal-based audio mixer for combining multiple songs and applying transitions.

### Features

* Mix multiple songs
* Select individual clips
* Volume control
* Fade-in
* Fade-out
* Fade transitions
* Crossfade transitions
* MP3 output
* 320 kbps output
* Automatic duration detection

### Requirements

* Python
* FFmpeg
* FFprobe

### Run

```bash
cd AudioMixer
python AudioMixer.py
```

The final mix is saved in:

```text
AudioMixer/mixed_audio/
```

---

## 03. 🏷️ Barcode Generator

### Description

Generate barcodes directly from Python.

### Run

```bash
cd Barcode
python barcodeGenerator.py
```

### Dependency

Install the barcode package if required:

```bash
pip install python-barcode
```

---

## 04. 🖼️ Image Compressor

### Description

A simple image compression utility designed to reduce image file size while maintaining reasonable quality.

### Run

```bash
cd ImageCompressor
python ImageCompressor.py
```

### Typical dependency

```bash
pip install Pillow
```

---

## 05. 📄 Image → PDF

### Description

Convert image files into PDF documents.

### Run

```bash
cd ImgToPDF
python ImgToPDF.py
```

### Typical dependency

```bash
pip install Pillow
```

---

## 06. 🧾 Invoice Generator

### Description

Generate professional PDF invoices using Python.

### Features

* Customer information
* Product/service details
* Quantity
* Pricing
* Tax/total calculations
* PDF output

### Run

```bash
cd InvoiceGenerator
python InvoiceGenerator.py
```

### Typical dependency

```bash
pip install reportlab
```

---

## 07. 🔐 PDF Locker

### Description

A utility for protecting PDF documents with password-based security.

### Run

```bash
cd "PDF Locker"
python PDFLocker.py
```

> Check the project's source/imports if additional PDF libraries are required.

---

## 08. 🔑 Password Generator

### Description

Generate random passwords from the terminal.

### Run

```bash
cd PassWordGenerator
python PassWordGenerator.py
```

This project is designed to demonstrate Python's randomization and string-handling capabilities.

---

## 09. 📱 QR Generator

### Description

Generate QR codes from text, URLs, or other information.

### Run

```bash
cd QRGenerator
python QRGenerator.py
```

### Typical dependency

```bash
pip install qrcode[pil]
```

---

## 10. 💻 System Information

### Description

Display useful information about the current computer and operating system.

### Run

```bash
cd SystemInfo
python SystemInfo.py
```

---

## 11. 🧹 Temporary Files Cleaner

### Description

A system utility for identifying and cleaning temporary files.

### Run

```bash
cd TemporaryFilesCleaner
python TemporaryFilesCleaner.py
```

> ⚠️ Review what the program is going to remove before using any file-cleaning utility.

---

## 12. 🔊 Text → Speech

### Description

Convert written text into spoken audio.

### Features

* English text-to-speech
* Hindi text-to-speech
* MP3 output
* User-defined output filename
* Automatic output folder

### Install

```bash
pip install gTTS
```

### Run

```bash
cd TextToSpeech
python TextToSpeech.py
```

The generated audio is saved in the project's speech output folder.

---

## 13. 🐢 Turtle Graphics

### Description

A graphics project using Python's built-in Turtle module to create drawings and animations.

### Run

```bash
cd "Turtle Graphics"
python TurtleGraphics.py
```

No external package is normally required because `turtle` is included with standard Python installations.

---

## 14. ⌨️ Typing Speed Test

### Description

A terminal-based typing speed test that measures typing performance.

### Features

* Typing challenge
* Time measurement
* Speed calculation
* Accuracy calculation

### Run

```bash
cd TypingSpeedTest
python TypingSpeedTest.py
```

---

## 15. 🎬 Video → Audio

### Description

Extract audio from video files and save it as an audio file.

### Requirements

* Python
* FFmpeg

### Run

```bash
cd VideoTOAudio
python VideoTOAudio.py
```

---

## 16. 🎞️ Video → GIF

### Description

Convert video clips into animated GIF files.

### Requirements

* Python
* FFmpeg

### Run

```bash
cd VideoToGIF
python VideoToGIF.py
```

---

## 17. 🎤 Vocal Extractor

### Description

An audio-processing project designed to separate vocals from instrumental/background audio.

### Run

```bash
cd VocalExtractor
python VocalExtractor.py
```

> Depending on the implementation, this project may require additional audio-processing or machine-learning dependencies.

---

## 18. ▶️ YouTube Downloader

### Description

A terminal-based YouTube downloading utility.

### Features

* Enter a video URL
* Download media from the terminal
* Audio/video processing
* FFmpeg integration

### Requirements

* Python
* `yt-dlp`
* FFmpeg

### Install

```bash
pip install yt-dlp
```

Install FFmpeg separately and make sure it is available in your system PATH.

### Run

```bash
cd YoutubeDownloader
python YoutubeDownloader.py
```

---

# 🛠️ Installing Common Dependencies

Some projects use third-party Python packages.

You can install them individually:

```bash
pip install gTTS
pip install Pillow
pip install python-barcode
pip install qrcode[pil]
pip install reportlab
pip install yt-dlp
```

For multimedia projects, install FFmpeg separately.

---

# 📁 Repository Structure

```text
Small-Python-Projects/
│
├── AudioCutter/
├── AudioMixer/
├── Barcode/
├── ImageCompressor/
├── ImgToPDF/
├── InvoiceGenerator/
├── PDF Locker/
├── PassWordGenerator/
├── QRGenerator/
├── SystemInfo/
├── TemporaryFilesCleaner/
├── TextToSpeech/
├── Turtle Graphics/
├── TypingSpeedTest/
├── VideoTOAudio/
├── VideoToGIF/
├── VocalExtractor/
├── YoutubeDownloader/
│
├── .gitignore
└── README.md
```

---

# 🎯 Purpose

This repository is a collection of small Python projects created to:

* Practice Python programming
* Learn Python libraries
* Experiment with automation
* Work with multimedia
* Build useful command-line utilities
* Understand file processing
* Turn programming ideas into working applications

The projects range from simple beginner utilities to more advanced multimedia tools.

---

# 📈 Learning Progress

The projects cover concepts such as:

* Python fundamentals
* Functions
* Loops
* Conditional statements
* File handling
* OS operations
* Subprocesses
* CLI applications
* Image processing
* PDF generation
* Audio processing
* Video processing
* Text-to-speech
* System utilities
* Third-party Python packages

---

# 🔮 Future Projects

This repository will continue to grow with more small Python projects.

Possible future additions:

* 📸 Image → ASCII Art
* 📁 File Organizer
* 🔍 Duplicate File Finder
* 🎵 MP3 Metadata Editor
* 📝 Markdown → PDF Converter
* 🖼️ Image Resizer
* 📊 CSV Analyzer
* 🌐 Website Status Checker
* 📋 Clipboard Manager
* 🎙️ Audio Recorder
* 🗜️ File Compressor
* 📑 PDF Merger
* 🧮 Advanced Calculator

---

# 👨‍💻 Author

**Prasham Jain**

GitHub: [@Prashamjn](https://github.com/Prashamjn)
X - [@Prasham_jn_](https://x.com/Prasham_jn_)
Instagram - [@Prasham_jn_](https://www.instagram.com/prasham_jn_/)

---

## ⭐ Support

If you find these projects useful or interesting, consider giving the repository a ⭐ on GitHub.

Happy Coding! 🐍💻
