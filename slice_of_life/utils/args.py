import argparse


def get_args():
    parser = argparse.ArgumentParser(
        description='Bulk rip audio from video files and split into small chunks.')

    parser.add_argument('--video-dir', '-v', required=True,
                        help='The directory of videos to process.')

    parser.add_argument('--output-dir', '-o', default='/tmp',
                        help='The directory to place output audio files (default=/tmp).')

    parser.add_argument('--segment-time', '-s', default=180, type=int,
                        help='The length of the audio snippets in seconds (default=180).')

    parser.add_argument('--artist-name', required=True,
                        help='The artist name for the mp3 tags.')
    parser.add_argument('--album-name', required=True,
                        help='The album name for the mp3 tags.')
    parser.add_argument(
        '--album-art', help='The cover art to be embedded into the mp3 files.')

    return parser.parse_args()
