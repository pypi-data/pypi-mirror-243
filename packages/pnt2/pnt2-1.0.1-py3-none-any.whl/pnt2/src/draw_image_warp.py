# Nov-26-2023
# draw_image_warp.py

import cv2 as cv
from pathlib import Path

from pnt2.src import cfg_pnt2


def draw_image_warp():

    path_in = str(Path.cwd() / cfg_pnt2.dir_debug / 'image.png')
    image_in = cv.imread(path_in, cv.IMREAD_UNCHANGED)

    angle: float = cfg_pnt2.angle_result
    scale: float = cfg_pnt2.scale_result
    mat_rotate = cv.getRotationMatrix2D(cfg_pnt2.center, angle, scale)

    image_out = cv.warpAffine(image_in, mat_rotate, cfg_pnt2.dsize_roi)

    path_out = str(Path.cwd() / cfg_pnt2.dir_debug / 'image_warp.png')
    cv.imwrite(path_out, image_out)
