import json
import pandas as pd
from pathlib import Path
import typer
from typing import Dict, List, Text
from giffer import gifware, imgware

# LANG - hindi, bengali, gujurati, odia, punjabi, urdu, marati, | tamil, telugu, kannada, malayalam

parser = typer.Typer(help="GIF CLI")


def bake_template(path: Path) -> dict:
    '''Designs the template string from the configuration file.
    Input:
        path: Configuration file
    Returns:
        Template

    eg:
    config
    {
        'num_frames': 2,
        'duration': "[1,3]",
        'tags': {
            'T1': {'frames': [1,2], 'box': [0,0,1,1], 'color': 'black'},
            'T2': {'frames': [2],   'box': [1,1,2,2], 'color': 'black'}
        }
    }

    template:
    {
        '1': [
            {'caption': 'T1', 'box': [0,0,1,1], 'color': 'black'}
        ]
        '2': [
            {'caption': 'T1', 'box': [0,0,1,1], 'color': 'black'},
            {'caption': 'T2', 'box': [1,1,2,2], 'color': 'black'}
        ]
    }

    '''
    config = json.load((path).open('r', encoding='utf-8'))

    vframes = set(frame for _, v in config['tags'].items() for frame in v['frames'])
    template = {
        'meta': {'duration': config['duration']}
    }
    for frame in vframes:
        template[str(frame)] = [{'caption': t, 'box': v['box'], 'fill': v['color'],'bgloc':v.get('bgloc',None)}
                                for t, v in config['tags'].items() if frame in v['frames']]

    return template


@parser.command()
def parse(path: str = typer.Option(..., '--path', '-p', help='Path to the source GIF/Image file'),
          data: str = typer.Option('data', '--data', '-d',
                                   help='Path to data dir', show_default=True),
          lang: str = typer.Option(..., '--lang', '-l', help='Languages comma separated: hindi, marathi, odia')):
    '''Runs the code for each language & generates a modified SRC for the same.'''
    SRC = Path(path)
    DATA = Path(data)
    LANG = [L.strip() for L in lang.split(',')]
    FILE = f'covid-spread - {SRC.stem}.csv'
    CONFIG = f'{SRC.stem}.json'
    SUFFIX = Path(SRC).suffix

    data = pd.read_csv(DATA/FILE, index_col='language', skiprows=[1])
    template = bake_template(DATA/CONFIG)

    OUT = Path('out')/'gif'/SRC.stem if SUFFIX == '.gif' else Path('out')/'image'/SRC.stem
    OUT.mkdir(exist_ok=True, parents=True)

    for L in LANG:
        print(f'Creating {L}{SUFFIX}')
        template['meta']['lang'] = L

        if SUFFIX == '.gif':
            gifware(SRC, data[L].to_dict(), template, f'{OUT}/{L}.gif')
        else:
            imgware(SRC, data[L].to_dict(), template, f'{OUT}/{L}.png')


if __name__ == '__main__':
    parser()
