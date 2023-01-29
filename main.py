import shutil
import sys

from classes.subtitles import Subtitle
from modules import logger
from modules import logic
from modules import path

log = logger.get_logger(__name__)
# log.setLevel('DEBUG')

# push command line argument for testing in pycharm
# sys.argv.append('d:/downloads')
root = path.get_root(sys.argv, 'd:/downloads')

subtitle_list = Subtitle.get_from_path(root)
log.debug(f'{subtitle_list=}')

grouped_subtitles = Subtitle.group_by_path(subtitle_list)
log.debug(f'{grouped_subtitles=}')

subtitles: list[Subtitle] = []
for path, files in grouped_subtitles.items():
    biggest = Subtitle.get_biggest(files)
    subtitles.append(biggest)
log.debug(f'{subtitles=}')

# loop through flattened groups of srt files
for subtitle in subtitles:
    # create source path for copy
    src = subtitle.path
    dst = logic.get_destination_path(subtitle.parent, subtitle.name)
    log.info(f'COPY | SRC | {src}')
    log.info(f'COPY | DST | {dst}')
    shutil.copy(src, dst)
