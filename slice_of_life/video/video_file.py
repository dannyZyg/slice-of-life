import subprocess
from pymediainfo import MediaInfo
import os
import shutil
from mutagen.easyid3 import EasyID3


class VideoFile:

    title: str
    extension: str
    absolute_path: str
    audio_track: int
    subtitle_track: int

    def __init__(self, title: str, extension: str, absolute_path: str):
        self.title = title
        self.extension = extension
        self.absolute_path = absolute_path
