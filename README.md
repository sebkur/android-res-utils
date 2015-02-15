# Creating PNGs from SVG resource

Call this to generate a number of PNG files in the res/drawable-\*
directories of your Android project from a SVG image:

    pngs_from_svg.py <svg file> <res dir> <independent pixel size>
	<color> <opacity> [<suffix>]

Example:

    pngs_from_svg.py path_to_my/image.svg path_to_my_project/res
	32 "#000" 0.54 _light

    pngs_from_svg.py path_to_my/image.svg path_to_my_project/res
	32 "#fff" 1.0 _dark
