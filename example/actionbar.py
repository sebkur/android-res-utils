#!/usr/bin/python3

import pngs_from_svg as pfs


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
    Icon("svg/material/ic_info_48px", "info"),
    Icon("svg/material/ic_settings_48px", "settings"),
    Icon("svg/material/ic_battery_50_48px", "battery"),
    Icon("svg/ic_app_protection", "app_protection"),
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
        pfs.create_images(svg, res, dest, config.suffix, isize,
                           config.color, config.opacity)
