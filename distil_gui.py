import sys
import distil_engine
import requests
import traceback
from PySide6.QtWidgets import QInputDialog
from distil_engine import *

from PySide6.QtCore import Qt, QTimer

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QLineEdit,
    QLabel,
    QProgressBar
)


class BootScreen(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("DISTIL")

        self.setFixedSize(650, 350)

        self.setStyleSheet("""
        QWidget{
            background:#121212;
            color:white;
        }

        QLabel{
            font-family:Consolas;
        }

        QProgressBar{
            border:1px solid #444;
            background:#222;
            height:24px;
            text-align:center;
        }

        QProgressBar::chunk{
            background:#00d26a;
        }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.title = QLabel("DISTIL")

        self.title.setStyleSheet(
            "font-size:34px;font-weight:bold;"
        )

        self.status = QLabel(
            "INITIALISING CORE..."
        )

        self.bar = QProgressBar()

        self.bar.setMaximum(100)

        layout.addWidget(self.title)
        layout.addSpacing(20)
        layout.addWidget(self.status)
        layout.addSpacing(10)
        layout.addWidget(self.bar)

        self.setLayout(layout)

        play_sound(
            "jarvis_online.mp3"
        )

        self.progress = 0

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.update_boot
        )

        self.timer.start(180)

    def update_boot(self):

        self.progress += 6

        self.bar.setValue(
            self.progress
        )

        if self.progress == 24:

            self.status.setText(
                "Loading AI Assistant..."
            )

        elif self.progress == 48:

            self.status.setText(
                "Loading Spotify..."
            )

        elif self.progress == 72:

            self.status.setText(
                "Loading Automations..."
            )

        elif self.progress == 96:

            self.status.setText(
                "DISTIL OS ONLINE"
            )

        if self.progress >= 100:

            self.timer.stop()

            self.main = DistilGUI()

            self.main.show()

            self.close()


class DistilGUI(QWidget):

    def __init__(self):

        super().__init__()
        self.setStyleSheet("""
        QWidget{
            background:#121212;
            color:white;
        }
        """)

        self.setWindowTitle("DISTIL OS")

        self.resize(1100, 650)

        from PySide6.QtWidgets import QHBoxLayout

        import subprocess
        import psutil
        from datetime import datetime

        self.subprocess = subprocess
        self.psutil = psutil
        self.datetime = datetime

        main_layout = QHBoxLayout()

        left = QVBoxLayout()

        right = QVBoxLayout()

        self.output = QTextEdit()
        self.output.setStyleSheet("""
        QTextEdit{
            background:#0d1117;
            color:#00ff88;
            border:2px solid #262626;
            border-radius:14px;
            padding:12px;
            font-family:Menlo;
            font-size:15px;
        }
        """)

        self.output.setReadOnly(True)

        self.entry = QLineEdit()

        self.output.setStyleSheet("""
        QTextEdit{
            background:#0d1117;
            color:#00ff88;
           border:2px solid #1f8f5a;
            border-radius:14px;
            padding:12px;
            font-family:Menlo;
            font-size:15px;
        }
        """)

        self.entry.setPlaceholderText(
            "Ask DISTIL..."
        )
        left.addWidget(
            self.output
        )

        left.addWidget(
            self.entry
        )

        self.status = QLabel()

        self.status.setStyleSheet("""
        QLabel{

        background:#1b1b1b;

        border:2px solid #303030;

        border-radius:18px;

        padding:24px;

        font-family:Menlo;

        font-size:16px;

        color:lightblue;

        }
        """)

        right.addWidget(
            self.status
        )

        main_layout.addLayout(
            left,
            3
        )

        main_layout.addLayout(
            right,
            1
        )

        self.setLayout(
            main_layout
        )

        distil_engine.gui_logger = self.log

        self.entry.returnPressed.connect(
            self.run_command
        )

        self.output.append("""
        <h1 style="color:#00ff88;">DISTIL</h1>

        Welcome back <b>Harley</b>.

        All systems online.

        Type <span style="color:#00ff88;">help</span> to begin.
        """)

        self.weather = self.get_weather

        self.spotify = self.get_spotify()

        self.weather_timer = QTimer()

        self.weather_timer.timeout.connect(
            self.refresh_weather
        )

        self.weather_timer.start(10000)

        self.spotify_timer = QTimer()

        self.spotify_timer.timeout.connect(
            self.refresh_spotify
        )

        self.spotify_timer.start(
            1000
        )

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.update_status
        )

        self.timer.start(
            1000
        )

        self.update_status()

        QTimer.singleShot(
            1500,
            self.startup_face_music
        )

        self.entry.setFocus()

    def get_spotify(self):

        try:

            script = '''
            tell application "Spotify"

                if player state is playing then

                    set trackName to name of current track

                    set artistName to artist of current track

                    return "▶ " & trackName & " - " & artistName

                else

                    return "⏸ Spotify Paused"

                end if

            end tell
            '''

            output = self.subprocess.check_output(
                [
                    "osascript",
                    "-e",
                    script
                ]
            )

            return output.decode().strip()

        except:

            return "Spotify Closed"

    def startup_face_music(self):

        detected = check_face_background()

        if detected:

            song, ok = QInputDialog.getText(
                self,
                "DISTIL",
                "Welcome back Harley.\nWhat song do you want?"
            )

            if ok and song.strip():
                play_spotify(
                    song.strip()
                )

    def log(self, text):

        self.output.append(text)

    @property
    def get_weather(self):

        try:

            url = (
                "https://api.open-meteo.com/v1/forecast"
                "?latitude=53.1848"
                "&longitude=-3.0258"
                "&current=temperature_2m,weather_code"
            )

            response = requests.get(
                url,
                timeout=5
            )

            data = response.json()

            print(data)

            current = data["current"]

            temp = current["temperature_2m"]

            code = current["weather_code"]

            weather_codes = {

                0: "☀️ Clear",
                1: "🌤 Mainly Clear",
                2: "⛅ Partly Cloudy",
                3: "☁️ Cloudy",

                45: "🌫 Fog",
                48: "🌫 Fog",

                51: "🌦 Drizzle",
                53: "🌦 Drizzle",
                55: "🌦 Drizzle",

                61: "🌧 Rain",
                63: "🌧 Rain",
                65: "🌧 Heavy Rain",

                71: "❄️ Snow",
                73: "❄️ Snow",
                75: "❄️ Heavy Snow",

                95: "⛈ Thunderstorm"

            }

            weather = weather_codes.get(
                code,
                "Unknown"
            )

            return f"{weather}\n{temp}°C"

        except Exception as e:

                traceback.print_exc()

                return "Unavailable"

    def refresh_weather(self):

        self.weather = self.get_weather
        self.spotify = self.get_spotify()

    def refresh_spotify(self):

        self.spotify = self.get_spotify()

    def update_status(self):

        battery = self.subprocess.check_output(
            [
                "pmset",
                "-g",
                "batt"
            ]
        ).decode()

        percent = "Unknown"

        for part in battery.split():

            if "%" in part:

                percent = part

                break

        ram = self.psutil.virtual_memory()

        cpu = self.psutil.cpu_percent()

        self.status.setText(
            f"""
        <h1 style="color:#00ff88;">🟢 DISTIL</h1>

        <div style="color:#888;">
        PERSONAL ASSISTANT
        </div>

        <hr>

        <b>🕒 TIME</b><br>
        {self.datetime.now().strftime("%H:%M:%S")}

        <br><br>

        <b>🎵 NOW PLAYING</b><br>
        {self.spotify}

        <br><br>

        <b>🌤 WEATHER</b><br>
        {self.weather}

        <br><br>

        <b>🔋 BATTERY</b><br>
        {percent}

        <br><br>

        <b>🖥 CPU</b><br>
        {cpu}%

        <br><br>

        <b>💾 RAM</b><br>
        {round(ram.used / (1024 ** 3), 1)} GB
        """
        )

    def run_command(self):

        command = self.entry.text().strip().lower()

        if command == "":
            return

        self.output.append(
            f'<b> <span style="color:#00ff88;">❯</span> {command}'
        )

        self.entry.clear()

        if handle_natural_command(command):
            return

        if command == "help":

            help_menu()

        elif command == "study":

            study()

        elif command == "focus":

            focus()

        elif command == "status":

            status()

        elif command == "exit":

            self.close()

        else:

            self.output.append(
                "Unknown command."
            )

app = QApplication(sys.argv)

boot = BootScreen()

boot.show()

sys.exit(
    app.exec()
)