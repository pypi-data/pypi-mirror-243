# Nov-27-2023
# create_template.py

import cv2 as cv
import numpy as np

from shapes_recognition.src import cfg


def create_template(rows, cols):

    img_template_height = rows * cfg.cell_height + rows * cfg.space + cfg.caption_height
    img_template_width = cols * cfg.cell_width + (cols + 1) * cfg.space

    channels = 3
    img_template = np.empty((img_template_height, img_template_width, channels), dtype=np.uint8)
    img_template.fill(cfg.color_background)

    img_template, g_img_template, r_img_template = cv.split(img_template)

    if cfg.show_caption:
        color = cfg.color_caption_enable
    else:
        color = cfg.color_caption_disable

    add_layer_border(img_template)
    draw_abcd(img_template, color[0])

    add_layer_border(g_img_template)
    draw_abcd(g_img_template, color[1])

    add_layer_border(r_img_template)
    draw_abcd(r_img_template, color[2])

    return img_template, g_img_template, r_img_template


def draw_abcd(layer, caption_text_color):

    x0 = cfg.x_caption_pos + cfg.space
    y0 = cfg.y_caption_pos

    draw_text(layer, x0, y0, caption_text_color, cfg.font_scale, 'A')
    x0 += cfg.cell_width + cfg.space
    draw_text(layer, x0, y0, caption_text_color, cfg.font_scale, 'B')
    x0 += cfg.cell_width + cfg.space
    draw_text(layer, x0, y0, caption_text_color, cfg.font_scale, 'C')
    x0 += cfg.cell_width + cfg.space
    draw_text(layer, x0, y0, caption_text_color, cfg.font_scale, 'D')


def draw_text(layer, x, y, text_color, font_scale, text):
    font = cv.FONT_HERSHEY_SIMPLEX
    font_color = text_color
    thickness = 2
    cv.putText(layer,
               text,
               (x, y),
               font,
               font_scale,
               font_color,
               thickness,
               cv.LINE_AA)


def add_layer_border(layer):

    height = layer.shape[0]
    width = layer.shape[1]

    for j in range(height):
        layer[j, 0] = cfg.color_border
        layer[j, width - 1] = cfg.color_border

    for i in range(width):
        layer[0, i] = cfg.color_border
        layer[height - 1, i] = cfg.color_border
