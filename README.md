# PyMedia
A Python CLI/GUI based media player.
If you have any suggestions on how to improve the code or repeatedly run in to an error then please open an issue.
Also yes I am aware of the formatting issue with the readme, Github didn't wanna while I was editing this.

# Already known issues
1. Alsa shitting out a warning sometimes
2. Help command still unavailable (I forgot to add this during release of v1.1.0)

# How to install
<h3>Windows</h3>
1. Install 7zip if you haven't already, the install file is actively available in the repo files. <br>
2. Use 7zip to unzip `ffmpeg.7z`. This file is important as it is required in YT-DLP
<h3>Ubuntu</h3>
1. Open your terminal application with ctrl+alt+t <br>
2. Run `sudo apt install ffmpeg`
<h3>Final</h3>
(Follow the next steps only if you've downloaded/cloned the source code)<br>
3. cd to project directory <br>
4. Run `python3 -m pip install -r requirements.txt`

# How to use
1. Get a youtube or soundcloud link, or generally anything youtube-dlp supports.
2. Run `main.py`
3. Type in "play " and then paste in your link. (Example: `start https://youtu.be/dQw4w9WgXcQ`)

# Media controls
`play`: Loads an audio file from either local files or a youtube link. (Aliases: `start`) <br>
`pause`: Pauses the current audio. <br>
`unpause`: Resume the current audio. (Aliases: `resume`, `unpause`, `continue`) <br>
`stop`: Stops playing the current soundtrack and moves on to the next one in queue. <br>
`exit`: Exits out of the media player. (Aliases: `quit`, `leave`)

# To do
1. Allow for user to select between keeping downloaded files or deleting them.
2. Check if file is already downloaded.
3. Allow for GUI usage of app.
4. Compile app in to a `.exe`
