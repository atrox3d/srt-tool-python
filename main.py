import shutil
import sys

from classes.subtitles import Subtitle, SubtitleList
from modules import logger
from modules import logic
from modules import path

log = logger.get_logger(__name__)
# log.setLevel('DEBUG')

# push command line argument for testing in pycharm
# sys.argv.append('d:/downloads')
root = path.get_root(sys.argv)

subtitle_list = SubtitleList.from_path(root)
log.debug(f'{subtitle_list=}')

grouped_subtitles = subtitle_list.to_dict()
log.debug(f'{grouped_subtitles=}')

subtitle_list = SubtitleList()
for path, files in grouped_subtitles.items():
    biggest = SubtitleList.get_biggest(files)
    subtitle_list.append(biggest)
log.debug(f'{subtitle_list=}')

# loop through flattened groups of srt files
for subtitle in subtitle_list:
    # create source path for copy
    src = subtitle.path
    dst = logic.get_destination_path(subtitle.parent, subtitle.name)
    log.info(f'COPY | SRC | {src}')
    log.info(f'COPY | DST | {dst}')
    shutil.copy(src, dst)
