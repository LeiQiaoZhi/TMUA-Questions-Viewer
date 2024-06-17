import matplotlib.pyplot as plt
from matplotlib.colors import to_hex

PADDING = 6
FILTER_FRAME_GRID_OPTIONS = {"padx": 0, "pady": 4, "sticky": "nsew"}
FONT = "Merriweather"

CMAP = "viridis"


def get_hex_colors_from_cmap(cmap_name, num_colors):
    # Get the colormap
    cmap = plt.get_cmap(cmap_name)

    # Generate evenly spaced values between 0 and 1
    values = [i / num_colors for i in range(num_colors)]

    # Get the hex colors
    hex_colors = [to_hex(cmap(value)) for value in values]

    return hex_colors
