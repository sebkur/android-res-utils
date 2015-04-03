#!/usr/bin/python3

import os
import shlex
import subprocess
import tempfile
import shutil
import argparse
import re

import xml.etree.ElementTree as ElementTree

DIRS = ["drawable-mdpi", "drawable-hdpi", "drawable-xhdpi", "drawable-xxhdpi"]

def remove_opacity(path):
    style = path.get('style')

    if style is not None:
        style = re.sub("opacity:\s*\d?\.?\d*;?", "", style)
        path.set("style", style)

    if path.get('fill-opacity') is not None:
        del path.attrib['fill-opacity']


def remove_color(path):
    style = path.get('style')

    if style is not None:
        style = re.sub("fill:\s*#\d{3,6};?", "", style)
        path.set("style", style)


def modify_svg(svg, tmp, color, opacity):
    ns = "http://www.w3.org/2000/svg"
    ElementTree.register_namespace("", ns)

    tree = ElementTree.parse(svg)

    if opacity:
        for path in tree.iter("{" + ns + "}g"):
            remove_opacity(path)

    for path in tree.iter("{" + ns + "}path"):
        if path.get('fill') != "none":
            if color:
                remove_color(path)
                path.set("fill", color)

            if opacity:
                remove_opacity(path)
                path.set("opacity", str(opacity))

    tree.write(tmp)


def create_images(svg, dir_pngs, namebase, suffix, isize, color, opacity, nopngcrush=False):
    # dimensions for mdpi/hdpi/xhdpi/xxhdpi
    sizes = [isize, isize * 1.5, isize * 2, isize * 3]

    tmp_svg = tempfile.mkstemp(".svg")
    os.close(tmp_svg[0])

    modify_svg(svg, tmp_svg[1], color, opacity)

    for s in range(len(sizes)):
        size = sizes[s]
        output_dir = os.path.join(dir_pngs, DIRS[s])

        if not os.path.isdir(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        output = os.path.join(output_dir, namebase + suffix + ".png")
        print (svg + ' -> ' + output)

        create_png(tmp_svg[1], output, size, nopngcrush)

    os.remove(tmp_svg[1])


def create_png(svg, output, size, nopngcrush):
    cmd = "inkscape -C -e " + output + " -h " + str(size) + " " + svg
    args = shlex.split(cmd, False, running_on_posix)
    subprocess.call(args)

    if nopngcrush == False:
        tmp_png = tempfile.mkstemp(".png")
        os.close(tmp_png[0])
        shutil.copyfile(output, tmp_png[1])
        os.remove(output)

        cmd = "pngcrush " + tmp_png[1] + " " + output
        args = shlex.split(cmd, False, running_on_posix)
        subprocess.call(args)

        os.remove(tmp_png[1])


def is_posix():
    try:
        import posix
        return True
    except ImportError:
        return False

running_on_posix = is_posix()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("input_filename",      help="Path to the svg file")
    parser.add_argument("output_directory",    help="Output directory")
    parser.add_argument("size",                help="Size in pixel for the mdpi variant", type=int)
    parser.add_argument("-c", "--color",       help="Color, e.g. '#104E8B'")
    parser.add_argument("-o", "--opacity",     help="Opacity, e.g. '0.54'",               type=float)
    parser.add_argument("-s", "--suffix",      help="Suffix for the output filenames",    default="")
    parser.add_argument("-nc", "--nopngcrush", help="Don't run pngcrush", action="store_true")
    args = parser.parse_args()

    svg_name = os.path.basename(args.input_filename)
    name = svg_name
    if svg_name.lower().endswith(".svg"):
        name = svg_name[:-4]

    create_images(args.input_filename, args.output_directory, name, args.suffix, args.size, args.color, args.opacity, nopngcrush=args.nopngcrush)
