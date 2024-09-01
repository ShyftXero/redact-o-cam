import cv2
import numpy as np
import pyfakewebcam
from PIL import Image, ImageSequence
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import time
import sys
import os
import dlib
import threading
import queue

console = Console()

def load_image(path):
    try:
        image = Image.open(path)
        if image.format == 'GIF':
            frames = []
            for frame in ImageSequence.Iterator(image):
                frame = frame.convert("RGBA")
                frame = np.array(frame)
                frames.append(frame)
            return frames
        else:
            image = image.convert("RGBA")
            return [np.array(image)]
    except FileNotFoundError:
        console.print(f"[bold red]Error:[/bold red] Image not found at {path}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Error loading image:[/bold red] {str(e)}")
        sys.exit(1)

def overlay_image(background, overlay, x, y):
    background_width = background.shape[1]
    background_height = background.shape[0]
    if x >= background_width or y >= background_height:
        return background
    h, w = overlay.shape[0], overlay.shape[1]
    if x + w > background_width:
        w = background_width - x
        overlay = overlay[:, :w]
    if y + h > background_height:
        h = background_height - y
        overlay = overlay[:h]
    
    overlay_image = overlay[..., :3]
    mask = overlay[..., 3:] / 255.0
    
    roi = background[y:y+h, x:x+w]
    blended = roi * (1.0 - mask) + overlay_image * mask
    background[y:y+h, x:x+w] = blended.astype(np.uint8)
    return background

