# PyMedia
A Python CLI/GUI based media player. <br>
If you have any suggestions on how to improve the code or repeatedly run in to an error then please open an issue. <br><br>
<b>This is the dev branch, do expect bugs and debug information being printed out.</b>

# Already known issues
1. ValueError upon trying to use any command directly after queue is empty. (Actual cause is not 100% known)
2. `exit` command doesn't exit fully when playing audio and will need to press ctrl+c in order to fully exit. (?)

# How to install
<h3>Binaries</h3>
1. Go to https://github.com/Weebed-Coder/PyMedia/releases/tag/v1.2.1a <br>
2. Download the binary for your appropriate platform <br>
3. (Optional) Move the binary to an appropriate folder <br>
4. Run the binary.

<h2>Installation from source</h2>
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
3. Choose if you want to use gui with `--nogui` or `-ng`. Or, leave it blank to default to gui. <br>
4. (1/2) If you're using CLI, type in "play " and then paste in your link. (Example: `start https://youtu.be/dQw4w9WgXcQ`) <br>
(2/2) If you're using GUI, type in your link in to the text box with "URL" next to it then press "confirm". <br>

Quick note: You can now use a search term such as "Rick Astley - Never Gonna Give You Up" on both CLI and GUI.

# Media controls
`play`: Loads an audio file from either local files or a youtube link. (Aliases: `start`) <br>
`pause`: Pauses the current audio. <br>
`unpause`: Resume the current audio. (Aliases: `resume`, `unpause`, `continue`) <br>
`stop`: Stops playing the current soundtrack and moves on to the next one in queue. <br>
`exit`: Exits out of the media player. (Aliases: `quit`, `leave`)
