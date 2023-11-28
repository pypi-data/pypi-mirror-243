# Nov-27-2023
# cfg_pnt3.py

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

angle_min: float = 20
angle_max: float = 120
angle_ratio_threshold: float = 2.5

y_image_blue: int = -1
x_image_blue: int = -1
y_image_red: int = -1
x_image_red: int = -1

y_templ_blue: int = -1
x_templ_blue: int = -1
y_templ_red: int = -1
x_templ_red: int = -1

# 1 of 3
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
