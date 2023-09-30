# Opaque_Set

*NOTE: "Total Remaining Grey" refers to the area of the grey remaining on the first two graphs, NOT to the area of the figure in the bottom graph.

These programs are tools to analyze opaque sets.
(No curves allowed)

The "no_plot" version is bare bones, meant to show only the total length of line segments and their effectivity at covering a given region. It is best paired with something like a neural network.

The other version is more interactive and informative.

There are 3 plots shown when running opaque.py. The first two both show what lines go through the given area and the coverage lines. The first graph shows the lines y = mx + b of interest only for -1 <= m <= 1. Any point on the graph within the grey area is a point that describes a line that passes through the area. The second graph switches all values x and y that describe the area and the line segments. Then it does the same as the first, finding the y = mx + b lines of interest only for -1 <= m <= 1. This covers every possible line that could pass through the area. The colored area (blue on the left, red on the right) shows the lines that pass through the barriers. A set is opaque if the grey area is covered by the colored region entirely on both graphs. The "Total Remaining Area" refers to the amount of grey that is left uncovered in both graphs. The size of this area describes the amount of lines that are able to pass through, so this value is returned for the sake of understanding how close it is to being opaque. The total combined length of all barriers is also calculated. These two values are the only things returned by the "no_plot" version, as these would be the values of interest for training data with large sets. Since the total remaining area is calculated purely with geometry, it runs fairly fast. Any changes may be made to make this program more efficient.

[![DOI](https://zenodo.org/badge/698029054.svg)](https://zenodo.org/badge/latestdoi/698029054)
