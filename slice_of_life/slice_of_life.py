import logging
import os
import webbrowser
from signal import SIGINT, signal
from sys import exit, stdout

from audio.audio_handler import AudioHandler
from utils.args import confirm_args, get_args
from video.video_handler import VideoHandler

logger = logging.getLogger("slice_of_life")
logging.basicConfig(level=logging.DEBUG)


def handler(signal_received, frame):
    exit(0)


def main():
    signal(SIGINT, handler)

    args = get_args()

    video_handler = VideoHandler()
    logger.info("Loading video metadata...")

    if args.series_dir:
        videos = video_handler.load_videos_in_directory(path=args.series_dir)
    else:
        videos = []
        video = video_handler.load_single_video(path=args.film_file)

        if video is None:
            logger.error(f"Incompatable video file: {args.film_file}")
            exit(1)

        videos = [video]

    video_handler.select_audio_tracks(videos)

    confirmed = confirm_args(args=args, video_files=videos)

    if not confirmed:
        exit(0)

    num_videos = len(videos)
    videos_text = "1 video" if num_videos == 1 else f"{num_videos} videos"
    logger.info(f"Extracting audio from {videos_text}...\n")

    audio_files = video_handler.bulk_extract_audio_from_videos(
        video_files=videos,
        destination_path=args.output_dir,
    )

    audio_handler = AudioHandler()
    num_audio = len(audio_files)
    audio_text = "1 file" if num_audio == 1 else f"{num_audio} files"
    logger.info(f"Slicing audio for {audio_text}...\n")

    split_path = os.path.join(args.output_dir, args.artist_name.replace(" ", "_").lower())
    logger.debug(f"split_path: {split_path}")

    episode_splits = audio_handler.bulk_split_audio_files(
        audio_files=audio_files,
        destination_path=split_path,
    )

    logger.info("Tagging MP3 files...\n")

    audio_handler.bulk_tag_mp3s(
        split_files=episode_splits,
        artist_name=args.artist_name,
        album_art=args.album_art,
        season_number=args.season_number,
    )

    stdout.write("Done!\n")

    # TODO check if mac or linux
    webbrowser.open(f"file://{split_path}")


if __name__ == "__main__":
    main()
