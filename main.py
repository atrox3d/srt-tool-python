import sys
import logging
from pathlib import Path
import shutil

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(module)s | %(levelname)-" + str(len("CRITICAL")) + "s | %(message)s",
    datefmt='%Y/%m/%d %H:%M:%S',
    stream=sys.stdout
)
log = logging.getLogger(__name__)

sys.argv.append('d:/downloads')
try:
    root = sys.argv[1]
except IndexError:
    root = '.'
root = Path(root).absolute()

log.info(f'{root=}')

srts = list(root.glob('**/*.srt'))

# create dictionary path -> list[ dict(filename, filesize) ]
groups = {}
for srt in srts:
    if srt.parent.name.lower() == 'subs' or srt.parent.parent.name.lower() == 'subs':
        filedict = dict(name=srt.name, size=srt.stat().st_size)
        if groups.get(srt.parent, None):
            groups[srt.parent].append(filedict)
        else:
            groups[srt.parent] = [filedict]

# flatten list to the bigger file
for path, files in groups.items():
    bigger = None
    max_size = 0
    for file in files:
        if file['size'] > max_size:
            bigger = file['name']

    groups[path] = bigger

for path, file in groups.items():
    src = path / file

    if path.name.lower() == 'subs':
        # if .../moviename/subs/file.srt

        # .../moviename/
        dest_path = path.parent
        # moviename
        dest_name = path.parent.parts[-1] + '.srt'
        # .../moviename/moviename.srt
        dst = dest_path / dest_name
    elif path.parent.name.lower() == 'subs':
        # if .../seasonname/subs/episodename/file.srt

        # .../seasonname/
        dest_path = path.parent.parent
        # episodename
        dest_name = path.parts[-1] + '.srt'
        # .../season/episodename.srt
        dst = dest_path / dest_name
    else:
        raise ValueError(f'unknown path structure: {path / file}')

    log.info(f'COPY | SRC | {src}')
    log.info(f'COPY | DST | {dst}')
    shutil.copy(src, dst)
