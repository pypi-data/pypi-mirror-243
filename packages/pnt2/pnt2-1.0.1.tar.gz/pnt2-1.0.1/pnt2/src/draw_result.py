# Nov-26-2023
# draw_result.py

import cv2 as cv

from pnt2.src import cfg_pnt2


def draw_result(tag):

    path_in = cfg_pnt2.dir_debug + '/' + tag + '_peaks.png'
    magn = cv.imread(path_in, cv.IMREAD_UNCHANGED)

    x1 = cfg_pnt2.X0
    y1 = cfg_pnt2.Y0
    x2: int = 0
    y2: int = 0

    if tag == 'image':
        x2 = int(cfg_pnt2.x_src)
        y2 = int(cfg_pnt2.y_src)

    if tag == 'templ':
        x2 = int(cfg_pnt2.x_dst)
        y2 = int(cfg_pnt2.y_dst)

    thickness = 1
    cv.line(magn,
            (x1, y1),
            (x2, y2),
            cfg_pnt2.black, thickness)

    path_out = cfg_pnt2.dir_debug + '/' + tag + '_result.png'
    cv.imwrite(path_out, magn)
