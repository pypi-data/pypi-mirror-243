# Nov-26-2023
# draw_similarity_map.py

import sys
import os
import cv2 as cv

from pnt2.src import cfg_pnt2


def draw_similarity_map(similarity_map):

    # Save Magnitude in file as grayscale.
    # ---------------------------------------------------------
    similarity_map_gray_path = cfg_pnt2.dir_debug + '/' + '_similarity_map_gray.png'
    result = cv.imwrite(similarity_map_gray_path, similarity_map)

    if result is False:
        print('ERROR: draw_similarity_map()')
        sys.exit(1)
    # ---------------------------------------------------------

    # Convert similarity_map to ColorMap.
    # ---------------------------------------------------------
    if os.path.exists(similarity_map_gray_path):

        similarity_map_gray = cv.imread(similarity_map_gray_path, cv.IMREAD_GRAYSCALE)

        os.remove(similarity_map_gray_path)

        similarity_map_color = cv.applyColorMap(similarity_map_gray, cv.COLORMAP_TURBO)
    else:
        print("ERROR in draw_similarity_map(): The file does not exist")
        sys.exit(1)
    # ---------------------------------------------------------

    similarity_map_color_path = cfg_pnt2.dir_debug + '/' + '_similarity_map.png'
    cv.imwrite(similarity_map_color_path, similarity_map_color)
