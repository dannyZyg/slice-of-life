import subprocess
from alive_progress import alive_bar
import time
from tqdm import tqdm
from ffmpeg_progress_yield import FfmpegProgress
from pymediainfo import MediaInfo
import os
import shutil
from mutagen.easyid3 import EasyID3
from .video_file import VideoFile
from audio.audio_file import AudioFile


class VideoHandler:
    """ A class responsible for handling and processing multiple video files. """

    def validate_is_supported_video_file(self, file_extension: str) -> bool:
        supported_file_extensions = ['.mkv', '.mp4']
        return file_extension in supported_file_extensions

    def load_videos_in_directory(self, path: str) -> list[VideoFile]:

        videos = []

        for file in os.listdir(path):
            file_title, file_ext = os.path.splitext(file)

            is_supported_file_type = self.validate_is_supported_video_file(file_ext)

            if is_supported_file_type:
                videos.append(
                    VideoFile(
                        title=file_title,
                        extension=file_ext,
                        absolute_path=f'{path}/{file}'
                    )
                )
        return videos

    def bulk_extract_audio_from_videos(self, video_files: list[VideoFile], destination_path: str) -> list[AudioFile]:

        audio_files = []
        file_ext = '.mp3'

        for video_file in video_files:

            output_file = f'{video_file.title}{file_ext}'
            output_full_path = f'{destination_path}/{output_file}'

            did_extract = self.extract_audio(
                video_file=video_file,
                audio_track=0,
                output_file=output_full_path,
            )

            if did_extract:
                audio_files.append(
                    AudioFile(
                        title=video_file.title,
                        extension=file_ext,
                        absolute_path=output_full_path,
                    )
                )

        return audio_files

    def extract_audio(self, video_file: VideoFile, audio_track: int, output_file: str) -> bool:
        """ Extracts an audio track from a video file using ffmpeg. """

        if os.path.isfile(video_file.absolute_path):

            command = [
                'ffmpeg',
                '-y',
                '-i', f'{video_file.absolute_path}',
                '-vn',
                '-ar', '44100',
                '-ac', '2',
                '-ab', '192k',
                '-f', 'mp3',
                '-map', '0:v:0',
                '-map', f'0:a:{audio_track}',
                f'{output_file}',
            ]
            ff = FfmpegProgress(command)

            with tqdm(total=100, position=1, desc=video_file.title) as pbar:
                for progress in ff.run_command_with_progress():
                    pbar.update(progress - pbar.n)

            return True

        else:
            print(f'File {video_file} does not exist.')
            return False
