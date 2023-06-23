from sys import stdout
from typing import List
import logging
import argparse

from prettytable import PrettyTable

from video.video_handler import VideoHandler
from video.video_file import VideoFile

logger = logging.getLogger("slice_of_life")


def get_args():
    parser = argparse.ArgumentParser(
        description="Bulk rip audio from video files and split into small chunks."
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--video-dir", "-vd", help="Directory containing videos. Intended for episodes.")
    group.add_argument("--video-file", "-vf", help="Path to a single video file. Intented for films.")

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
    parser.add_argument("--album-art", help="The cover art to be embedded into the mp3 files.")

    return parser.parse_args()


def confirm_args(args, video_files: List[VideoFile]):
    while True:

        def print_settings():
            print("\nPlease check and confirm the following settings:")

            video_path_title = "Video Directory" if args.video_dir else "Video File"
            video_path_value = {args.video_dir} if args.video_dir else {args.video_file}

            table = PrettyTable(
                [video_path_title, "Output Directory", "Album Art File", "Artist Tag", "Segment Time"]
            )

            table.add_row(
                [video_path_value, args.output_dir, args.album_art, args.artist_name, args.segment_time]
            )

            print(table)

            print("\nTo convert the following video files:")
            VideoHandler.list_videos(video_files)

        print_settings()
        accept = input("Continue with these settings? yes/no > \n")

        while accept.lower() not in ("yes", "y", "no", "n"):
            print_settings()
            accept = input("\nContinue with these settings? yes/no > \n")

        if accept == "no" or accept == "n":
            exit(0)

        if accept == "yes" or accept == "y":
            stdout.flush()
            break
