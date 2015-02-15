#!/usr/bin/python3

import sys
import os
import shlex
import subprocess
import tempfile
import shutil

DIRS = ["drawable-mdpi", "drawable-hdpi", "drawable-xhdpi", "drawable-xxhdpi"]
SUFFIXES = ["light", "dark"]
# see http://www.google.com/design/spec/style/icons.html#icons-system-icons
# bottom-most section
COLORS = ["#000000", "#ffffff"]
OPACITIES = [0.54, 1.0]


def create_images(svg, namebase):
    for s in range(len(sizes)):
        size = sizes[s]
        output_dir = os.path.join(dir_pngs, DIRS[s])

        if not os.path.isdir(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        for t in range(len(SUFFIXES)):
            suffix = SUFFIXES[t]
            output = os.path.join(output_dir, namebase + "_" + suffix + ".png")
            print (svg + ' -> ' + output)

            tmp_svg = tempfile.mkstemp(".svg")[1]

            f = open(svg, 'r')
            data = f.read()
            f.close()

            data = data.replace(
                "fill=\"#000000\"",
                "fill=\"" + COLORS[t] + "\"")
            data = data.replace(
                "fill-opacity=\"1.0\"",
                "fill-opacity=\"" + str(OPACITIES[t]) + "\"")

            f = open(tmp_svg, 'w')
            f.write(data)
            f.close()

            create_png(tmp_svg, output, size)

            os.remove(tmp_svg)


def create_png(svg, output, size):
    cmd = "inkscape -C -e " + output + " -h " + str(size) + " " + svg
    args = shlex.split(cmd)
    subprocess.call(args)

    tmp_png = tempfile.mkstemp(".png")[1]
    shutil.copyfile(output, tmp_png)

    cmd = "pngcrush " + tmp_png + " " + output
    args = shlex.split(cmd)
    print (args)
    subprocess.call(args)

    os.remove(tmp_png)

if __name__ == "__main__":

    if len(sys.argv) != 4:
        print ("usage: " + sys.argv[0] +
               " <filename (input)> <size> <res directory (output)>")
        print (len(sys.argv))
        exit(1)

    svg_path = sys.argv[1]
    isize = int(sys.argv[2])
    dir_pngs = sys.argv[3]

    # dimensions for mdpi/hdpi/xhdpi/xxhdpi
    sizes = [isize, isize * 1.5, isize * 2, isize * 3]

    svg_name = os.path.basename(svg_path)
    name = svg_name
    if svg_name.lower().endswith(".svg"):
        name = svg_name[:-4]

    create_images(svg_path, name)
