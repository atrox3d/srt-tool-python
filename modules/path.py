from pathlib import Path
from modules import logger

log = logger.get_logger(__name__)


def get_root(args, path=None) -> Path:
    """
    get root path to begin search
    :param args:
    :param path:
    :return:
    """
    log.info(f'{args=}')
    log.info(f'{path=}')
    if not path:
        # get path from command line argument or work from cwd
        try:
            root_path = args[1]
        except IndexError:
            log.warning('No Path and no script args: setting root_path to cwd')
            root_path = '.'
    else:
        root_path = path
        log.info(f'setting {root_path=}')

    # set root path
    root_path = Path(root_path).absolute()
    log.info(f'{root_path=}')
    return root_path


def get_files(root_path: Path, pattern='**/*') -> list[Path]:
    """
    search .srt files under root path and return them in a list of paths
    :param root_path:
    :param pattern:
    :return:
    """
    # get list of all .srt files
    srt_files = list(root_path.glob(pattern))
    return srt_files
