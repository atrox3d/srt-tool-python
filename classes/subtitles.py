from pathlib import Path

from classes.subtitle import Subtitle
from modules import logger

log = logger.get_logger(__name__)


class SubtitleList(list):
    def __init__(self, iterable=None):
        super().__init__(self._validate_and_initialize(item) for item in iterable or [])

    def __setitem__(self, index, item):
        super().__setitem__(index, self._validate_and_initialize(item))

    def insert(self, index, item):
        super().insert(index, self._validate_and_initialize(item))

    def append(self, item):
        super().append(self._validate_and_initialize(item))

    def extend(self, other):
        if isinstance(other, type(self)):
            super().extend(other)
        else:
            super().extend(self._validate_and_initialize(item) for item in other)

    @staticmethod
    def _validate_and_initialize(value):
        if isinstance(value, (str, Path)):
            return Subtitle(value)
        elif isinstance(value, Subtitle):
            return value
        raise TypeError(
            f"string or Path value expected, got {type(value).__name__}"
        )

    @classmethod
    def from_path(cls, path, pattern='**/*.srt'):
        if isinstance(path, str):
            path = Path(path)
        return cls(path.glob(pattern))

    # @staticmethod
    def to_dict(self) -> dict:
        """
        create a dictionary using srt paths as keys and a list of dicts(filename, size) as values
        :param subs_list:
        :return:
        """
        grouped = {}
        for sub in self:
            if 'subs' in str(sub.parent).lower():
                #  create or update list of srt files
                if grouped.get(sub.parent, None):
                    grouped[sub.parent].append(sub)
                else:
                    grouped[sub.parent] = [sub]
            else:
                log.warning(f'SKIPPING: not under [Ss]ubs/ | {sub.path}')
        return grouped

    @staticmethod
    def get_biggest(subs_list: list):
        """
        return biggest file in dict list
        :param subs_list:
        :return:
        """
        bigger = None
        max_size = 0
        for sub in subs_list:
            if sub.size > max_size:
                bigger = sub
        return bigger


if __name__ == '__main__':
    sub = Subtitle("../2_English.srt")
    print(f'{sub.path=}')
    print(f'{sub.parent=}')
    print(f'{sub.name=}')
    print(f'{sub.size=}')

    srts = list(Path('..').glob('**/*.srt'))
    subs = SubtitleList(srts)
    print(f'{subs=}')
    subs.append(Subtitle('../2_English.srt'))
    subs.append(Subtitle('../2_English.srt'))
    print(f'{subs=}')
    subs = SubtitleList.from_path('..')
    print(f'{subs=}')
    group = subs.to_dict()
    print(f'{group=}')
