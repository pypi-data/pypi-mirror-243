# Nov-26-2023
# get_angle.py

"""
Система координат изображения в OpenCV (opencv-coordinates)

The coordinate origin is assumed to be the top-left corner. Rotation angle in degrees.
Positive values mean counter-clockwise rotation (против часовой стрелки).


0----------------> X
|
|
|
|
|
Y


Система координат централизованная (center-coordinates)

         Y
         ^
         |
         |
---------0--------> X
         |
         |
         |
         |
"""

import math

from pnt2.src import cfg_pnt2


def get_angle(x_a, y_a, x_b, y_b) -> float:

    """
    (x_a, y_a), (x_b, y_b) - координаты двух локальных максимумов спектра
    (пиков) в системе координат изображения (opencv-coordinates).

    Проводим два вектора из центра изображения в точки нахождения этих пиков.
    Функция вычисляет угол между этими векторами в централизованной системе
    координат.

    Диапазон измерения угла [0 - 180] градусов. Результат всегда >= 0,
    т.е. угол не зависит от порядка вводимых векторов.
    """

    # Координаты пиков в централизованной системе координат.
    _x1 = float(x_a - cfg_pnt2.X0)
    _y1 = float(cfg_pnt2.Y0 - y_a)

    _x2 = float(x_b - cfg_pnt2.X0)
    _y2 = float(cfg_pnt2.Y0 - y_b)

    top = (_x1 * _x2) + (_y1 * _y2)
    bottom = math.sqrt((_x1 * _x1) + (_y1 * _y1)) * math.sqrt((_x2 * _x2) + (_y2 * _y2))

    if bottom > 0.0:
        cos_angle = top / bottom

        if cos_angle > 1.0:
            cos_angle = 1.0
        if cos_angle < -1.0:
            cos_angle = -1.0

        angle_rad = math.acos(cos_angle)
        angle_deg = math.degrees(angle_rad)
    else:
        angle_deg = 0.0

    return angle_deg


def get_angle_axe_x(x, y) -> float:

    """
    x, y - координаты локального максимума спектра (пика) в
    системе координат изображения (opencv-coordinates).

    Проводим вектор из центра изображения в точку нахождения пика.
    Функция вычисляет угол между этим вектором и осью X в централизованной
    системе координат.
    Диапазон [0 - 360] градусов. Результат всегда >= 0.
    """

    # Координаты пиков в централизованной системе координат.
    _x1 = float(x - cfg_pnt2.X0)
    _y1 = float(cfg_pnt2.Y0 - y)

    _x2 = 1.0
    _y2 = 0.0

    top = (_x1 * _x2) + (_y1 * _y2)
    bottom = math.sqrt((_x1 * _x1) + (_y1 * _y1)) * math.sqrt((_x2 * _x2) + (_y2 * _y2))

    if bottom > 0.0:
        cos_angle = top / bottom

        if cos_angle > 1.0:
            cos_angle = 1.0
        if cos_angle < -1.0:
            cos_angle = -1.0

        angle_rad = math.acos(cos_angle)
        angle_deg = math.degrees(angle_rad)

        if _y1 < 0.0:
            angle_deg = 360.0 - angle_deg
    else:
        angle_deg = 0.0

    return angle_deg

