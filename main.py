import sys
import logging
from pathlib import Path
import shutil


def get_logger(name):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(module)s | %(levelname)-" + str(len("CRITICAL")) + "s | %(message)s",
        datefmt='%Y/%m/%d %H:%M:%S',
        stream=sys.stdout
    )
    logger = logging.getLogger(name)
    return logger


def get_root(path=None):
    # push command line argument for testing in pycharm
    sys.argv.append('d:/downloads')

    if not path:
        # get path from command line argument or work from cwd
        try:
            root = sys.argv[1]
        except IndexError:
            root = '.'
    else:
        root = path

        # set root path
        root = Path(root).absolute()
        # log.info(f'{root=}')
        return root


# get list of all .srt files
srts = list(root.glob('**/*.srt'))

# group srt files by path:
# create dictionary path -> list[ dict(filename, filesize) ]
groups = {}
for srt in srts:
    # select parent (movies), or parent of parent (tvshows), of srt file
    if srt.parent.name.lower() == 'subs' or srt.parent.parent.name.lower() == 'subs':
        # store srt filename and size in temp dict
        filedict = dict(name=srt.name, size=srt.stat().st_size)
        #  create or update list of srt files
        if groups.get(srt.parent, None):
            groups[srt.parent].append(filedict)
        else:
            groups[srt.parent] = [filedict]

# flatten list of srt files to the bigger file
for path, files in groups.items():
    bigger = None
    max_size = 0
    for file in files:
        if file['size'] > max_size:
            bigger = file['name']
    groups[path] = bigger

# loop through flattened groups of srt files
for path, file in groups.items():
    # create source path for copy
    src = path / file

    if path.name.lower() == 'subs':
        # rename srt files based on movie name
        # if .../moviename/subs/file.srt

        # set destination path to movie folder
        dest_path = path.parent

        # set destination filename to movie folder name + .srt
        dest_name = path.parent.parts[-1] + '.srt'

        # create destination srt path
        dst = dest_path / dest_name
    elif path.parent.name.lower() == 'subs':
        # rename srt files based on tvshow episode name
        # if .../seasonname/subs/episodename/file.srt

        # set destination path to tvshow folder
        dest_path = path.parent.parent

        # set destination filename to subtitle folder name + .srt
        dest_name = path.parts[-1] + '.srt'

        # create destination srt path
        dst = dest_path / dest_name
    else:
        # implement new structure if exception is arisen
        raise ValueError(f'NOT IMPLEMENTED | unknown path structure: {path / file}')

    log.info(f'COPY | SRC | {src}')
    log.info(f'COPY | DST | {dst}')
    shutil.copy(src, dst)
