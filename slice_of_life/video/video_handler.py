import logging
import os
from time import sleep
from typing import List

from audio.audio_file import AudioFile
from ffmpeg_progress_yield import FfmpegProgress
from prettytable import PrettyTable
from tqdm import tqdm
from video.video_file import VideoFile

logger = logging.getLogger(__name__)


class VideoHandler:
    """A class responsible for handling and processing multiple video files."""

    def validate_is_supported_video_file(self, file_extension: str) -> bool:
        supported_file_extensions = [".mkv", ".mp4"]
        return file_extension in supported_file_extensions

    @staticmethod
    def list_videos(videos: List[VideoFile]) -> None:
        table = PrettyTable(
            [
                "Video Title",
                "Selected Audio Track",
            ]
        )

        for video in videos:
            table.add_row(
                [
                    f"{video.title}{video.extension}",
                    str(video.audio_tracks[video.selected_audio_track].language),
                ]
            )

        print(table)

    def load_videos_in_directory(self, path: str) -> List[VideoFile]:
        videos = []

        for file in tqdm(os.listdir(path)):
            file_title, file_ext = os.path.splitext(file)

            is_supported_file_type = self.validate_is_supported_video_file(file_ext)

            if is_supported_file_type:
                videos.append(VideoFile(title=file_title, extension=file_ext, absolute_path=f"{path}/{file}"))

        return sorted(videos, key=lambda v: v.title)

    def load_single_video(self, path: str) -> None | VideoFile:
        file_title, file_ext = os.path.splitext(path)

        print(file_ext)
        is_supported_file_type = self.validate_is_supported_video_file(file_ext)

        if not is_supported_file_type:
            return None

        return VideoFile(title=file_title, extension=file_ext, absolute_path=path)

    def select_audio_tracks(self, videos):
        first_chosen_audio_track = None

        os.system("clear")
        table = PrettyTable(["Track ID", "Audio Track"])

        for video in videos:
            while video.selected_audio_track is None:
                if video.is_mkv:
                    valid_track_ids = list(range(0, len(video.audio_tracks)))

                    # Choose track 1 if that is all that is available
                    if len(valid_track_ids) == 1:
                        video.selected_audio_track = valid_track_ids[0]
                        break

                    # Attempt to find the same track as was selected for video 1 in the subsequent videos.
                    if first_chosen_audio_track:
                        matching_tracks = [
                            i
                            for i, t in enumerate(video.audio_tracks)
                            if t._track_id == first_chosen_audio_track._track_id
                            and t.language == first_chosen_audio_track.language
                        ]

                        if matching_tracks:
                            logger.debug(f"Audio track chosen for {video.title}")
                            logger.debug(
                                f"Using the audio track selected for video 1 as it exists in {video.title}"
                            )
                            video.selected_audio_track = matching_tracks[0]
                            break

                    for index, track in enumerate(video.audio_tracks):
                        table.add_row([index, track.language])

                    # Output options for this video
                    print(f"\nSelect audio track for {video.title}")
                    print("The video file contains the following audio tracks:")
                    print(table)

                    selected_track = input("\nPlease choose an audio track id: ")

                    try:
                        selected_track_as_int = int(selected_track)
                        if selected_track_as_int in valid_track_ids:
                            video.selected_audio_track = selected_track_as_int
                            first_chosen_audio_track = video.audio_tracks[selected_track_as_int]
                            break

                        else:
                            print(f"Invalid input! Possible values are: {valid_track_ids}")
                            sleep(1)
                    except ValueError:
                        print(f"Invalid input! Possible values are: {valid_track_ids}")
                        sleep(1)
                else:
                    video.selected_audio_track = 0

    def bulk_extract_audio_from_videos(
        self,
        video_files: List[VideoFile],
        destination_path: str,
    ) -> List[AudioFile]:
        audio_files = []
        file_ext = ".mp3"

        for video_file in tqdm(video_files, total=len(video_files)):
            output_file = f"{video_file.title}{file_ext}"
            output_full_path = f"{destination_path}/{output_file}"

            did_extract = self.extract_audio(
                video_file=video_file,
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

    def extract_audio(self, video_file: VideoFile, output_file: str) -> bool:
        """Extracts an audio track from a video file using ffmpeg."""

        if os.path.isfile(video_file.absolute_path):
            command = [
                "ffmpeg",
                "-y",
                "-i",
                f"{video_file.absolute_path}",
                "-vn",
                "-ar",
                "44100",
                "-ac",
                "2",
                "-ab",
                "192k",
                "-f",
                "mp3",
                "-map",
                "0:v:0",
                "-map",
                f"0:a:{video_file.selected_audio_track}",
                f"{output_file}",
            ]
            ff = FfmpegProgress(command)

            with tqdm(total=100, position=1, desc=video_file.title) as pbar:
                for progress in ff.run_command_with_progress():
                    pbar.update(progress - pbar.n)

            return True

        else:
            print(f"File {video_file} does not exist.")
            return False
