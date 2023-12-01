"""
Methods related to colors.
"""
from typing import Sequence

import numpy as np
from matplotlib.colors import to_hex, to_rgb


def fader(color1: str, color2: str, fraction: float) -> str:
    """
    Returns a color that is partway between two other colors.

    Parameters:
    color1 - Starting color in hex, e.g. #000000
    color2 - Ending color in hex, e.g. #ffffff
    fraction - Float between 0 and 1 representing how far from `color1` the output color
        should be. At the extremes, if `fraction=0`, then we return `color1` and if
        `fraction=1`, then we return `color2`.
    """
    color1 = np.array(to_rgb(color1))
    color2 = np.array(to_rgb(color2))
    return to_hex((1 - fraction) * color1 + fraction * color2)


def multifader(colors: Sequence[str], fractions: Sequence[float]) -> Sequence[str]:
    """
    Allows for fading between mutliple, equally-spaced colors. Returns a list of colors
    whose length is equal to that of `fracs` using the function `fader`.

    Parameters:
    colors - A list of colors that are considered equally spaced, e.g. if
        `colors=["#ffffff", "#ff0000", "000000"]` then the total spectrum will shift
        from white (at 0.0) to red (at 0.5) to black (at 1.0).
    fracs - A list of floats from 0 to 1 in ascending order representing at which point
        one wants to sample a point, e.g. using the above example and
        `fader=[0.3, 0.5, 0.9]` then this returns:
            ['#ff6666', '#ff0000', '#cc0000', '#330000']
        The second color is the 1st element of `colors` since its corresponding `fracs`
        value was 0.5.
    """
    output_colors = []
    # Get evenly spaced fractions for each color
    color_fracs = np.linspace(0, 1, len(colors))

    for frac in fractions:
        # If the frac matches with a color, just use that color
        if frac in color_fracs:
            color = colors[np.where(color_fracs == frac)[0][0]]
        else:
            # Find which colors the fraction is inbetween
            frac_ind = np.searchsorted(color_fracs, frac)
            # Find the fraction it is between those two colors
            internal_frac = (frac - color_fracs[frac_ind - 1]) / (
                color_fracs[frac_ind] - color_fracs[frac_ind - 1]
            )
            # Get the color
            color = fader(
                color1=colors[frac_ind - 1],
                color2=colors[frac_ind],
                fraction=internal_frac,
            )

        output_colors.append(color)

    return output_colors
