# Creating PNGs from SVG resource

Call this to generate a number of PNG files in the res/drawable-\*
directories of your Android project from a SVG image:

    pngs_from_svg.py <svg file> <independent pixel size> <res dir>

Example:

    pngs_from_svg.py path_to_my/image.svg 32 path_to_my_project/res
