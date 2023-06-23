import logging
from signal import signal, SIGINT, SIGKILL
from sys import exit, stdout

from audio.audio_handler import AudioHandler
from video.video_handler import VideoHandler
from utils.args import get_args, confirm_args

logger = logging.getLogger("slice_of_life")
logging.basicConfig(level=logging.INFO)


def handler(signal_received, frame):
    exit(0)


def main():
    signal(SIGINT, handler)

    args = get_args()

    video_handler = VideoHandler()
    logger.info("Loading video metadata...")

    if args.video_dir:
        videos = video_handler.load_videos_in_directory(path=args.video_dir)
    else:
        videos = []
        video = video_handler.load_single_video(path=args.video_file)

        if video is None:
            logger.error(f"Incompatable video file: {args.video_file}")
            exit(1)

        videos = [video]

    video_handler.select_audio_tracks(videos)

    confirm_args(args=args, video_files=videos)

    num_videos = len(videos)
    num_text_video = "1 video" if num_videos == 1 else f"{num_videos} videos"

    logger.info("Extracting audio from %s...\n", num_text_video)

    audio_files = video_handler.bulk_extract_audio_from_videos(
        video_files=videos,
        destination_path=args.output_dir,
    )

    audio_handler = AudioHandler()
    num_audio = len(audio_files)
    num_text_audio = "1 file" if num_audio == 1 else f"{num_audio} files"

    logger.info(f"Slicing audio for {num_text_audio}...\n")

    episode_splits = audio_handler.bulk_split_audio_files(
        audio_files=audio_files,
        destination_path=args.output_dir,
        artist_name=args.artist_name,
    )

    logger.info("Tagging MP3 files...\n")

    audio_handler.bulk_tag_mp3s(
        split_files=episode_splits,
        artist_name=args.artist_name,
    )

    stdout.write("Done!\n")


if __name__ == "__main__":
    main()
