from audio.audio_handler import AudioHandler
from video.video_handler import VideoHandler
from signal import signal, SIGINT
from sys import exit
from utils.args import get_args


def handler(signal_received, frame):
    exit(0)


if __name__ == '__main__':

    signal(SIGINT, handler)

    args = get_args()

    video_dir = args.video_dir
    output_dir = args.output_dir
    album_art = args.album_art
    artist_name = args.artist_name
    album_name = args.album_name
    segment_time = args.segment_time

    print(f'Video directory: {video_dir}')
    print(f'Output directory: {output_dir}')
    print(f'Album Art file: {album_art}')
    print(f'Artist tag: {artist_name}')
    print(f'Album tag: {album_name}')
    print(f'Segment time (seconds): {segment_time}')

    video_handler = VideoHandler()
    audio_handler = AudioHandler()

    videos = video_handler.load_videos_in_directory(path=video_dir)

    num_videos = len(videos)
    num_text_video = '1 video' if num_videos == 1 else f'{num_videos} videos'

    print(f'Extracting audio from {num_text_video}...\n')
    print('\n')

    audio_files = video_handler.bulk_extract_audio_from_videos(
        video_files=videos,
        destination_path='/tmp',
    )

    num_audio = len(audio_files)
    num_text_audio = '1 audio file' if num_audio == 1 else f'{num_audio} files'

    print(f'Slicing audio for {num_text_video}...\n')

    split_audio_files = audio_handler.bulk_split_audio_files(
        audio_files=audio_files,
        destination_path='/tmp'
    )

    print('Tagging MP3 files...\n')

    audio_handler.bulk_tag_mp3s(
        audio_files=split_audio_files,
        artist_name='hibana',
        album_name='hibana',
    )

    print('Done!')
