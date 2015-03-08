# Creating PNGs from SVG resource

These python scripts take as input an SVG image, replace all black colored
paths with a specified color and opacity, scale it to a specified DP size
and create crunched PNG images from that for the different sizes needed in
the drawable-\* directories of an Android project.

## Different operation modes

There are now two versions of the script. One that replaces certain
color/opacity patterns and another one that manipulates XML and is
tailored to work with the icons from the Material icons repository.

1. The first version looks for color/opacity patterns that specify black
shapes in the SVG and uses text substitution to change the color and opacity
to the user-specified one.

2. The second version parses the SVG using an XML parser, looks for paths
that do not have any color set (the default for relevant shapes in the
Material icons), and adds a fill and opacity attribute for each path.

## Usage from the command line

Call this to generate a number of PNG files in the res/drawable-\*
directories of your Android project from a SVG image:

    pngs_from_svg.py <svg file> <res dir> <independent pixel size>
	<color> <opacity> [<suffix>]

    pngs_from_svg_xml.py <svg file> <res dir> <independent pixel size>
	<color> <opacity> [<suffix>]

Example:

    pngs_from_svg.py path_to_my/image.svg path_to_my_project/res
	32 "#000" 0.54 _light

    pngs_from_svg.py path_to_my/image.svg path_to_my_project/res
	32 "#fff" 1.0 _dark

    pngs_from_svg_xml.py path_to_my/image.svg path_to_my_project/res
	32 "#000" 0.54 _light

    pngs_from_svg_xml.py path_to_my/image.svg path_to_my_project/res
	32 "#fff" 1.0 _dark

## Usage from within python scripts

Make sure to update your PYTHON\_PATH variable:

	export PYTHONPATH=$PYTHONPATH:/path_to/android-res-utils

Import the module:

	import pngs_from_svg as pfs

Or alternatively:

	import pngs_from_svg_xml as pfsx

Then call the function:

	pfs.create_images(svg, res, dest, suffix, isize, color, opacity)

Or alternatively:

	pfsx.create_images(svg, res, dest, suffix, isize, color, opacity)

## Examples

There are some examples in the 'examples' subdirectory that demonstrate
the capabilities of the XML-based scripts. Use the script 'actionbar.py' to
generate some beautiful ActionBar icons directly from Material repository
icons.
