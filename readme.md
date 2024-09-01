# 👁️ REDACT-O-CAM 🕵️‍♂️

## 🎭 What's This Madness?

This little gem of code is your ticket to digital anonymity in a world that's about as private as a glass-walled public restroom. Whether you're dodging the fashion police, hiding from your ex, or just tired of AI trying to guess your age (and failing miserably), this tool has got you covered. Literally.

## 🚀 Features

- **Face Redaction**: Turn your face into whatever you want! A cat, a potato, or that painting your aunt made that no one can quite figure out.
- **GIF Support**: Because static images are so last century. Now your face can be a looping meme!
- **Offset Adjustment**: For when you want your digital mask to be just a little bit off-center, like your sense of humor.
- **Scaling**: Make your cover image bigger or smaller. Perfect for when you're feeling particularly big-headed or humble.
- **Virtual Webcam Output**: Fool your video calls into thinking you're a respectable member of society.
- **ASCII Art Mode**: For those who think life is better in text format.
- **Matrix Mode**: Embrace your inner Neo and dodge those digital bullets!

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
- Uncontrollable laughter from coworkers
- Existential crises about the nature of reality and identity
- The sudden urge to wear a tinfoil hat

## 🎩 Final Thoughts

Remember, in a world of constant surveillance, the best defense is a good offense. Or in this case, a ridiculously fun face redaction tool. Stay safe, stay sane, and may your digital face always be as mysterious as the ingredients in a hot dog!

**P.S.** If you're reading this, you're probably on a list somewhere. But hey, at least you're in good company! 👋
