import cv2
import imageio as io
import typer
from pathlib import Path

sm = typer.Typer()


@sm.command('split')
def split_and_store(path: str = typer.Option(..., '--path', '-p', help='Pass the path of the GIF file')):
    '''Splits the GIFs into its individual components.'''
    f = Path(path)
    Path(f'{f.parent}/frames/{f.stem}').mkdir(exist_ok=True, parents=True)

    for (i, frame) in enumerate(io.get_reader(f)):
        io.imwrite(f'{f.parent}/frames/{f.stem}/{f.stem}_{i}.tiff', frame)


@sm.command('merge')
def read_and_merge(path: str = typer.Option(..., '--path', '-p', help='Pass the path of the frames', ),
                   name: str = typer.Option(..., '--name', '-n', help='Pass the name of the file.')):
    '''Reads TIFF files from the path specified & creates a GIF out of it.'''
    f = Path(path)
    frames = []

    for p in sorted(list(f.glob('*.tiff')), key=lambda x: int(x.stem.rsplit('_')[1])):
        frame = io.imread(p)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
        frames.append(frame)

    io.mimwrite(f.parent.parent/name, frames, fps=1)


if __name__ == "__main__":
    sm()
