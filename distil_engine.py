import subprocess
import os
import time
import json
import pyautogui
import cv2
from datetime import datetime
import psutil
import shutil
import threading

gui_logger = None


def log(text):

    if gui_logger:

        gui_logger(text)

    else:

        print(text)

DISTIL_FOLDER = "/Users/harleynoble16/Year2Python/DISTIL"

SOUNDS_FOLDER = os.path.join(
    DISTIL_FOLDER,
    "sounds"
)

EYE_FILE = os.path.join(
    DISTIL_FOLDER,
    "eye_calibration.json"
)

WEBSITES = {
    "youtube": "https://youtube.com",
    "chatgpt": "https://chatgpt.com",
    "github": "https://github.com",
    "netflix": "https://netflix.com",
    "enor": "https://www.enorclothing.com"
}

SPOTIFY_ALIASES = {
    "gym": "gym playlist",
    "study": "study playlist",
    "lofi": "lofi playlist",
    "chill": "chill study mix",
    "phonk": "phonk playlist"
}
gesture_active = True
gesture_camera = None


def play_sound(file_name):
    path = os.path.join(
        SOUNDS_FOLDER,
        file_name
    )

    if os.path.exists(path):
        subprocess.Popen([
            "afplay",
            path
        ])


def speak(text):
    subprocess.run([
        "say",
        text
    ])

def media_pause():

    subprocess.run([
        "osascript",
        "-e",
        'tell application "Spotify" to playpause'
    ])

def media_next():
    subprocess.run([
        "osascript",
        "-e",
        'tell application "Spotify" to next track'
    ])


def media_previous():
    subprocess.run([
        "osascript",
        "-e",
        'tell application "Spotify" to previous track'
    ])


def boot():
    print()
    print("INITIALISING DISTIL CORE...\n")

    steps = [
        "█□□□□□□□□□□□□□□□ 06%",
        "██□□□□□□□□□□□□□□ 12%",
        "███□□□□□□□□□□□□□ 18%",
        "████□□□□□□□□□□□□ 24%",
        "█████□□□□□□□□□□□ 30%",
        "██████□□□□□□□□□□ 36%",
        "███████□□□□□□□□□ 42%",
        "████████□□□□□□□□ 48%",
        "█████████□□□□□□□ 54%",
        "██████████□□□□□□ 60%",
        "███████████□□□□□ 66%",
        "████████████□□□□ 72%",
        "█████████████□□□ 78%",
        "██████████████□□ 84%",
        "███████████████□ 90%",
        "████████████████ 96%",
        "████████████████ 100%"
    ]

    play_sound(
        "jarvis_online.mp3"
    )

    for step in steps:
        print(step)
        time.sleep(1)

    print()
    print("DISTIL OS ONLINE")
    print(f"Time: {datetime.now().strftime('%H:%M')}")
    print("Type help\n")

