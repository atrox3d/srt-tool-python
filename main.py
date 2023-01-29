import shutil

from modules import logger
from modules import logic
from modules import path

if __name__ == '__main__':
    log = logger.get_logger(__name__)
    # log.setLevel('DEBUG')

    # push command line argument for testing in pycharm
    # sys.argv.append('d:/downloads')
    # root = path.get_root('d:/downloads')
    root = path.get_root()

    srts = path.get_srtfiles(root)
    log.debug(f'{srts=}')

    groups = logic.group_srts_by_path(srts)
    log.debug(f'{groups=}')

    for path, files in groups.items():
        biggest = logic.get_biggest(files)
        filename, size = biggest.values()
        groups[path] = filename
    log.debug(f'{groups=}')

    parameters = []
    parameter = {}
    # loop through flattened groups of srt files
    for path, file in groups.items():
        # create source path for copy
        source_path = path / file
        destination_path = logic.get_destination_path(path, file)
        parameter = dict(src=source_path, dst=destination_path)
        parameters.append(parameter)

    for parameter in parameters:
        log.debug(f'{parameter=}')
        src, dst = parameter.values()
        log.info(f'COPY | SRC | {src}')
        log.info(f'COPY | DST | {dst}')
        shutil.copy(src, dst)
