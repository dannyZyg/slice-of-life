import argparse
from video.video_handler import VideoHandler
from video.video_file import VideoFile


def get_args():
    parser = argparse.ArgumentParser(
        description="Bulk rip audio from video files and split into small chunks."
    )

    parser.add_argument("--video-dir", "-v", required=True, help="The directory of videos to process.")

    parser.add_argument(
        "--output-dir", "-o", default="/tmp", help="The directory to place output audio files (default=/tmp)."
    )

    parser.add_argument(
        "--segment-time",
        "-s",
        default=180,
        type=int,
        help="The length of the audio snippets in seconds (default=180).",
    )

    parser.add_argument("--artist-name", required=True, help="The artist name for the mp3 tags.")
    parser.add_argument("--album-name", required=True, help="The album name for the mp3 tags.")
    parser.add_argument("--album-art", help="The cover art to be embedded into the mp3 files.")

    return parser.parse_args()


def confirm_args(args, video_files: list[VideoFile]):

    while True:

        def print_settings():
            print(f"Video directory: {args.video_dir}")
            print(f"Output directory: {args.output_dir}")
            print(f"Album Art file: {args.album_art}")
            print(f"Artist tag: {args.artist_name}")
            print(f"Album tag: {args.album_name}")
            print(f"Segment time (seconds): {args.segment_time}")
            print("\n")
            print("To convert the following video files:")
            VideoHandler.list_videos(video_files)
            print("\n")

        print_settings()
        accept = input("Continue with these settings? yes/no > ")

        while accept.lower() not in ("yes", "y", "no", "n"):
            print_settings()
            accept = input("Continue with these settings? yes/no > ")

        if accept == "no" or accept == "n":
            exit(0)

        if accept == "yes" or accept == "y":
            break
