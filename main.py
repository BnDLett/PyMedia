import sys

import argparse
import colorama
import os
import threading
import time
import yt_dlp
from PyQt6.QtWidgets import *
from pygame import mixer

from letts_utils import queue

mixer.init()

version = "1.4.0a"

colorama.init(True)
print(f"{colorama.Back.YELLOW}Halt! This is a dev release, expect bugs and incomplete features. Current version is "
      f"{version}.")

ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
    'outtmpl': "cache/%(title)s-%(id)s.%(ext)s",
    "paths": {'mp3': 'cache', 'webm': 'cache'},
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

help_info = """
Commands:
 play - Play an audio by link or search term. 
   Usage: play [link]
   Aliases: start, queue
 pause - Pause the currently playing audio.
   Usage: pause
 resume - Resumes the paused audio. Has no effect if audio isn't paused.
   Usage: resume
   Aliases: unpause, continue
 exit - Exits the program. 
   Usage: exit
   Aliases: leave, quit
 stop - Stops the currently playing audio.
   Usage: stop

Flags:
 -nocache - Will delete the .wav file once it is done playing, this is useful for when you're minimizing disk space usage.
   Usage: play [link] -nocache
   Aliases: -n
"""  # I understand this may be bad practice however for now I'll keep it this way, it simplifies the program.

global audio_process
global audio_queue
global audio_thread
audio_process = mixer.Channel
audio_thread = False
audio_queue = queue.Queue()


def download_audio(link: str):
    """
    Downloads audio using the YT-DLP library.
    :param link: The link to the audio to be downloaded.
    :return:
    """
    print("Loading audio... this may take a moment.")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        if link.startswith("https://") == False and link.startswith("www.") == False:
            funny_dict = ydl.extract_info(f"ytsearch:{link}", download=False)['entries'][0]['id']
            link = f"https://youtube.com/watch?v={funny_dict}"
        elif link.startswith("http://"):
            print("Visiting http websites is unsafe, please refrain from visiting websites using http and not https as "
                  "they're insecure.")

        info = ydl.extract_info(link, False)
        info = ydl.prepare_filename(info)

        print(info)

        if info.endswith(".webm"):
            info = info.replace(".webm", ".mp3")
        else:
            print(1)
            info = info.replace(info[-4:], ".mp3")

        print(info)

        if os.path.exists(info):  # This is for caches (if any)
            return info
        ydl.download([link])

    return info


def start_audio():
    """
    Starts the audio thread and deletes audio cache if specified.
    :return:
    """

    global audio_thread, file
    while True:
        if audio_queue.empty():
            audio_thread = False
            return

        try:
            file = audio_queue.get_next_item()
        except Exception as exc:
            print(f"{colorama.Fore.RED}An error has occured:\n{exc}")
            pass

        global audio_process
        global paused
        # audio_wavobj = simpleaudio.WaveObject.from_wave_file(file[0])
        # audio_process = audio_wavobj.play()
        # audio_process.wait_done()
        tada = mixer.Sound(file[0])
        audio_process = tada.play()
        paused = False
        while audio_process.get_busy():
            time.sleep(0.1)
        # if file[1]:
        #     os.remove(f"{file[0]}")
        # TODO: Reimplement this in a manner that supports queuing. This will be implemented in v1.5.0a


def attempt_clear():
    """
    Attempts to clear the terminal. Does not work for macOS.
    :return:
    """
    try:
        os.system("clear")
    except Exception as hi_neko:  # This is not tested on a Windows machine yet.
        os.system("cls")


def prepare_and_play(link: str = None, del_cache: bool = True):
    """
    Prepares and plays audio using YT-DLP and PyGame Mixer.
    :param link: The link for the audio to be downloaded.
    :param del_cache: If audio cache should be deleted or not.
    :return:
    """

    print(link)
    global audio_thread
    file_loc = download_audio(link)
    audio_queue.append_to_queue([file_loc, del_cache])
    if not audio_thread:
        audio_thread = threading.Thread(target=start_audio, name="PyMedia Audio Player")
        audio_thread.start()


