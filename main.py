import sys
import logging
from pathlib import Path
import shutil
from typing import Dict, List


def get_logger(name):
    """
    get standard logger to stdout, level INFO
    :param name:
    :return:
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(module)s | %(levelname)-" + str(len("CRITICAL")) + "s | %(message)s",
        datefmt='%Y/%m/%d %H:%M:%S',
        stream=sys.stdout
    )
    logger = logging.getLogger(name)
    return logger


def get_root(path=None) -> Path:
    """
    get root path to begin search
    :param path:
    :return:
    """
    if not path:
        # get path from command line argument or work from cwd
        try:
            root_path = sys.argv[1]
        except IndexError:
            root_path = '.'
    else:
        root_path = path

        # set root path
        root_path = Path(root_path).absolute()
        log.info(f'{root_path=}')
        return root_path


def get_srtfiles(root_path, pattern='**/*.srt') -> list[Path]:
    """
    search .srt files under root path and return them in a list of paths
    :param root_path:
    :param pattern:
    :return:
    """
    # get list of all .srt files
    srt_files = list(root_path.glob(pattern))
    return srt_files


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


def get_destination_path(path, file) -> Path:
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
        raise ValueError(f'NOT IMPLEMENTED | unknown path structure: {path / file}')
    return dest_path


if __name__ == '__main__':
    log = get_logger(__name__)
    # log.setLevel('DEBUG')
    # push command line argument for testing in pycharm
    # sys.argv.append('d:/downloads')
    root = get_root('d:/downloads')

    srts = get_srtfiles(root)
    log.debug(f'{srts=}')

    groups = group_srts_by_path(srts)
    log.debug(f'{groups=}')

    for path, files in groups.items():
        biggest = get_biggest(files)
        filename, size = biggest.values()
        groups[path] = filename
    log.debug(f'{groups=}')

    parameters = []
    parameter = {}
    # loop through flattened groups of srt files
    for path, file in groups.items():
        # create source path for copy
        source_path = path / file
        destination_path = get_destination_path(path, file)
        parameter = dict(src=source_path, dst=destination_path)
        parameters.append(parameter)

    for parameter in parameters:
        log.debug(f'{parameter=}')
        src, dst = parameter.values()
        log.info(f'COPY | SRC | {src}')
        log.info(f'COPY | DST | {dst}')
        shutil.copy(src, dst)
