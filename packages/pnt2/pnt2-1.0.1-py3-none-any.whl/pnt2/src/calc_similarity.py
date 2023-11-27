# Nov-26-2023
# calc_similarity.py

import cv2 as cv
import numpy as np

from pnt2.src import cfg_pnt2
from pnt2.src.magnitude import get_magn_roi, get_magn_half
from pnt2.src.get_peaks import get_peaks
from pnt2.src.create_table import create_table
from pnt2.src.draw_magn import draw_magn
from pnt2.src.draw_peaks import draw_peaks
from pnt2.src.draw_result import draw_result
from pnt2.src.draw_image_warp import draw_image_warp
from pnt2.src.draw_similarity_map import draw_similarity_map
from pnt2.src.utils_list import save_list_of_peaks_txt


def calc_similarity(image: np.uint8, templ: np.uint8) -> float:

    image_magn_roi = get_magn_roi(image)
    image_magn_half = get_magn_half(image_magn_roi)
    image_list_of_peaks = get_peaks(image_magn_half)
    image_table = create_table(image_list_of_peaks)
    n_image_peaks = len(image_list_of_peaks)

    if cfg_pnt2.debug_mode:
        draw_magn('image', image_magn_roi)
        draw_peaks('image', image_list_of_peaks)
        save_list_of_peaks_txt('image_list_of_peaks', image_list_of_peaks)

    templ_magn_roi = get_magn_roi(templ)
    templ_magn_half = get_magn_half(templ_magn_roi)
    templ_list_of_peaks = get_peaks(templ_magn_half)
    templ_table = create_table(templ_list_of_peaks)
    n_templ_peaks = len(templ_list_of_peaks)

    if cfg_pnt2.debug_mode:
        draw_magn('templ', templ_magn_roi)
        draw_peaks('templ', templ_list_of_peaks)
        save_list_of_peaks_txt('templ_list_of_peaks', templ_list_of_peaks)

    similarity_map_current: np.float32 = np.float32(0)
    similarity_map_result: np.float32 = np.float32(0)

    similarity_result: float = -1

    for j in range(1, n_image_peaks):

        index_src = j
        x_src = image_table[j, 0]
        y_src = image_table[j, 1]
        length_src = image_table[j, 2]
        angle_src = image_table[j, 3]

        for i in range(1, n_templ_peaks):

            index_dst = i
            x_dst = templ_table[i, 0]
            y_dst = templ_table[i, 1]
            length_dst = templ_table[i, 2]
            angle_dst = templ_table[i, 3]

            angle: float = float(angle_dst - angle_src)
            scale: float = float(length_dst / length_src)
            mat_rotate = cv.getRotationMatrix2D(cfg_pnt2.center, angle, scale)

            image_magn_roi_warp \
                = cv.warpAffine(image_magn_roi, mat_rotate, cfg_pnt2.dsize_roi)

            if cfg_pnt2.debug_mode:
                similarity_current, similarity_map_current \
                    = calc_similarity_cont_map(
                                            np.float32(image_magn_roi_warp),
                                            np.float32(templ_magn_roi))
            else:
                similarity_current = calc_similarity_cont(
                                            np.float32(image_magn_roi_warp),
                                            np.float32(templ_magn_roi))

            if similarity_current > similarity_result:
                similarity_result = similarity_current

                if cfg_pnt2.debug_mode:
                    similarity_map_result = similarity_map_current.copy()
                    cfg_pnt2.index_src = index_src
                    cfg_pnt2.index_dst = index_dst
                    cfg_pnt2.x_src = x_src
                    cfg_pnt2.y_src = y_src
                    cfg_pnt2.x_dst = x_dst
                    cfg_pnt2.y_dst = y_dst
                    cfg_pnt2.angle_result = angle
                    cfg_pnt2.scale_result = scale

    if cfg_pnt2.debug_mode:
        draw_result('image')
        draw_result('templ')
        draw_image_warp()
        draw_similarity_map(similarity_map_result)

    return similarity_result


def calc_similarity_cont_map(
        magnitude_1: np.float32,
        magnitude_2: np.float32) -> (float, np.float32):

    arr_zero = np.zeros(cfg_pnt2.dsize_roi, dtype=np.float32)
    arr_1 = np.maximum(magnitude_1, arr_zero)
    arr_2 = np.maximum(magnitude_2, arr_zero)

    arr_min = np.minimum(arr_1, arr_2)
    arr_max = np.maximum(arr_1, arr_2)

    similarity_map = np.subtract(arr_max, arr_min, where=arr_min > 0)
    nonzero_count = np.count_nonzero(similarity_map)

    if nonzero_count == 0:
        similarity = 1.0
    else:
        average = np.sum(similarity_map) / nonzero_count
        similarity = 1.0 / (1.0 + cfg_pnt2.param_similarity * average)

    return similarity, similarity_map


def calc_similarity_cont(
        magnitude_1: np.float32,
        magnitude_2: np.float32) -> float:

    arr_zero = np.zeros(cfg_pnt2.dsize_roi, dtype=np.float32)
    arr_1 = np.maximum(magnitude_1, arr_zero)
    arr_2 = np.maximum(magnitude_2, arr_zero)

    arr_min = np.minimum(arr_1, arr_2)
    arr_max = np.maximum(arr_1, arr_2)

    similarity_map = np.subtract(arr_max, arr_min, where=arr_min > 0)
    nonzero_count = np.count_nonzero(similarity_map)

    if nonzero_count == 0:
        similarity = 1.0
    else:
        average = np.sum(similarity_map) / nonzero_count
        similarity = 1.0 / (1.0 + cfg_pnt2.param_similarity * average)

    return similarity
