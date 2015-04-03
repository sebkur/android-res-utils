# Creating PNGs from SVG resource

These python scripts take as input an SVG image, replace paths with a
specified color and opacity, scale it to a specified DP size
and create crunched PNG images from that for the different sizes needed in
the drawable-\* directories of an Android project.

## Usage from the command line

Call this to generate a number of PNG files in the res/drawable-\*
directories of your Android project from a SVG image:

    pngs_from_svg.py <svg file> <res dir> <independent pixel size>
                     [--color <color>] [--opacity <opacity>] [--suffix <suffix>] [--nopngcrush]

or use the help command to display a list of options:

    pngs_from_svg.py --help
 
Example usage:

    pngs_from_svg.py path_to_my/image.svg path_to_my_project/res 32
    --color "#000" --opacity 0.54 --suffix _light

    pngs_from_svg.py path_to_my/image.svg path_to_my_project/res 32
	--color "#fff" --opacity 1.0 --suffix _dark

## Usage from within python scripts

Make sure to update your PYTHON\_PATH variable:

	export PYTHONPATH=$PYTHONPATH:/path_to/android-res-utils

Import the module:

	import pngs_from_svg as pfs

Then call the function:

	pfs.create_images(svg, res, dest, suffix, isize, color, opacity)

## Examples

There are some examples in the 'examples' subdirectory that demonstrate
the capabilities of this script. Use the script 'actionbar.py' to
generate some beautiful ActionBar icons directly from svg files (including some
icons from the Material repository).
