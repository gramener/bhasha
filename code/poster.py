import cv2
import imageio as io
import typer
from pathlib import Path


def splitone(path: str = typer.Option(..., '--path', '-p', help='Pass path to the directory containing the mp4 files.'),
             num: int = typer.Option(0, '--num', '-n', help='Pass the frame number.')):
    '''Creates a poster image for all mp4 files in the path.'''
    f = Path(path)

    for gif in f.glob('*.gif'):
        for (i, frame) in enumerate(io.get_reader(gif)):
            if i == num:
                frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
                io.imwrite(f'{f}/{gif.parent.stem}-{gif.stem}.png', frame)


if __name__ == '__main__':
    typer.run(splitone)
