import sys
from pathlib import Path
from modules import  logger

log = logger.get_logger(__name__)


def get_root(path=None) -> Path:
    """
    get root path to begin search
    :param path:
    :return:
    """
    if not path:
        # get path from command line argument or work from cwd
        log.info(f'{path=}')
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
