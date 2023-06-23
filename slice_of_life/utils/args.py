import argparse
import logging
from sys import stdout
from typing import List

from prettytable import PrettyTable
from video.video_file import VideoFile
from video.video_handler import VideoHandler

logger = logging.getLogger("slice_of_life")


def get_args():
    parser = argparse.ArgumentParser(
        description="Bulk rip audio from video files and split into small chunks."
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--series-dir", "-sd", help="Directory containing a series of episodes.")
    group.add_argument("--film-file", "-ff", help="Path to a single movie (1 film) file.")

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
    parser.add_argument("--season-number", required=False, help="The season number.")
    parser.add_argument("--album-art", help="The cover art to be embedded into the mp3 files.")

    return parser.parse_args()


def confirm_args(args, video_files: List[VideoFile]):
    while True:

        def print_settings():
            print("\nPlease check and confirm the following settings:")

            video_path_title = "Series Directory" if args.series_dir else "Film File"
            video_path_value = {args.series_dir} if args.series_dir else {args.film_file}

            table = PrettyTable(
                [
                    video_path_title,
                    "Output Directory",
                    "Album Art File",
                    "Artist Tag",
                    "Season Number",
                    "Segment Time",
                ]
            )

            table.add_row(
                [
                    video_path_value,
                    args.output_dir,
                    args.album_art,
                    args.artist_name,
                    args.season_number,
                    args.segment_time,
                ]
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
