from pathlib import Path

from modules import logger

log = logger.get_logger(__name__)


class Subtitle:

    def __init__(self, path):
        path = Path(path).resolve()
        self.path = path
        # path, name = srt_path.parts[:-1], srt_path.parts[-1]
        self.parent = path.parent
        self.name = path.name
        self.size = path.stat().st_size

    @classmethod
    def get_subtitles(cls, srt_list):
        return [cls(srt) for srt in srt_list]

    @staticmethod
    def group_by_path(subs_list) -> dict:
        """
        create a dictionary using srt paths as keys and a list of dicts(filename, size) as values
        :param subs_list:
        :return:
        """
        grouped = {}
        for sub in subs_list:
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
    print(sub.path)
    print(sub.parent)
    print(sub.name)
    print(sub.size)

