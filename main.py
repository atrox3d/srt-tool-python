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
        # log.info(f'{root=}')
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


def group_srts(srt_list: list[Path]) -> dict:
    """
    create a dictionary using srt paths as keys and a list of dicts(filename, size) as values
    :param srt_list:
    :return:
    """
    # group srt files by path:
    # create dictionary path -> list[ dict(filename, filesize) ]
    grouped = {}
    for srt in srt_list:
        # select parent (movies), or parent of parent (tvshows), of srt file
        if srt.parent.name.lower() == 'subs' or srt.parent.parent.name.lower() == 'subs':
            # store srt filename and size in temp dict
            filedict: dict[str, int]
            filedict = dict(name=srt.name, size=srt.stat().st_size)
            #  create or update list of srt files
            if grouped.get(srt.parent, None):
                grouped[srt.parent].append(filedict)
            else:
                grouped[srt.parent] = [filedict]
    return grouped


def flatten_to_biggest(grouped: dict) -> dict:
    """
    convert list of dicts in one dict corresponding to the bigger srt file
    :param grouped:
    :return:
    """
    # flatten list of srt files to the bigger file
    flat_groups = grouped.copy()
    for path, files in flat_groups.items():
        bigger = None
        max_size = 0
        for file in files:
            if file['size'] > max_size:
                bigger = file['name']
        flat_groups[path] = bigger
    return flat_groups


def get_copyparams(grouped: dict) -> list[dict]:
    """
    create list of dicts containing source and dest path
    :param grouped:
    :return:
    """
    parameters = []
    parameter = {}
    # loop through flattened groups of srt files
    for path, file in grouped.items():
        # create source path for copy
        source_path = path / file

        if path.name.lower() == 'subs':
            # rename srt files based on movie name
            # if .../moviename/subs/file.srt

            # set destination path to movie folder
            dest_path = path.parent

            # set destination filename to movie folder name + .srt
            dest_name = path.parent.parts[-1] + '.srt'

            # create destination srt path
            destination_path = dest_path / dest_name
        elif path.parent.name.lower() == 'subs':
            # rename srt files based on tvshow episode name
            # if .../seasonname/subs/episodename/file.srt

            # set destination path to tvshow folder
            dest_path = path.parent.parent

            # set destination filename to subtitle folder name + .srt
            dest_name = path.parts[-1] + '.srt'

            # create destination srt path
            destination_path = dest_path / dest_name
        else:
            # implement new structure if exception is arisen
            raise ValueError(f'NOT IMPLEMENTED | unknown path structure: {path / file}')
        parameter = dict(src=source_path, dst=destination_path)
        parameters.append(parameter)
    return parameters


if __name__ == '__main__':
    log = get_logger(__name__)
    # log.setLevel('DEBUG')
    # push command line argument for testing in pycharm
    # sys.argv.append('d:/downloads')
    root = get_root('d:/downloads')

    srts = get_srtfiles(root)
    log.debug(f'{srts=}')

    groups = group_srts(srts)
    log.debug(f'{groups=}')

    flattened = flatten_to_biggest(groups)
    log.debug(f'{flattened=}')

    params = get_copyparams(flattened)
    log.debug(f'{params=}')

    for param in params:
        log.info(f'{param=}')
        # src = param['src']
        # dst = param['dst']
        src, dst = param.values()
        log.info(f'COPY | SRC | {src}')
        log.info(f'COPY | DST | {dst}')
        shutil.copy(src, dst)
