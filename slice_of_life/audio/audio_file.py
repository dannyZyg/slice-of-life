class AudioFile:
    title: str
    extension: str
    absolute_path: str

    def __init__(self, title: str, extension: str, absolute_path: str):
        self.title = title
        self.extension = extension
        self.absolute_path = absolute_path
