from audio.audio_file import AudioFile
from ffmpeg_progress_yield import FfmpegProgress
import os
from mutagen.easyid3 import EasyID3


class AudioHandler:
    """ A class responsible for handling and processing multiple audio files. """

    def bulk_split_audio_files(self, audio_files: list[AudioFile], destination_path: str) -> list[AudioFile]:

        split_audio_files = []
        split_path = os.path.join(destination_path, 'tmp_split_audio__')

        if not os.path.exists(split_path):
            os.mkdir(split_path)

        for audio_file in audio_files:
            episode_sub_path = os.path.join(split_path, f'episode__{audio_file.title}')

            if not os.path.exists(episode_sub_path):
                os.mkdir(episode_sub_path)

            did_split = self.split_audio(audio_file, output_dir=episode_sub_path)
            if did_split:
                for f in os.listdir(episode_sub_path):
                    file_name, file_ext = os.path.splitext(f)
                    split_audio_files.append(
                        AudioFile(
                            title=file_name,
                            extension=file_ext,
                            absolute_path=f'{episode_sub_path}/{f}',
                        )
                    )

        return split_audio_files

    def split_audio(self, audio_file: AudioFile, segment_time: int = 180, output_dir: str = '/tmp') -> bool:
        """ Splits an audio track at intervals determined by the supplied segment time in seconds. """
        command = [
            'ffmpeg',
            '-y',
            '-i', audio_file.absolute_path,
            '-f', 'segment',
            '-segment_time', f'{segment_time}',
            '-c', 'copy',
            f'{output_dir}/{audio_file.title}%03d.mp3',
        ]

        ff = FfmpegProgress(command)
        ff.run_command_with_progress()

        return True

    def bulk_tag_mp3s(self, audio_files: list[AudioFile], artist_name: str, album_name: str) -> None:
        for audio_file in audio_files:
            self.tag_mp3(
                audio_file=audio_file,
                artist_name=artist_name,
                album_name=album_name,
            )

    def tag_mp3(self, audio_file: AudioFile, artist_name: str, album_name: str) -> None:
        """ Tags mp3 file with the supplied metadata. """
        audio = EasyID3(audio_file.absolute_path)
        audio['title'] = audio_file.title
        audio['artist'] = artist_name
        audio['album'] = album_name
        audio.save()
