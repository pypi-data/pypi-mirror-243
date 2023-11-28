# Nov-27-2023
# cfg.py

method: int = 0

path_image = ''
path_templ = ''

n_items: int = 6
n_types: int = -1
n_types_max: int = 4
n_items_recognition: int = 0

canonical_size: int = 100

cell_size: int = 200
cell_width: int = cell_size
cell_height: int = cell_size

caption_height: int = 45
x_caption_pos: int = cell_width // 2 - 8
y_caption_pos: int = 33
space: int = 9

show_caption: bool = True
color_background: int = 224
color_border: int = 64
color_caption_enable = (0, 38, 255)
color_caption_disable = (224, 224, 224)
font_scale = 1.0

time_self_study = ''
time_recognition = ''

dir_self_study = 'DATA_SELF_STUDY'
dir_recognition = 'DATA_RECOGNITION'
dir_results = '_RESULTS_'
