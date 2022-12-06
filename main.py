import threading, yt_dlp, os
from pygame import mixer

mixer.init()

def downloadAudio(userInp):
    print("Loading audio... this may take a moment.")

    if "https://" or "www" in userInp:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(userInp, False)
            info = ydl.prepare_filename(info)
            ydl.download([userInp])

    info = info.replace("webm", "mp3")
    return info

def startAudio(audioLoc:str="../expAudio.mp3"):
    mixer.music.load(audioLoc)
    mixer.music.play()
    os.system("cls")
    print("Enjoy your music!")

    while True:
        clear = True
        try:
            userInp = input()
            if "stop" in userInp.lower():
                mixer.music.stop()
            elif "pause" in userInp.lower():
                mixer.music.pause()
            elif "unpause" in userInp.lower() or "resume" in userInp.lower():
                mixer.music.unpause()
            elif "start" in userInp.lower():
                userInp = userInp.replace("start", "").strip()    
                mixer.music.queue(downloadAudio(userInp))
            elif "current" in userInp.lower():
                os.system('cls')
                print(f"Position: {mixer.music.get_pos()/1000} seconds\nVolume: {mixer.music.get_volume()}")
                clear = False
            elif "exit" in userInp.lower():
                exit()
        finally:
            if clear == True:
                os.system('cls')

ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
    "paths": {'mp3':'cache', 'webm':'cache'},
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

while True:
    userInp = input()
    if userInp.startswith("start"):
        userInp = userInp.replace("start", "").strip()
        thread = threading.Thread(target=startAudio, name="pyAudioPlayer", args=(downloadAudio(userInp),))
        thread.start()
        while True:
            if thread.is_alive:
                continue
            else:
                break
            
