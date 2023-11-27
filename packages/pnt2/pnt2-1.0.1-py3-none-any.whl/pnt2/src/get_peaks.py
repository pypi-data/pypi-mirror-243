# Nov-26-2023
# get_peaks.py

import numpy as np
from numpy import ndarray

from pnt2.src import cfg_pnt2

color_black: np.uint8 = np.uint8(0)
color_dark_gray: np.uint8 = np.uint8(80)
color_light_gray: np.uint8 = np.uint8(160)

coeff_1: float = 0.02
coeff_2: float = 0.01
coeff_3: float = 0.005

seed_y: int = 0
seed_x: int = 0

peak_y: int = 0
peak_x: int = 0


def get_peaks(magn_half: ndarray):

    global seed_y, seed_x, peak_y, peak_x
    global coeff_1, coeff_2, coeff_3
    global color_black, color_dark_gray, color_light_gray

    z_max = np.amax(magn_half)
    z_step = coeff_1 * z_max

    n_detected_peaks = 0

    list_of_peaks = []

    z_cut = z_max
    n_cut = 1

    while True:

        z_cut -= z_step

        if z_cut < 0.0:
            break

        canvas = np.where(magn_half > z_cut,
                          color_light_gray, color_black)

        while True:

            result = np.where(canvas == color_light_gray)

            number = result[0].size
            if number == 0:
                break

            list_coord = list(zip(result[0], result[1]))

            first = list_coord[0]
            seed_y = int(first[0])
            seed_x = int(first[1])

            fill_canvas(canvas,
                        magn_half,
                        color_light_gray,
                        color_dark_gray)

            if list_of_peaks.count((peak_y, peak_x)) == 0:
                list_of_peaks.append((peak_y, peak_x))

            n_detected_peaks = len(list_of_peaks)

        if n_detected_peaks >= cfg_pnt2.n_peaks:
            break

        if n_detected_peaks > 4:
            z_step = coeff_2 * z_max
        if n_detected_peaks > 8:
            z_step = coeff_3 * z_max

        n_cut += 1

    return list_of_peaks


def fill_canvas(
        canvas,
        magnitude: ndarray,
        old_value: np.uint8,
        new_value: np.uint8):

    """
        https://gist.github.com/JDWarner/1158a9515c7f1b1c21f1
        Thanks, JD!
    """

    global seed_y, seed_x, peak_y, peak_x

    ysize_1 = canvas.shape[0] - 1
    xsize_1 = canvas.shape[1] - 1

    stack = {(seed_y, seed_x)}

    magnitude_max = np.float32(0)

    while stack:

        y, x = stack.pop()

        temp = magnitude[y, x]

        if temp > magnitude_max:

            magnitude_max = temp

            peak_y = y
            peak_x = x

        if canvas[y, x] == old_value:

            canvas[y, x] = new_value

            if y > 0:
                stack.add((y - 1, x))
            if y < ysize_1:
                stack.add((y + 1, x))
            if x > 0:
                stack.add((y, x - 1))
            if x < xsize_1:
                stack.add((y, x + 1))
