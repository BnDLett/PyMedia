import yt_dlp, threading, queue, colorama, os, simpleaudio

"""
PyMedia from Weebed-Coder
Version 1.1.0
"""

ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
    "paths": {'wav':'cache', 'webm':'cache'},
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192',
    }],
}

global audio_process

def download_audio(user_input: str):
    print("Loading audio... this may take a moment.")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(user_input, False)
        info = ydl.prepare_filename(info)

        if info.endswith(".webm"):
            info = info.replace(".webm", ".wav")
        else:
            info = info.replace(info[-4:], ".wav")
        
        print(os.listdir())
        if info in os.listdir(): # This is for caching
            print(os.listdir())
            return info
        ydl.download([user_input])

    return info

def start_audio():
    while True:
        if audio_queue.empty():
            audio_thread = False
            exit()

        try:
            file = audio_queue.get()
        except Exception as exc:
            print(f"{colorama.Fore.RED}An error has occured:\n{exc}")
            pass

        print(file)

        global audio_process
        audio_wavobj = simpleaudio.WaveObject.from_wave_file(file[0])
        audio_process = audio_wavobj.play()
        audio_process.wait_done()
        if file[1]: os.remove(file)

def attempt_clear():
    try:
        os.system("clear")
    except Exception as hi_neko: # This is not tested on a windows machine yet.
        os.system("cls")

def user_interface():
    global audio_queue
    global audio_thread
    audio_queue = queue.Queue()
    audio_thread = False

    while True:
        clear = False
        del_cache = False
        user_input = input("Please enter a command. Use help for a list of commands.\n> ").split(" ")

        try:
            if user_input[2] in ["-nocache", "-n"]:
                del_cache = True
        except:
            pass

        if user_input[0].lower() in ["help", "-?"]:
            print("Help list is not yet ready.")

        elif user_input[0].lower() in ["play", "start", "queue"]:
            file_loc = download_audio(user_input[1]) 
            audio_queue.put([file_loc, del_cache])
            if audio_thread == False:
                audio_thread = threading.Thread(target = start_audio, name = "PyMedia Audio Player")
                audio_thread.start()

        elif user_input[0].lower() in ["pause"]:
            audio_process.pause()

        elif user_input[0].lower() in ["continue", "resume", "unpause"]:
            audio_process.resume()

        elif user_input[0].lower() in ["stop"]:
            audio_process.stop()
        
        elif user_input[0].lower() in ["quit", "exit", "leave"]:
            exit()
        
        if clear:
            attempt_clear()

if __name__ == "__main__":
    while True:
        try:
            user_interface()
        except Exception as e:
            print(f"{colorama.Fore.RED}An error has occured, if this error continues to occur then open an issue in the project github. Restarting interface.\n\nError:\n{e}{colorama.Fore.RESET}")
