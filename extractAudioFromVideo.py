# https://superuser.com/questions/525210/splitting-an-audio-file-into-chunks-of-a-specified-length


# FFMPEG commands
# https://www.catswhocode.com/blog/19-ffmpeg-commands-for-all-needs


import subprocess
from pymediainfo import MediaInfo
import os
import shutil
from mutagen.easyid3 import EasyID3

artistName = None
audio_track = 0


os.chdir(r"/Users/danny/Documents/Python Scripts/extractAudio")

# extract audio from video files in the directory, then delete video
for f in os.listdir():
    file_name, file_ext = os.path.splitext(f)
    if file_ext == ".mkv":
        extract_audio(f, audio_track, file_name)
    else:
        None

# move all created audio to specified folder
for f in os.listdir():
    file_name, file_ext = os.path.splitext(f)
    if file_ext == ".mp3":
        moveExtractedAudio(f)
    else:
        None

os.chdir(r"/Users/danny/Documents/Python Scripts/extractAudio/extractedAudio")

for f in os.listdir():
    file_name, file_ext = os.path.splitext(f)
    if file_ext == ".mp3":
        split_audio(file_name)
        # delete full audio file
        os.remove(f)
    else:
        None

for f in os.listdir():
    file_name, file_ext = os.path.splitext(f)
    if file_ext == ".mp3":

        # strip numbers for album/artist name
        artistName = ''.join([i for i in file_name if not i.isdigit()])
        tagMP3(str(f), file_name)
    else:
        None
