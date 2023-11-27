# Nov-26-2023
# get_similarity.py

from pnt2.src import cfg_pnt2
from pnt2.src.canonical import convert_to_canonical
from pnt2.src.calc_similarity import calc_similarity
from pnt2.src.draw_canonical import draw_canonical


def get_similarity(path_1: str, path_2: str) -> float:

    image = convert_to_canonical('image', path_1)
    templ = convert_to_canonical('templ', path_2)

    if cfg_pnt2.debug_mode:
        draw_canonical(image, templ)

    similarity = calc_similarity(image, templ)

    return similarity
