# PyMedia
A Python based CLI and GUI media player. <br>

# How to install
### Binaries
1. Go to the latest version that best suits you.
2. Download the binary for your platform.
3. (Recommended) Move the binary to an appropriate folder.
4. Run the binary.

## Installation from source
### Windows
1. Install 7zip if you haven't already, the install file is actively available in the repo files.
2. Use 7zip to unzip `ffmpeg.7z`. This file is required for YT-DLP.
### Ubuntu
1. Open your terminal application with ctrl+alt+t.
2. Run `sudo apt install ffmpeg`
### Final
3. cd to project directory in the terminal.
4. Run `python3 -m pip install -r requirements.txt`
5. Run `python3 main.py`

# How to use
1. Get a link that YT-DLP supports (YouTube, TikTok, Soundcloud, etc.).
2. Run `main.py`
3. Choose if you want to use CLI with `--gui [true/false]` or `-g [true/false]`. You can also leave it blank to default to the GUI.
4. (1/2) CLI: Type in `[either start or play] [link or search term]`. (Example: `start https://youtu.be/dQw4w9WgXcQ`) <br>
   (2/2) GUI: Enter the link or search term into the text box and press "enter."

# Media controls
`play`, `start`: Loads an audio file from either local cache, a search term, or a supported link. <br>
`pause`: Pauses the current audio. <br>
`unpause`, `resume`, `unpause`, `continue`: Resume the current audio. <br>
`stop`: Stops playing the current soundtrack and moves on to the next one in queue. <br>
`exit`, `quit`, `leave`: Exits out of the media player.