def gesture_mode():

    cam = cv2.VideoCapture(0)

    print("Motion gesture active.\n")

    print("Right = next")
    print("Left = previous")
    print("Up = play pause\n")

    last_frame = None

    gesture_started = False

    start_x = None
    start_y = None

    last_action = 0

    RIGHT_TRIGGER = 400
    LEFT_TRIGGER = 390
    UP_TRIGGER = 220

    COOLDOWN = 2.5

    MIN_AREA = 4000
    MIN_WIDTH = 350
    MIN_HEIGHT = 220

    while True:

        success, frame = cam.read()

        if not success:
            break

        frame = cv2.flip(
            frame,
            1
        )

        frame_width = frame.shape[1]
        frame_height = frame.shape[0]

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        gray = cv2.GaussianBlur(
            gray,
            (15, 15),
            0
        )

        if last_frame is None:

            last_frame = gray
            continue

        diff = cv2.absdiff(
            last_frame,
            gray
        )

        threshold = cv2.threshold(
            diff,
            25,
            255,
            cv2.THRESH_BINARY
        )[1]

        contours, _ = cv2.findContours(
            threshold,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        biggest_x = None
        biggest_y = None

        biggest_area = 0

        for contour in contours:

            area = cv2.contourArea(
                contour
            )

            if area < MIN_AREA:
                continue

            x, y, w, h = cv2.boundingRect(
                contour
            )

            if w < MIN_WIDTH:
                continue

            if h < MIN_HEIGHT:
                continue

            centre_x = x + (w // 2)
            centre_y = y + (h // 2)

            if centre_y < frame_height * 0.45:
                continue

            if not (
                frame_width * 0.20
                <
                centre_x
                <
                frame_width * 0.80
            ):
                continue

            if area > biggest_area:

                biggest_area = area

                biggest_x = centre_x
                biggest_y = centre_y

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )

        now = time.time()

        if biggest_x:

            if not gesture_started:

                gesture_started = True

                start_x = biggest_x
                start_y = biggest_y

            if now - last_action > COOLDOWN:

                movement_x = (
                    biggest_x -
                    start_x
                )

                movement_y = (
                    start_y -
                    biggest_y
                )

                if movement_y > UP_TRIGGER:

                    media_pause()

                    print(
                        "PLAY / PAUSE"
                    )

                    last_action = now

                    gesture_started = False


                elif movement_x > RIGHT_TRIGGER:

                    media_next()

                    print(
                        "NEXT"
                    )

                    last_action = now

                    gesture_started = False


                elif movement_x < -LEFT_TRIGGER:

                    media_previous()

                    print(
                        "PREVIOUS"
                    )

                    last_action = now

                    gesture_started = False

        else:

            gesture_started = False

            start_x = None
            start_y = None

        cv2.putText(
            frame,
            "DISTIL MEDIA",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.imshow(
            "DISTIL Motion Gesture",
            frame
        )

        last_frame = gray

        if cv2.waitKey(1) == 27:
            break

    cam.release()

    cv2.destroyAllWindows()

    print(
        "Gesture mode offline.\n"
    )

def get_biggest_face(faces):
    biggest_face = None
    biggest_area = 0

    for x, y, w, h in faces:
        area = w * h

        if area > biggest_area:
            biggest_area = area
            biggest_face = (
                x,
                y,
                w,
                h
            )

    return biggest_face


def get_middle_faces(
    faces,
    frame_width
):
    return [
        (x, y, w, h)
        for x, y, w, h in faces
        if frame_width * 0.30 <
        x + (w // 2) <
        frame_width * 0.70
    ]


def face_debug():
    cam = cv2.VideoCapture(0)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml"
    )

    print("Face debug active. Press ESC to stop.\n")

    while True:
        success, frame = cam.read()

        if not success:
            break

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        gray = cv2.equalizeHist(
            gray
        )

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=2,
            minSize=(30, 30)
        )

        frame_width = frame.shape[1]

        faces = get_middle_faces(
            faces,
            frame_width
        )

        face = get_biggest_face(
            faces
        )

        count = 0

        if face:
            x, y, w, h = face
            count = 1

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

        cv2.putText(
            frame,
            f"Faces: {count}",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.imshow(
            "DISTIL Face Debug",
            frame
        )

        if cv2.waitKey(1) == 27:
            break

    cam.release()
    cv2.destroyAllWindows()


def eye_calibrate():
    cam = cv2.VideoCapture(0)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml"
    )

    positions = {}

    for label in [
        "centre",
        "left",
        "right"
    ]:
        input(
            f"Move head {label} then press Enter..."
        )

        time.sleep(1)

        success, frame = cam.read()

        if not success:
            continue

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        gray = cv2.equalizeHist(
            gray
        )

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=2,
            minSize=(30, 30)
        )

        frame_width = frame.shape[1]

        faces = get_middle_faces(
            faces,
            frame_width
        )

        face = get_biggest_face(
            faces
        )

        if not face:
            continue

        x, y, w, h = face

        positions[label] = int(
            x + (w // 2)
        )

        print(
            f"{label} saved at {positions[label]}."
        )

    cam.release()

    with open(
        EYE_FILE,
        "w"
    ) as file:
        json.dump(
            positions,
            file
        )

    print(
        "Eye calibration saved.\n"
    )


def load_eye_calibration():
    if not os.path.exists(
        EYE_FILE
    ):
        return None

    with open(
        EYE_FILE,
        "r"
    ) as file:
        return json.load(
            file
        )


def eye_tracking():
    positions = load_eye_calibration()

    if not positions:
        print(
            "Run eye calibrate first.\n"
        )
        return

    cam = cv2.VideoCapture(0)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml"
    )

    print(
        "Head tracking active. Press ESC to stop.\n"
    )

    last_direction = ""

    while True:
        success, frame = cam.read()

        if not success:
            break

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        gray = cv2.equalizeHist(
            gray
        )

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.05,
            minNeighbors=2,
            minSize=(30, 30)
        )

        frame_width = frame.shape[1]

        faces = get_middle_faces(
            faces,
            frame_width
        )

        face = get_biggest_face(
            faces
        )

        direction = "CENTRE"

        if face:
            x, y, w, h = face

            current = int(
                x + (w // 2)
            )

            distances = {
                "LEFT": abs(
                    current -
                    positions["left"]
                ),
                "CENTRE": abs(
                    current -
                    positions["centre"]
                ),
                "RIGHT": abs(
                    current -
                    positions["right"]
                )
            }

            direction = min(
                distances,
                key=distances.get
            )

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

        if direction != last_direction:
            print(
                direction
            )

            last_direction = direction

        cv2.putText(
            frame,
            direction,
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.imshow(
            "DISTIL Tracking",
            frame
        )

        if cv2.waitKey(1) == 27:
            break

    cam.release()
    cv2.destroyAllWindows()


def open_spotify_search(search):
    pyautogui.hotkey(
        "command",
        "space"
    )

    time.sleep(0.2)

    pyautogui.write(
        "Spotify"
    )

    pyautogui.press(
        "enter"
    )

    time.sleep(1)

    pyautogui.hotkey(
        "command",
        "l"
    )

    time.sleep(0.5)

    pyautogui.write(
        search,
        interval=0.02
    )

    pyautogui.press(
        "enter"
    )

    time.sleep(2)


def play_spotify(search):
    search = SPOTIFY_ALIASES.get(
        search,
        search
    )

    open_spotify_search(
        search
    )

    pyautogui.press(
        "enter"
    )

    time.sleep(2)

    pyautogui.moveTo(
        355,
        330,
        duration=0.2
    )

    pyautogui.click()

    print(
        f"Playing {search}.\n"
    )


def search_spotify(search):
    open_spotify_search(
        search
    )

    print(
        f"Spotify search opened for {search}.\n"
    )


def google_search(search):
    query = search.replace(
        " ",
        "+"
    )

    url = (
        f"https://www.google.com/search?q={query}"
    )

    subprocess.run([
        "open",
        "-a",
        "Safari",
        url
    ])

    print(
        f"Searching Google for {search}.\n"
    )

def open_app_by_name(app_name):

    subprocess.run([
        "open",
        "-a",
        app_name
    ])


def take_screenshot():
    app_name = input(
        "Which app: "
    ).strip()

    name = input(
        "Screenshot name: "
    ).strip()

    if not name:
        name = "screenshot"

    try:
        open_app_by_name(
            app_name
        )

        time.sleep(1)

    except:
        pass

    file_name = f"{name}.png"

    path = os.path.join(
        DISTIL_FOLDER,
        file_name
    )

    screenshot = pyautogui.screenshot()

    screenshot.save(
        path
    )

    print(
        f"Screenshot saved: {file_name}\n"
    )


def open_website(name):
    if name not in WEBSITES:
        return False

    subprocess.run([
        "open",
        "-a",
        "Safari",
        WEBSITES[name]
    ])

    print(
        f"{name} opened.\n"
    )

    return True


def open_app(app_name):
    open_app_by_name(
        app_name
    )

    print(
        f"{app_name} opened.\n"
    )


def type_in_app(
    app_name,
    text
):
    open_app_by_name(
        app_name
    )

    time.sleep(2)

    if app_name.lower() == "notes":
        pyautogui.hotkey(
            "command",
            "n"
        )

    time.sleep(1)

    pyautogui.write(
        text,
        interval=0.02
    )

    print(
        "Text typed.\n"
    )


def study():
    open_app_by_name(
        "Safari"
    )

    open_app_by_name(
        "Spotify"
    )

    open_app_by_name(
        "PyCharm"
    )

    subprocess.run([
        "open",
        os.path.expanduser(
            "~/Documents"
        )
    ])

    subprocess.run([
        "open",
        "https://chatgpt.com"
    ])

    print(
        "Study workspace loaded.\n"
    )


def focus():
    study()

    play_spotify(
        "study"
    )

    print(
        "FOCUS MODE ACTIVE."
    )

    speak(
        "Focus mode active"
    )


def add_note():
    file_name = input(
        "File name: "
    ).strip()

    note = input(
        "Write note: "
    )

    path = os.path.join(
        DISTIL_FOLDER,
        f"{file_name}.txt"
    )

    with open(
        path,
        "w"
    ) as file:
        file.write(
            f"{datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n{note}"
        )

    print(
        "Note saved.\n"
    )

def shutdown_in(hours):

    def task():

        time.sleep(
            hours * 3600
        )

        subprocess.run([
            "osascript",
            "-e",
            'tell application "System Events" to shut down'
        ])

    threading.Thread(
        target=task,
        daemon=True
    ).start()

    print(
        f"Mac will shut down in {hours} hour(s).\n"
    )

def help_menu():
    print("""""
play gym
play study
search spotify eminem
google sql joins
gesture
screenshot
face debug
eye calibrate
eye
open notes and type hello
open youtube
open github
make note
study
focus
status
close all
exit
""""")


def status():

    total, used, free = shutil.disk_usage("/")

    ram = psutil.virtual_memory()

    cpu = psutil.cpu_percent(
        interval=1
    )

    battery_info = subprocess.check_output([
        "pmset",
        "-g",
        "batt"
    ]).decode()

    battery_percent = "Unknown"

    for part in battery_info.split():

        if "%" in part:

            battery_percent = part
            break

    print("\nDISTIL STATUS\n")

    print(
        f"Battery: {battery_percent}"
    )

    print(
        f"Time: {datetime.now().strftime('%H:%M')}"
    )

    print(
        f"Storage Free: {round(free / (1024**3))} GB"
    )

    print(
        f"RAM Used: {round(ram.used / (1024**3),1)} GB"
    )

    print(
        f"CPU Usage: {cpu}%\n"
    )

def handle_natural_command(command):

    if command.startswith("play "):
        search = command.replace(
            "play ",
            "",
            1
        ).strip()

        play_spotify(
            search
        )

        return True

    if command.startswith(
        "search spotify "
    ):
        search = command.replace(
            "search spotify ",
            "",
            1
        ).strip()

        search_spotify(
            search
        )

        return True

    if command.startswith(
        "google "
    ):
        search = command.replace(
            "google ",
            "",
            1
        ).strip()

        google_search(
            search
        )

        return True

    if command.startswith("close "):
        app_name = command.replace(
            "close ",
            "",
            1
        ).strip()

        subprocess.run([
            "osascript",
            "-e",
            f'tell application "{app_name}" to quit'
        ])

        print(
            f"{app_name} closed.\n"
        )
        return True

    if command == "gesture":
        gesture_mode()
        return True

    if command == "screenshot":
        take_screenshot()
        return True

    if command == "face debug":
        face_debug()
        return True

    if command == "eye calibrate":
        eye_calibrate()
        return True

    if command == "eye":
        eye_tracking()
        return True

    if command.startswith(
        "open "
    ) and " and type " in command:

        parts = command.replace(
            "open ",
            "",
            1
        ).split(
            " and type "
        )

        app_name = parts[0].strip()
        text = parts[1].strip()

        type_in_app(
            app_name,
            text
        )

        return True

    if command == "status":
        status()

        return True

    if command.startswith(
        "open "
    ):
        target = command.replace(
            "open ",
            "",
            1
        ).strip()

        if open_website(
            target
        ):
            return True

        open_app(
            target
        )

        return True

    if command.startswith(
        "make note"
    ):
        add_note()
        return True

from pathlib import Path
import os
import sys

if getattr(sys, "frozen", False):

    base_path = Path(sys._MEIPASS)

else:

    base_path = Path(__file__).parent

cascade_path = (
    base_path /
    "haarcascade_frontalface_default.xml"
)

def check_face_background():

    cam = cv2.VideoCapture(0)

    face_cascade = cv2.CascadeClassifier(
        str(cascade_path)
    )

    start_time = time.time()

    detected = False

    while time.time() - start_time < 5:

        success, frame = cam.read()

        if not success:
            break

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=4,
            minSize=(80, 80)
        )

        if len(faces) > 0:
            detected = True
            break

    cam.release()

    return detected