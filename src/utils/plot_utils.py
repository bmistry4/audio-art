import numpy as np
from matplotlib import patches
from matplotlib.path import Path


def hex_to_RGB(hex_str):
    """ #FFFFFF -> [255,255,255]"""
    # Pass 16 to the integer function for change of base
    return [int(hex_str[i:i + 2], 16) for i in range(1, 6, 2)]


def get_color_gradient(c1, c2, n):
    """
    Given two hex colors, returns a color gradient
    with n colors.
    """
    assert n > 1
    c1_rgb = np.array(hex_to_RGB(c1)) / 255
    c2_rgb = np.array(hex_to_RGB(c2)) / 255
    mix_pcts = [x / (n - 1) for x in range(n)]
    rgb_colors = [((1 - mix) * c1_rgb + (mix * c2_rgb)) for mix in mix_pcts]
    return ["#" + "".join([format(int(round(val * 255)), "02x") for val in item]) for item in rgb_colors]


def get_alphas(lower, upper, bins):
    return [a for a in np.linspace(lower, upper, bins)]


def switch_off_axes(axs):
    if isinstance(axs, np.ndarray):
        for ax in axs.ravel():
            ax.set_axis_off()
    else:
        axs.set_axis_off()

########################################################################################################################

def plot_patches(theta, radii, widths, colours, axis, alphas, radii_offset=0.):
    # Plot rounded cones using Bézier curves
    for t, r, w, c, a in zip(theta, radii, widths, colours, alphas):
        control_radius = r * 2  # hyperparam; adjust the control point influence
        vertices = [
            (t - w / 2, radii_offset),  # Start point
            (t - w / 2, control_radius),  # Control point 1
            (t + w / 2, control_radius),  # Control point 2
            (t + w / 2, radii_offset),  # End point
        ]
        codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]

        path = Path(vertices, codes)
        patch = patches.PathPatch(path, facecolor=c, edgecolor='none', antialiased=True, alpha=a)
        axis.add_patch(patch)
