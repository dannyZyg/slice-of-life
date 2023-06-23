from typing import List
import os
import subprocess

from mutagen.easyid3 import EasyID3

from audio.audio_file import AudioFile


class AudioHandler:
    """A class responsible for handling and processing multiple audio files."""

    def bulk_split_audio_files(
        self, audio_files: List[AudioFile], destination_path: str, artist_name: str
    ) -> List[List[AudioFile]]:
        episodes = []
        split_path = os.path.join(destination_path, artist_name.replace(" ", "_").lower())

        if not os.path.exists(split_path):
            os.mkdir(split_path)

        # Deal with each episode
        for audio_file in audio_files:
            episode_sub_path = os.path.join(split_path, audio_file.title)

            if not os.path.exists(episode_sub_path):
                os.mkdir(episode_sub_path)

            did_split = self.split_audio(audio_file, output_dir=episode_sub_path)
            if did_split:
                split_audio_files = []

                # Add episode splits to list
                for f in os.listdir(episode_sub_path):
                    file_name, file_ext = os.path.splitext(f)
                    split_audio_files.append(
                        AudioFile(
                            title=file_name,
                            extension=file_ext,
                            absolute_path=f"{episode_sub_path}/{f}",
                        )
                    )

                episodes.append(split_audio_files)

        return episodes

    def split_audio(self, audio_file: AudioFile, segment_time: int = 180, output_dir: str = "/tmp") -> bool:
        """Splits an audio track at intervals determined by the supplied segment time in seconds."""

        command = [
            "ffmpeg",
            "-y",
            "-i",
            audio_file.absolute_path,
            "-f",
            "segment",
            "-segment_time",
            f"{segment_time}",
            "-c",
            "copy",
            f"{output_dir}/{audio_file.title}_%03d.mp3",
        ]

        if subprocess.run(command).returncode != 0:
            print("There was an error splitting the audio file.")

        return True

    def bulk_tag_mp3s(self, split_files: List[List[AudioFile]], artist_name: str) -> None:
        for episode in split_files:
            for index, audio_file in enumerate(episode):
                self.tag_mp3(
                    audio_file=audio_file,
                    artist_name=artist_name,
                    album_name=f"{artist_name} Episode {index + 1}",
                )

    def tag_mp3(self, audio_file: AudioFile, artist_name: str, album_name: str) -> None:
        """Tags mp3 file with the supplied metadata."""
        audio = EasyID3(audio_file.absolute_path)
        audio["title"] = audio_file.title
        audio["artist"] = artist_name
        audio["album"] = album_name
        audio.save()
