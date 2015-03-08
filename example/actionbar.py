#!/usr/bin/python3

import pngs_from_svg_xml as pfsx


class Icon:
    def __init__(self, source, dest):
        self.source = source
        self.dest = dest


class Config:
    def __init__(self, color, opacity, suffix):
        self.color = color
        self.opacity = opacity
        self.suffix = suffix

ICONS = [
    Icon("material/ic_info_48px", "info"),
    Icon("material/ic_settings_48px", "settings"),
    Icon("material/ic_battery_50_48px", "battery"),
    ]

CONFIGS = [
    Config("#f00", 0.75, "_red"),
    Config("#00f", 0.5, "_blue"),
    ]

res = "res"
isize = 24

for icon in ICONS:
    svg = icon.source + ".svg"
    dest = icon.dest
    for config in CONFIGS:
        pfsx.create_images(svg, res, dest, config.suffix, isize,
                           config.color, config.opacity)
