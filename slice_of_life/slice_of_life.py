from video.video_handler import VideoHandler
import os
from signal import signal, SIGINT
from sys import exit


def handler(signal_received, frame):
    exit(0)


if __name__ == '__main__':

    signal(SIGINT, handler)

    while True:
        video_handler = VideoHandler()

        current_dir = os.getcwd()

        videos = video_handler.load_videos_in_directory(path=current_dir)

        num_videos = len(videos)
        num_text = '1 video' if num_videos == 1 else f'{num_videos} videos'

        print(f'Extracting audio from {num_text}...')
        audio_files = video_handler.bulk_extract_audio_from_videos(
            video_files=videos,
            destination_path='/tmp',
        )