def user_interface():
    """
    CLI user interface
    :return:
    """

    while True:
        clear = True
        del_cache = False
        user_input = input("Please enter a command. Use help for a list of commands.\n> ").split(" ")

        try:
            if user_input[2] in ["-nocache", "-n"]:
                del_cache = True
        except:
            pass

        if user_input[0].lower() in ["help", "-?"]:
            attempt_clear()
            clear = False
            print(help_info)

        elif user_input[0].lower() in ["play", "start", "queue"]:
            prepare_and_play(link=user_input[1], del_cache=del_cache)

        elif user_input[0].lower() in ["pause"]:
            audio_process.pause()

        elif user_input[0].lower() in ["continue", "resume", "unpause"]:
            audio_process.unpause()

        elif user_input[0].lower() in ["stop"]:
            audio_process.stop()

        elif user_input[0].lower() in ["quit", "exit", "leave"]:
            exit()

        if clear:
            attempt_clear()


def previous_in_queue():
    audio_process.stop()
    audio_queue.get_previous_items(True)


class GUIInterface(QMainWindow):
    """
    GUI interface
    :return:
    """

    def __init__(self, program_version):
        super().__init__()

        global audio_process
        global paused
        paused = False

        self.__audio_process__ = audio_process
        self.__paused__ = paused
        self.__version__ = program_version
        self.spacing = 5

        self.setWindowTitle(f"PyMedia {self.__version__}")
        self.setGeometry(0, 0, 600, 200)

        self.link = QLineEdit("", self)
        self.link.setGeometry(5, 5, 325, 25)

        enter = QPushButton("Enter", self)
        enter.clicked.connect(self.run_audio)
        enter.setGeometry((self.link.x() + self.link.width()) + self.spacing, self.link.y(), 50, self.link.height())

        self.previous_btn = QPushButton("Previous", self)
        self.previous_btn.clicked.connect(previous_in_queue)
        self.previous_btn.setGeometry(self.link.x(), (self.link.y() + self.link.height()) + self.spacing, 70,
                                      self.link.height())

        self.pause_play = QPushButton("Pause/Play", self)
        self.pause_play.clicked.connect(self.change_pause_state)
        self.pause_play.setGeometry((self.previous_btn.x() + self.previous_btn.width()) + self.spacing,
                                    self.previous_btn.y(),
                                    self.previous_btn.width(), self.previous_btn.height())

        self.skip_btn = QPushButton("Skip", self)
        self.skip_btn.clicked.connect(lambda: audio_process.stop())
        self.skip_btn.setGeometry((self.pause_play.x() + self.pause_play.width()) + self.spacing, self.pause_play.y(),
                                  self.pause_play.width(), self.pause_play.height())

        self.pause_play.setDisabled(audio_queue.empty())
        self.skip_btn.setDisabled(audio_queue.empty())

    def change_pause_state(self):
        if not self.__paused__:
            audio_process.pause()
            self.__paused__ = True
            return

        audio_process.unpause()
        self.__paused__ = False

    def run_audio(self):
        """
        Runs the audio.
        :return:
        """
        import threading  # Ensures threading is imported
        thread = threading.Thread(target=prepare_and_play, args=(self.link.text(),))
        thread.start()
        self.pause_play.setDisabled(False)
        self.skip_btn.setDisabled(False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--gui", help="Change if the app boots with or without GUI.", type=bool)

    try:
        args = parser.parse_args()
        if args.gui: user_interface()

        App = QApplication(sys.argv)
        window = GUIInterface(version)
        window.show()
        os._exit(App.exec())
    except Exception as e:
        print(
            f"{colorama.Fore.RED}An error has occurred, if this error continues to occur then open an issue in the "
            f"project github.\n\nError:\n{e}{colorama.Fore.RESET}")
        raise e
