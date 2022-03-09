from audio.audio_handler import AudioHandler
from video.video_handler import VideoHandler
from signal import signal, SIGINT
from sys import exit
from utils.args import get_args, confirm_args


def handler(signal_received, frame):
    exit(0)


if __name__ == "__main__":

    signal(SIGINT, handler)

    args = get_args()

    album_art = args.album_art
    segment_time = args.segment_time

    video_handler = VideoHandler()
    print("--------------------------------------------------")
    print("Loading video metadata...")
    print("--------------------------------------------------")
    videos = video_handler.load_videos_in_directory(path=args.video_dir)

    video_handler.select_audio_tracks(videos)

    confirm_args(args=args, video_files=videos)

    num_videos = len(videos)
    num_text_video = "1 video" if num_videos == 1 else f"{num_videos} videos"

    print(f"Extracting audio from {num_text_video}...\n")
    print("\n")

    audio_files = video_handler.bulk_extract_audio_from_videos(
        video_files=videos,
        destination_path=args.output_dir,
    )

    audio_handler = AudioHandler()
    num_audio = len(audio_files)
    num_text_audio = "1 file" if num_audio == 1 else f"{num_audio} files"

    print(f"Slicing audio for {num_text_audio}...\n")

    split_audio_files = audio_handler.bulk_split_audio_files(
        audio_files=audio_files,
        destination_path=args.output_dir,
    )

    print("Tagging MP3 files...\n")

    audio_handler.bulk_tag_mp3s(
        audio_files=split_audio_files,
        artist_name=args.artist_name,
        album_name=args.album_name,
    )

    print("Done!")
