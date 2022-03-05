import subprocess
from pymediainfo import MediaInfo
import os
import shutil
from mutagen.easyid3 import EasyID3


class AudioHandler:
    """ A class responsible for handling and processing multiple audio files. """

    # # function to move extracted audio to dedicated folder
    # def move_extracted_audio(file: str, destination_folder: str):
    #     """ Moves a file to a destination folder. """
    #     shutil.move(file, f'{destination_folder}/{file}')

    def split_audio(self, audio_file: str, segment_time: int = 180) -> None:
        """ Splits an audio track at intervals determined by the supplied segment time in seconds. """
        cmd = f'ffmpeg -i {audio_file} -f segment -segment_time {segment_time} -c copy {audio_file}%03d.mp3'
        subprocess.call(cmd, shell=True)

    def tag_mp3(file_name: str, artist_name: str, title: str, album: str) -> None:
        """ Tags mp3 file with the supplied metadata. """
        audio = EasyID3(file_name)
        audio['title'] = file_name
        audio['artist'] = artist_name
        audio['album'] = artist_name
        audio.save()
