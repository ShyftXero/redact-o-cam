# 👁️ REDACT-O-CAM 🕵️‍♂️

replace your face with a png or gif and create a virtual video device so you can use it in teams or for a live stream or something. 
## 🚀 Features

- **Face Redaction**:
- **GIF Support**: 
- **Offset Adjustment**:
- **Scaling**: 
- **Virtual Webcam Output**:
- **ASCII Art Mode**: 
- **Matrix Mode**: 

## 🛠️ Installation

1. Clone this repo (or don't, we're not the boss of you).
2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Question your life choices that led you to install yet another Python package.

## 🕹️ Usage

```
python redactocam.py &&  vlc v4l2:///dev/video4 # to start the cam and open the stream in a third party tool. could be discord, teams, etc. 
# OR 
python redactocam.py --img path/to/your/disguise.png --x-offset 10 --y-offset -5 --scale 1.1
```

```
./redactocam.py --help
                                                                                                                                                           
 Usage: redactocam.py [OPTIONS]                                                                                                                            
                                                                                                                                                           
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --img                                         TEXT     Path to the image (PNG or GIF) for face redaction [default: matrix_face.gif]                     │
│ --input-camera        -i                      INTEGER  Input camera device number [default: 0]                                                          │
│ --input-file          -f                      TEXT     Input video file path [default: None]                                                            │
│ --ascii                                                Render frame as ASCII to console                                                                 │
│ --color-ascii                                          Render ASCII in color                                                                            │
│ --ascii-file                                  TEXT     Save ASCII output to file [default: None]                                                        │
│ --matrix                                               Apply Matrix-style effect                                                                        │
│ --virtual-cam             --no-virtual-cam             Output to virtual webcam [default: virtual-cam]                                                  │
│ --virtual-cam-device                          TEXT     Virtual webcam device [default: /dev/video4]                                                     │
│ --list-cameras                                         List available cameras and exit                                                                  │
│ --debug                                                show extra debug info                                                                            │
│ --x-offset                                    INTEGER  Horizontal offset for image placement [default: 0]                                               │
│ --y-offset                                    INTEGER  Vertical offset for image placement [default: 0]                                                 │
│ --scale                                       FLOAT    Scale factor for the cover image (e.g., 0.95 for 5% reduction, 1.25 for 25% increase)            │
│                                                        [default: 1.0]                                                                                   │
│ --help                                                 Show this message and exit.                                                                      │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```


Replace `path/to/your/disguise.png` with whatever image you want to hide behind. Maybe a picture of your cat? Everyone loves cats on the internet!

## 🚨 Disclaimer

This tool is for entertainment purposes only. We are not responsible for:
- Accidental identity reveals
