#!/usr/bin/python3

import sys
import os
import shlex
import subprocess
import tempfile
import shutil

import xml.etree.ElementTree as ElementTree

DIRS = ["drawable-mdpi", "drawable-hdpi", "drawable-xhdpi", "drawable-xxhdpi"]


def modify_svg(svg, tmp, color, opacity):
    ns = "http://www.w3.org/2000/svg"
    ElementTree.register_namespace("", ns)

    tree = ElementTree.parse(svg)
    root = tree.getroot()

    for path in root.findall("{" + ns + "}path"):
        print(path)
        fill = path.get('fill')
        if fill is None:
            print(fill)
            path.set("fill", color)
            path.set("opacity", str(opacity))

    tree.write(tmp)


def create_images(svg, dir_pngs, namebase, suffix, isize, color, opacity):
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

        create_png(tmp_svg[1], output, size)

    #os.remove(tmp_svg[1])


def create_png(svg, output, size):
    cmd = "inkscape -C -e " + output + " -h " + str(size) + " " + svg
    args = shlex.split(cmd, False, running_on_posix)
    subprocess.call(args)

    tmp_png = tempfile.mkstemp(".png")
    os.close(tmp_png[0])
    shutil.copyfile(output, tmp_png[1])
    os.remove(output)

    cmd = "pngcrush " + tmp_png[1] + " " + output
    args = shlex.split(cmd, False, running_on_posix)
    print (args)
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

    nargs = len(sys.argv)
    if nargs != 6 and nargs != 7:
        print ("usage: " + sys.argv[0] +
               " <filename (input)> <res directory (output)> <size> <color> <opacity> [<suffix>]")
        exit(1)

    svg_path = sys.argv[1]
    dir_pngs = sys.argv[2]
    isize = int(sys.argv[3])
    color = sys.argv[4]
    opacity = float(sys.argv[5])

    suffix = ""
    if nargs == 7:
        suffix = sys.argv[6]

    svg_name = os.path.basename(svg_path)
    name = svg_name
    if svg_name.lower().endswith(".svg"):
        name = svg_name[:-4]

    create_images(svg_path, dir_pngs, name, suffix, isize, color, opacity)
