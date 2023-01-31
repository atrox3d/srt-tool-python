from pathlib import Path


class Subtitle:

    def __init__(self, path):
        path = Path(path).resolve()
        self.path = path
        # path, name = srt_path.parts[:-1], srt_path.parts[-1]
        self.parent = path.parent
        self.name = path.name
        self.size = path.stat().st_size

    def __str__(self):
        return str(self.path.as_posix())

    def __repr__(self):
        return f'{self.__class__.__name__}({str(self)!r})'
