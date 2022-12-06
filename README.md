# PyMedia
A Python CLI based media player.

# Already known issues
1. "Resume" doesn't work while playing an audio, meanwhile alternative does.
2. Can not load local files.
3. Audio thread potentionally not closing when it is supposed to.
4. Audio not starting after queue is finished.

# How to use
1. Find a local or youtube audio file.
2. Paste in the location. (ex. `start C:audios/media.mp3`; `start https://www.youtube.com/watch?v=dQw4w9WgXcQ`)
3. Enjoy

# Media controls
`start`: Loads an audio file from either local files or a youtube link. <br>
`pause`: Pauses the current audio. <br>
`unpause`: Resume the current audio. (Alias: `Resume`) <br>
`exit`: Exits out of the media player. <br>
`current`: Displays current information of the currently playing audio. Shows current position in the audio and current volume.

# To do
1. Check if the audio file already exists in the file system, if it does then play that.
2. Squash bugs.
