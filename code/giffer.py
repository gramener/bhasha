import cv2
import imageio as io
import numpy as np
from dataclasses import dataclass
from pathlib import Path
from pygifsicle import optimize
from PIL import Image, ImageDraw, ImageFont
from typing import List, Callable, Union


@dataclass
class Box:
    L: int = 0
    T: int = 0
    R: int = 0
    B: int = 0

    def pad(self, p=5):
        self.L, self.T = self.L + p, self.T + p
        self.R, self.B = self.R - p, self.B - p


def draw_clean_text(draw: ImageDraw, text: str, lang: str, box: Box, fill: str = 'black', spacing: int = 0, pad: int = 0) -> None:
    '''Place the text at the center of the bounding box.
    Input:
        draw:    ImageDraw instance
        text:    Content to add
        lang:    Language
        box:     Bounding box
        fill:    Color of text
        spacing: Vertical spacing between lines
        pad:     Inner padding to add to the bounding box
    '''
    box.pad(p=pad)
    W, H = (box.R - box.L), (box.B - box.T)
    font_path = f'data/fonts/indic/{lang}.ttf'
    F = ImageFont.truetype(font=font_path, size=1)

    size = 1

    w, h = draw.multiline_textsize(text, font=F, spacing=spacing)
    while w < W and h < H:
        size += 1
        F = ImageFont.truetype(font=font_path, size=size)
        w, h = draw.multiline_textsize(text, font=F, spacing=spacing)

    # TODO: fix, uncomment this if you want a static size & not dynamic size for texts
    # size = 30 if size < 70 else 100

    F = ImageFont.truetype(font=font_path, size=size)
    w, h = F.getsize_multiline(text)

    cx = (W - w) / 2 + box.L
    cy = (H - h) / 2 + box.T - 10

    draw.multiline_text((cx, cy), text, fill=fill, font=F, align='center', spacing=spacing)


def draw_caption(image: Union[np.ndarray, None], data: dict, captions: List[dict], lang: str, gif: bool = True) -> np.ndarray:
    '''Draws text on an Image.

    Input:
        image: Image to be modified
        data: tag => language mapping
        captions: List of tags with their metadata
        lang: Language of the text
        gif: Format of the input image

    Returns:
        Image with text drawn on it
    '''
    _image = Image.fromarray(image) if gif else image
    draw = ImageDraw.Draw(_image)

    for c in captions:
        caption = data[c['caption']]
        box = Box(*c['box'])
        fill = c['fill']
        # draw.rectangle([(box.L, box.T), (box.R, box.B)], fill="#ddffff", outline="blue")
        draw_clean_text(draw, caption, lang, box, fill, spacing=10, pad=8)

    return np.array(_image) if gif else _image


def gifware(file: Path, data: dict, template: dict, save: str = 'test.gif') -> None:
    '''Modify the contents of a GIF to regional languages.

    Input:
        file: GIF input file
        data: tag => language mapping
        template: Instructions on where to position the text
        save: Path to save the modified GIF
    '''
    gif = io.mimread(file)
    frames = []

    for (i, frame) in enumerate(gif):
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2RGB)
        if str(i) in template:
            frame = draw_caption(
                frame, data, captions=template[str(i)], lang=template['meta']['lang'])

        frames.append(frame)

    io.mimwrite(save, frames, duration=eval(template['meta']['duration']))
    optimize(str(save))


def imgware(file: Path, data: dict, template: dict, save: str = 'test.gif') -> None:
    '''Modify the contents of an Image to regional languages.

    Input:
        file: Image input file
        data: tag => language mapping
        template: Instructions on where to position the text
        save: Path to save the modified Image
    '''
    image = Image.open(file).convert('RGBA')
    image = draw_caption(
        image, data, captions=template["1"], lang=template['meta']['lang'], gif=False)
    print('Saving:', save)
    image.save(save, 'PNG')
