# Nov-26-2023
# draw_magn.py

import sys
import os
import cv2 as cv
import numpy as np

from pnt2.src import cfg_pnt2


def draw_magn(tag, any_image_magn):

    # Save Magnitude in file as grayscale.
    # ---------------------------------------------------------
    magnitude_gray_path = cfg_pnt2.dir_debug + '/' + tag + '_gray.png'
    result = cv.imwrite(magnitude_gray_path, any_image_magn)

    if result is False:
        print('ERROR: draw_magn()')
        sys.exit(1)
    # ---------------------------------------------------------

    # Convert Magnitude to ColorMap.
    # ---------------------------------------------------------
    magnitude_color = np.uint8(0)

    if os.path.exists(magnitude_gray_path):

        magnitude_gray = cv.imread(magnitude_gray_path, cv.IMREAD_GRAYSCALE)

        os.remove(magnitude_gray_path)

        if cfg_pnt2.colormap == 'HOT':
            magnitude_color = cv.applyColorMap(magnitude_gray, cv.COLORMAP_HOT)

        if cfg_pnt2.colormap == 'HSV':
            magnitude_color = cv.applyColorMap(magnitude_gray, cv.COLORMAP_HSV)

        if cfg_pnt2.colormap == 'JET':
            magnitude_color = cv.applyColorMap(magnitude_gray, cv.COLORMAP_JET)

        if cfg_pnt2.colormap == 'TURBO':
            magnitude_color = cv.applyColorMap(magnitude_gray, cv.COLORMAP_TURBO)
    else:
        print("ERROR in draw_magn(): The file does not exist")
        sys.exit(1)
    # ---------------------------------------------------------

    magnitude_color_path = cfg_pnt2.dir_debug + '/' + tag + '.png'
    cv.imwrite(magnitude_color_path, magnitude_color)