def get_ansi_color(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

def frame_to_ascii(frame, width=100, height=30, color=False):
    frame = cv2.resize(frame, (width, height))
    ascii_chars = '@%#*+=-:. '  # Extended ASCII palette
    ascii_frame = []

    if color:
        for row in frame:
            ascii_row = ''
            for pixel in row:
                b, g, r = pixel
                char_index = int(np.mean(pixel) * (len(ascii_chars) - 1) / 255)
                ascii_char = ascii_chars[char_index]
                ascii_row += f"{get_ansi_color(r, g, b)}{ascii_char}"
            ascii_frame.append(ascii_row)
        return '\n'.join(ascii_frame) + '\033[0m'  # Reset color at the end
    else:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        for row in frame:
            ascii_row = ''.join([ascii_chars[int(pixel * (len(ascii_chars) - 1) / 255)] for pixel in row])
            ascii_frame.append(ascii_row)
        return '\n'.join(ascii_frame)

def apply_matrix_effect(frame, face_locations):
    matrix_frame = np.zeros_like(frame)
    matrix_frame[:, :, 1] = 32  # Dark green background

    characters = np.random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'), size=frame.shape[:2])
    char_brightness = np.random.randint(64, 192, size=frame.shape[:2])

    for y in range(frame.shape[0]):
        for x in range(frame.shape[1]):
            cv2.putText(matrix_frame, characters[y, x], (x*10, y*10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, int(char_brightness[y, x]), 0), 1)

    # Highlight face areas
    for (x, y, w, h) in face_locations:
        matrix_frame[y:y+h, x:x+w, 1] = 192  # Lighter green for faces

    return matrix_frame

def list_available_cameras():
    table = Table(title="Available Cameras")
    table.add_column("Index", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Resolution", style="green")

    index = 0
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            break
        ret, frame = cap.read()
        if ret:
            name = f"Camera {index}"
            resolution = f"{int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}"
            table.add_row(str(index), name, resolution)
        cap.release()
        index += 1

    if index == 0:
        console.print("[yellow]No cameras found.[/yellow]")
    else:
        console.print(table)

def get_video_capture(input_camera, input_file):
    if input_file:
        cap = cv2.VideoCapture(input_file)
        if not cap.isOpened():
            console.print(f"[bold red]Error:[/bold red] Could not open video file {input_file}")
            sys.exit(1)
    else:
        cap = cv2.VideoCapture(input_camera)
        if not cap.isOpened():
            console.print(f"[bold red]Error:[/bold red] Could not open camera {input_camera}")
            sys.exit(1)
    return cap

def process_frame(frame, face_detector, image_frames, frame_index, debug, x_offset, y_offset, scale):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = face_detector(rgb_frame)

    for face in faces:
        x, y, w, h = face.left(), face.top(), face.width(), face.height()
        
        # Apply scaling
        scaled_w = int(w * scale)
        scaled_h = int(h * scale)
        
        # Adjust position to keep the image centered after scaling
        x_adj = x + (w - scaled_w) // 2
        y_adj = y + (h - scaled_h) // 2
        
        image = cv2.resize(image_frames[frame_index], (scaled_w, scaled_h))
        frame = overlay_image(frame, image, x_adj + x_offset, y_adj + y_offset)
        if debug:
            console.print(Panel(f"Face redacted at: ({x_adj}, {y_adj}, {x_adj+scaled_w}, {y_adj+scaled_h})", 
                            title="Face Detected", border_style="green"))

    return frame, faces

def frame_processing_thread(input_queue, output_queue, face_detector, image_frames, debug, x_offset, y_offset, scale):
    frame_index = 0
    while True:
        frame = input_queue.get()
        if frame is None:
            break
        processed_frame, faces = process_frame(frame, face_detector, image_frames, frame_index, debug, x_offset, y_offset, scale)
        output_queue.put((processed_frame, faces))
        frame_index = (frame_index + 1) % len(image_frames)

def main(
    img_path: str = typer.Option('matrix_face.gif', "--img", help="Path to the image (PNG or GIF) for face redaction"),
    input_camera: int = typer.Option(0, "--input-camera", "-i", help="Input camera device number"),
    input_file: str = typer.Option(None, "--input-file", "-f", help="Input video file path"),
    ascii_output: bool = typer.Option(False, "--ascii", help="Render frame as ASCII to console"),
    color_ascii: bool = typer.Option(False, "--color-ascii", help="Render ASCII in color"),
    ascii_file: str = typer.Option(None, "--ascii-file", help="Save ASCII output to file"),
    matrix_mode: bool = typer.Option(False, "--matrix", help="Apply Matrix-style effect"),
    virtual_cam: bool = typer.Option(True, help="Output to virtual webcam"),
    virtual_cam_device: str = typer.Option("/dev/video4", help="Virtual webcam device"),
    list_cameras: bool = typer.Option(False, "--list-cameras", help="List available cameras and exit"),
    debug: bool = typer.Option(False, '--debug', help='show extra debug info'),
    x_offset: int = typer.Option(0, "--x-offset", help="Horizontal offset for image placement"),
    y_offset: int = typer.Option(0, "--y-offset", help="Vertical offset for image placement"),
    scale: float = typer.Option(1.0, "--scale", help="Scale factor for the cover image (e.g., 0.95 for 5% reduction, 1.25 for 25% increase)")
):
    if list_cameras:
        list_available_cameras()
        return

    if input_file and input_camera != 0:
        console.print("[bold red]Error:[/bold red] Please specify either input camera or input file, not both.")
        sys.exit(1)

    image_frames = load_image(img_path)

    cap = get_video_capture(input_camera, input_file)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fake_webcam = None
    if virtual_cam:
        try:
            fake_webcam = pyfakewebcam.FakeWebcam(virtual_cam_device, width, height)
        except Exception as e:
            console.print(f"[bold red]Error creating virtual webcam:[/bold red] {str(e)}")
            console.print("Continuing without virtual webcam output.")
            virtual_cam = False

    ascii_file_handle = None
    if ascii_file:
        try:
            ascii_file_handle = open(ascii_file, 'w')
        except IOError as e:
            console.print(f"[bold red]Error opening ASCII output file:[/bold red] {str(e)}")
            sys.exit(1)

    face_detector = dlib.get_frontal_face_detector()

    input_queue = queue.Queue(maxsize=5)
    output_queue = queue.Queue(maxsize=5)

    processing_thread = threading.Thread(
        target=frame_processing_thread,
        args=(input_queue, output_queue, face_detector, image_frames, debug, x_offset, y_offset, scale)
    )
    processing_thread.start()

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                if input_file:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Loop video file
                    continue
                else:
                    console.print("[bold yellow]Warning:[/bold yellow] Failed to capture frame")
                    break

            input_queue.put(frame)

            if not output_queue.empty():
                processed_frame, faces = output_queue.get()

                if matrix_mode:
                    processed_frame = apply_matrix_effect(processed_frame, [(face.left(), face.top(), face.width(), face.height()) for face in faces])

                if virtual_cam and fake_webcam:
                    frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
                    fake_webcam.schedule_frame(frame_rgb)

                if ascii_output or ascii_file:
                    ascii_frame = frame_to_ascii(processed_frame, color=color_ascii)
                    if ascii_output:
                        if color_ascii:
                            print(ascii_frame)  # Use print for ANSI color codes
                        else:
                            console.print(ascii_frame)
                    if ascii_file_handle:
                        ascii_file_handle.write(ascii_frame + '\n\n')

                cv2.imshow('Face Redaction', processed_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        console.print("[bold green]Shutting down gracefully...[/bold green]")
    finally:
        input_queue.put(None)  # Signal the processing thread to stop
        processing_thread.join()
        cap.release()
        cv2.destroyAllWindows()
        if ascii_file_handle:
            ascii_file_handle.close()

if __name__ == "__main__":
    typer.run(main)