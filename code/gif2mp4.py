import subprocess
import typer
from pathlib import Path


def transform(path: str):
    folder = Path(path)
    for gif in folder.glob('*.gif'):
        subprocess.call(
            f'ffmpeg -i {folder/gif.stem}.gif -vsync 0 -f mp4 -pix_fmt yuv420p -y {folder/gif.stem}.mp4', shell=True)


if __name__ == '__main__':
    typer.run(transform)
