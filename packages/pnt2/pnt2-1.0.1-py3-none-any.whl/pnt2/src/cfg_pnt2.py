# Nov-26-2023
# cfg_pnt2.py

# -----------------------------
debug_mode = False
# debug_mode = True

dir_debug = '_DEBUG_INFO_'
# -----------------------------

n_peaks: int = 11

param_similarity: float = 0.07

image_name = ''
templ_name = ''
path_image = ''
path_templ = ''

canonical_size: int = 100
size_dft: int = 2048
lp_param: int = 4
size_roi: int = size_dft // lp_param
dsize_roi = (size_roi, size_roi)
size_roi_half: int = size_roi // 2
X0: int = size_roi_half
Y0: int = size_roi_half
center = (X0, Y0)

index_src: int = -1
index_dst: int = -1
x_src: float = 0
y_src: float = 0
x_dst: float = 0
y_dst: float = 0
angle_result: float = 0
scale_result: float = 0

# 1 of 4
# ---------------------------------------------------------
# colormap = 'HOT'
colormap = 'HSV'
# colormap = 'JET'
# colormap = 'TURBO'
# ---------------------------------------------------------

# colors (BGR)
# -----------------------------------------
black = (0, 0, 0)
maraschino = (0, 38, 255)
clover = (0, 143, 0)
aqua = (255, 150, 0)
cayenne = (0, 17, 148)
blueberry = (255, 51, 4)
magenta = (255, 64, 255)
ocean = (147, 84, 0)
nickel = (146, 146, 146)
moss = (81, 144, 0)
lemon = (0, 251, 255)
white = (255, 255, 255)
# -----------------------------------------

