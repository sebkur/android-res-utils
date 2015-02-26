#!/usr/bin/python3

import sys
import os
import shlex
import subprocess
import tempfile
import shutil

DIRS = ["drawable-mdpi", "drawable-hdpi", "drawable-xhdpi", "drawable-xxhdpi"]


def create_images(svg, namebase):
    for s in range(len(sizes)):
        size = sizes[s]
        output_dir = os.path.join(dir_pngs, DIRS[s])

        if not os.path.isdir(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        output = os.path.join(output_dir, namebase + suffix + ".png")
        print (svg + ' -> ' + output)

        tmp_svg = tempfile.mkstemp(".svg")
        os.close(tmp_svg[0])

        f = open(svg, 'r')
        data = f.read()
        f.close()

        data = data.replace( \
            "style=\"fill:#000000;opacity:1\"",
            "style=\"fill:" + color + ";opacity:" + str(opacity) + "\"")
        data = data.replace( \
            "style=\"opacity:1;fill:#000000\"",
            "style=\"opacity:" + str(opacity) + ";fill:" + color + "\"")
        data = data.replace(
            "fill=\"#000000\"",
            "fill=\"" + color + "\"")
        data = data.replace(
            "style=\"fill:#000000\"",
            "style=\"fill:" + color + "\"")
        data = data.replace(
            "fill-opacity=\"1.0\"",
            "fill-opacity=\"" + str(opacity) + "\"")

        f = open(tmp_svg[1], 'w')
        f.write(data)
        f.close()

        create_png(tmp_svg[1], output, size)

        os.remove(tmp_svg[1])


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

if __name__ == "__main__":

    running_on_posix = is_posix()

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
    
    suffix = "";
    if nargs == 7:
        suffix = sys.argv[6]

    # dimensions for mdpi/hdpi/xhdpi/xxhdpi
    sizes = [isize, isize * 1.5, isize * 2, isize * 3]

    svg_name = os.path.basename(svg_path)
    name = svg_name
    if svg_name.lower().endswith(".svg"):
        name = svg_name[:-4]

    create_images(svg_path, name)
