from typing import List, Optional

from pymkv import MKVFile, MKVTrack


class VideoFile:
    title: str
    extension: str
    absolute_path: str
    audio_tracks: List[MKVTrack]
    selected_audio_track: Optional[int] = None
    is_mkv: bool = False

    def __init__(self, title: str, extension: str, absolute_path: str):
        self.title = title
        self.extension = extension
        self.absolute_path = absolute_path

        if extension == ".mkv":
            self.is_mkv = True
            self.load_mkv_meta()

    def get_subtitle_tracks(self, tracks: List[MKVTrack]) -> List[MKVTrack]:
        return list(filter(lambda track: track._track_type == "subtitles", tracks))

    def get_audio_tracks(self, tracks: List[MKVTrack]) -> List[MKVTrack]:
        return list(filter(lambda track: track._track_type == "audio", tracks))

    def load_mkv_meta(self):
        mkv = MKVFile(self.absolute_path)

        tracks = mkv.get_track()
        self.audio_tracks = self.get_audio_tracks(tracks)
