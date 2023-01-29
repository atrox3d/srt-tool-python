from pathlib import Path
from modules import logger

log = logger.get_logger(__name__)


def group_srts_by_path(srt_list: list[Path]) -> dict:
    """
    create a dictionary using srt paths as keys and a list of dicts(filename, size) as values
    :param srt_list:
    :return:
    """
    grouped = {}
    for srt in srt_list:
        if 'subs' in map(str.lower, srt.parts):
            filedict = dict(name=srt.name, size=srt.stat().st_size)
            #  create or update list of srt files
            if grouped.get(srt.parent, None):
                grouped[srt.parent].append(filedict)
            else:
                grouped[srt.parent] = [filedict]
        else:
            log.warning(f'SKIPPING: not under [Ss]ubs/ | {srt}')
    return grouped


def get_biggest(files_list: list) -> dict:
    """
    return biggest file in dict list
    :param files_list:
    :return:
    """
    bigger = None
    max_size = 0
    for file in files_list:
        if file['size'] > max_size:
            bigger = file
    return bigger


def get_destination_path(path, filename) -> Path:
    """
    create list of dicts containing source and dest path
    :param path:
    :param file:
    :return:
    """

    if path.name.lower() == 'subs':
        # rename srt files based on movie name
        # if .../moviename/subs/file.srt

        # set destination path to movie folder
        dest_path = path.parent

        # set destination filename to movie folder name + .srt
        dest_name = path.parent.parts[-1] + '.srt'

        # create destination srt path
        dest_path = dest_path / dest_name
    elif path.parent.name.lower() == 'subs':
        # rename srt files based on tvshow episode name
        # if .../seasonname/subs/episodename/file.srt

        # set destination path to tvshow folder
        dest_path = path.parent.parent

        # set destination filename to subtitle folder name + .srt
        dest_name = path.parts[-1] + '.srt'

        # create destination srt path
        dest_path = dest_path / dest_name
    else:
        # implement new structure if exception is arisen
        raise ValueError(f'NOT IMPLEMENTED | unknown path structure: {path / filename} ')
    return dest_path
