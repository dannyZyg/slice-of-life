# from moviepy.editor import *
# audioclip = AudioFileClip("kimisui_movie.mkv")

# to split a clip (segment_time in seconds)
# $ ffmpeg -i test.mp3 -f segment -segment_time 180 -c copy out%03d.mp3
# https://superuser.com/questions/525210/splitting-an-audio-file-into-chunks-of-a-specified-length


# FFMPEG commands
# https://www.catswhocode.com/blog/19-ffmpeg-commands-for-all-needs


import subprocess
from pymediainfo import MediaInfo
import os
import shutil
from mutagen.easyid3 import EasyID3

artistName = None

# function to move extracted audio to dedicated folder
def moveExtractedAudio(file):
    shutil.move("{file}".format(file=file), "extractedAudio/{file}".format(file=file))

# extract audio from video, convert to mp3
def extract_audio(video, output):
    command = "ffmpeg -i {video} -vn -ar 44100 -ac 2 -ab 192k -f mp3 {output}.mp3".format(video=video, output=output)
    subprocess.call(command, shell=True)

# chop audio into segments
def split_audio(audio):
    command = "ffmpeg -i {audio}.mp3 -f segment -segment_time 180 -c copy {audio}%03d.mp3".format(audio=audio) 
    subprocess.call(command, shell=True)


os.chdir(r"/Users/danny/Documents/Python Scripts/extractAudio")

# extract audio from video files in the directory, then delete video
for f in os.listdir():
    file_name, file_ext = os.path.splitext(f)
    if file_ext == ".mkv":
        extract_audio(f, file_name)  
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

# create mp3 tags when called
def tagMP3(file, file_name):
    audio = EasyID3(file)
    audio['title'] = file_name
    audio['artist'] = artistName
    audio['album'] = artistName
    audio.save()


for f in os.listdir():
    file_name, file_ext = os.path.splitext(f)
    if file_ext == ".mp3":
        split_audio(file_name)
        # strip numbers for album/artist name
        os.remove(f)
    else:
        None

for f in os.listdir():
    file_name, file_ext = os.path.splitext(f)
    if file_ext == ".mp3":
        artistName = ''.join([i for i in file_name if not i.isdigit()])
        tagMP3(str(f), file_name)
    else:
        None




