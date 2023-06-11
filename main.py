import yt_dlp, threading, queue, colorama, os, time, argparse
import dearpygui.dearpygui as dpg

from pygame import mixer
mixer.init()

version = "1.2.1a"

"""
PyMedia from Weebed-Coder

This is an alpha version of PyMedia 1.2.0, do expect bugs and missing features.
"""

ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
    'outtmpl': "cache/%(title)s-%(id)s.%(ext)s",
    "paths": {'mp3':'cache', 'webm':'cache'},
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
""" 
# I understand this may be bad practice however for now I'll 
# keep it this way, simplifies the program. (aka am 
# too lazy to make a more convoluted solution)

global audio_process
global audio_queue
global audio_thread
audio_thread = False
audio_queue = queue.Queue()

def download_audio(user_input: str):
    """
    Downloads audio using yt_dlp library
    """
    print("Loading audio... this may take a moment.")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        if user_input.startswith("https://") == False and user_input.startswith("www.") == False:
            funny_dict = ydl.extract_info(f"ytsearch:{user_input}", download=False)['entries'][0]['id']
            user_input = f"https://youtube.com/watch?v={funny_dict}"
        elif user_input.startswith("http://"):
            print("Visiting http websites is unsafe, please refrain from visiting websites using http and not https as they're insecure.")

        info = ydl.extract_info(user_input, False)
        info = ydl.prepare_filename(info)

        print(info)

        if info.endswith(".webm"):
            info = info.replace(".webm", ".mp3")
        else:
            print(1)
            info = info.replace(info[-4:], ".mp3")
        
        print(info)

        if os.path.exists(info): # This is for caches (if any)
            return info
        ydl.download([user_input])

    return info

def start_audio():
    """
    Starts the audio thread, alongside handling removing items from queue.
    """

    global audio_thread
    while True:
        if audio_queue.empty():
            audio_thread = False
            return

        try:
            file = audio_queue.get()
        except Exception as exc:
            print(f"{colorama.Fore.RED}An error has occured:\n{exc}")
            pass

        global audio_process
        global paused
        #audio_wavobj = simpleaudio.WaveObject.from_wave_file(file[0])
        #audio_process = audio_wavobj.play()
        #audio_process.wait_done()
        tada = mixer.Sound(file[0])
        audio_process = tada.play()
        paused = False
        while audio_process.get_busy():
            time.sleep(0.1)
        if file[1]: os.remove(f"cache/{file}")

def attempt_clear():
    try:
        os.system("clear")
    except Exception as hi_neko: # This is not tested on a windows machine yet.
        os.system("cls")

def prepare_and_play(sender = False, user_input: str = None, del_cache: bool = True):
    """
    Prepares and plays the audio.
    """

    if sender:
        user_input = dpg.get_value("user_url")
    print(user_input)
    global audio_thread
    file_loc = download_audio(user_input) 
    audio_queue.put([file_loc, del_cache])
    if audio_thread == False:
        audio_thread = threading.Thread(target = start_audio, name = "PyMedia Audio Player")
        audio_thread.start()

def user_interface():
    """
    CLI user interface
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
            prepare_and_play(user_input = user_input[1], del_cache = del_cache)

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

def gui_interface():
    """
    GUI user interface
    """

    def change_pause_state():
        try:
            global audio_process
            global paused
            if paused == False: 
                audio_process.pause()
                paused = True
            else: 
                audio_process.unpause()
                paused = False
        except Exception as err:
            raise err
    
    # These are here to bypass some issues in DearPyGUI
    def move_along_now():
        audio_process.stop()
    def close_app(_sender, _data):
        os._exit(0)

    dpg.create_context()
    dpg.create_viewport()

    with dpg.window(label=f"PyMedia v{version}", tag="Primary Window"):
        # Note: Will need to add a bottom border for :sparkles:style:sparkles:
        with dpg.group(label="search_upper", horizontal=True):
            user_url = dpg.add_input_text(label="URL", tag="user_url")
            dpg.add_button(label="Confirm", callback=prepare_and_play)
            dpg.add_button(label="Exit", callback=close_app) # This is here due to a minor issue in DearPyGUI
            
        with dpg.group(label="main_middle"):
            pass # This section will contain locally installed files that can use
        with dpg.group(label="media_controls"):
            with dpg.group(label="playback_control", horizontal=True):
                dpg.add_button(label = "<") # Will need to round these out later when possible, also the button "<" will not work because there is no functionality for it yet
                dpg.add_button(label = "||", callback = change_pause_state)
                dpg.add_button(label = ">", callback = move_along_now)

    dpg.create_viewport(title=f'PyMedia v{version}', width=600, height=200)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--gui", help="Change if the app boots with or without GUI.", type=bool)
    while True:
        try:
            args = parser.parse_args()
            if args.gui: user_interface()
            gui_interface()
        except Exception as e:
            print(f"{colorama.Fore.RED}An error has occured, if this error continues to occur then open an issue in the project github. Restarting interface.\n\nError:\n{e}{colorama.Fore.RESET}")
