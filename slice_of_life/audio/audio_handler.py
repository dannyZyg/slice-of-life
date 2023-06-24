import logging
import os
import subprocess
from typing import List

from audio.audio_file import AudioFile
from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC, ID3

logger = logging.getLogger(__name__)


class AudioHandler:
    """A class responsible for handling and processing multiple audio files."""

    def bulk_split_audio_files(
        self, audio_files: List[AudioFile], destination_path: str
    ) -> List[List[AudioFile]]:
        episodes = []

        if not os.path.exists(destination_path):
            os.mkdir(destination_path)

        # Deal with each episode
        for audio_file in audio_files:
            episode_sub_path = os.path.join(destination_path, audio_file.title)

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

            os.remove(audio_file.absolute_path)

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

    def bulk_tag_mp3s(
        self,
        split_files: List[List[AudioFile]],
        artist_name: str,
        album_art: str | None = None,
        season_number: str | None = None,
    ) -> None:
        season_label = f" Season {season_number}" if season_number else ""
        logger.debug(f"Season Label: {season_label}")

        # Go through each episode
        for index, episode in enumerate(split_files):
            episode_label = f" Episode {index + 1}" if len(split_files) > 1 else ""
            logger.debug(f"Episode Label: {episode_label}")
            album_name = f"{artist_name}{season_label}{episode_label}"
            logger.debug(f"Album Name: {album_name}")

            # Tag each episode and attach album art
            for audio_file in episode:
                self.tag_mp3(
                    audio_file=audio_file,
                    artist_name=artist_name,
                    album_name=album_name,
                )

                if album_art:
                    self.add_album_art(audio_file.absolute_path, album_art)

    def tag_mp3(self, audio_file: AudioFile, artist_name: str, album_name: str) -> None:
        """Tags mp3 file with the supplied metadata."""
        audio = EasyID3(audio_file.absolute_path)
        audio["title"] = audio_file.title
        audio["artist"] = artist_name
        audio["album"] = album_name
        audio.save()

    def add_album_art(self, audio_path: str, album_art_path: str) -> None:
        audio = ID3(audio_path)

        # Create an APIC tag for album art
        apic = APIC()
        apic.type = 3  # Front cover image
        apic.mime = "image/jpeg"
        apic.desc = "Cover"
        with open(album_art_path, "rb") as f:
            apic.data = f.read()

        audio.add(apic)
        audio.save()
