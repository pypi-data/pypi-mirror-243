"""
Methods related to plotting, regarding matplotlib.
"""
from math import gcd
from typing import Optional, Sequence, Union

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.ticker import FixedLocator, MultipleLocator

LABEL_TYPES = [None, "explicit"]


def cumulative_bins(*arrs: Sequence[float], num_bins: int) -> Sequence[float]:
    """
    Will return an array to be used in a matplotlib histogram for the keyword `bins`.
    If you are plotting multiple histograms on the same plot, their bin width won't
    necessarily be the same size. Pass them to this method along with the total number
    of bins to rectify that.

    Parameters:
    arrs - The data that will be plotted in the histogram
    num_bins - The total number of bins
    """
    return np.histogram(np.hstack(arrs), bins=num_bins)[2]


def log_bins(*arrs: Sequence[float], num_bins: int) -> Sequence[float]:
    """
    Will return an array to be used in a matplotlib histogram for the keyword `bins`.
    These bins will have equal width in log space and, like `tot_bins`, can be passed
    multiple sets of data or just one.

    Parameters:
    arrs - The data that will be plotted in the histogram
    num_bins - The total number of bins
    """
    all_data = np.hstack(arrs)
    return np.geomspace(np.min(all_data), np.max(all_data), num_bins)


def bar_count(
    ax: plt.Axes,
    counts: Union[dict[str, float], Sequence[float]],
    labels: Optional[str] = None,
    label_bars: bool = False,
    sort_type: Optional[str] = None,
    *,
    bar_params: Optional[dict[str, ...]] = None,
    **kwargs: ...,
) -> plt.Axes.bar:
    """
    Creates a bar plot given values and labels. The parameter `counts` can be either a
    dictionary or a list (of values).

    Parameters:
    ax - Matplotlib axis to plot on
    counts - Dictionary of form {label: value} or a list of values
    labels (default None) - Optional list of labels. If specified, `counts` should then
        also be a list. If not specified, then `counts` should be a dictionary.
    label_bars (default False) - If True, each bar will be labeled with its value shown
        on top of the bar.
    sort_type (default None) - How to sort the bars. By default, it won't sort. Can be
        'asc' for sort ascending (smallest to largest value left to right) or 'desc' for
        descending.
    bar_params (default {}) - A dictionary of keywords to be specifically passed to
        `ax.bar`.
    kwargs - Other keywords used in the plot. They (with their defaults) are:
        label_fmt (default "{:.2f}") - The string format for the bar label
        ylabel (default "") - The label of the y axis
        xlabel (default "") - The label of the x axis
        ylabel_fs (default 13) - Fontsize of the y axis label
        xlabel_fs (default 13) - Fontsize of the x axis label
        title (default "") - The title of the plot
        title_fs (default 18) - The fontsize of the plot
        x_rot (default 45) - Degree angle to rotate the x axis bar labels
            counterclockwise from horizontal
    """
    # Make sure `counts` and `labels` play nicely together
    if labels is not None:
        if not isinstance(counts, (list, tuple, np.ndarray)):
            raise TypeError(
                "If `labels` is defined, then `counts` should be a list-type object, "
                f"not a {type(counts)} object."
            ) from None
        if not isinstance(labels, (list, tuple, np.ndarray)):
            raise TypeError(
                "If `labels` is defined, then it should be a list-type object, "
                f"not a {type(labels)} object."
            ) from None
        if len(counts) != len(labels):
            raise IndexError(
                "If `labels` is defined, then it should be an equal length to `counts`."
                f" Current lengths are {len(counts)=} and {len(labels)=}."
            ) from None
        values = counts
    else:
        values = list(counts.values())
        labels = list(counts.keys())

    # Sort data if needed
    if sort_type is not None:
        if sort_type not in {"asc", "desc"}:
            raise ValueError(
                f"`sort_type` should be either 'desc' or 'asc', not {sort_type}."
            )
        values, labels = zip(
            *sorted(
                zip(values, labels), key=lambda x: x[0], reverse=sort_type == "desc"
            )
        )

    bar_params = bar_params if bar_params is not None else {}
    bar = ax.bar(labels, values, **bar_params)
    # Label the top of each bar with its value?
    if label_bars:
        ax.bar_label(bar, fmt=kwargs.get("label_fmt", "{:.2f}"))
    ax.set_ylabel(kwargs.get("ylabel", ""), fontsize=kwargs.get("ylabel_fs", 13))
    ax.set_xlabel(kwargs.get("xlabel", ""), fontsize=kwargs.get("xlabel_fs", 13))
    ax.set_title(kwargs.get("title", ""), fontsize=kwargs.get("title_fs", 18))
    ax.tick_params(axis="x", rotation=kwargs.get("x_rot", 45))

    return bar


def histbar(
    ax: Axes,
    xs: Sequence[float],
    ys: Sequence[float],
    label_type: Optional[str] = None,
    capends: bool = True,
    fill: bool = False,
    **kwargs: ...,
) -> None:
    """
    Creates histogram for a set of y-values representing each bin. This is very similar
    to matplotlib's `step` method. That is, I made this before I realized that
    existed. Granted, this method allows for more customization, e.g. spacing-filling,
    so this method will continue to exist.

    Parameters:
    ax - Axis object to display plot on.
    xs - X data.
    ys - Y data, should be a length one less than `xs` since `xs` represents the limits
        of each vlaue of `ys`.
    label_type (default "all") - How to label the x-axis. By default, None will not
        touch the ticks at all. And "explicit" will explicitly label each value of `xs`
        and try to set the minor ticks by the greatest difference between the values of
        `xs`. This minor tick value can be specified below.
    cap_ends (default True) - If True, will create vertical lines at each end of the
        plot. This will, by default, go to a y-value of 0 but can be specified below. If
        False, will not cap the ends.
    fill (default False) - If True, will fill in the plot between the line specified
        by `xs` and `ys` and a specified value below (default 0). If False, there will
        not be any fill.
    kwargs - The following keywords can be specified:
        color (default "#000000") - The color of the line
        lw (default 2)- The linewidth of the line
        ls (default "solid") - The linestyle of the line
        alpha (default 1) - The transparency of the line (between 0 and 1)
        capends_ymin (default 0) - If `capends=True`, then a vertical line between y[0]
            and capends_ymin will be created along with one between y[-1] and
            capends_ymin.
        label_type_minor_locator - Distance between minor ticks. Default is dynamic, it
            will try to find the greatest distance between major ticks and use that.
        fill_color (default "#ffffff") - Color of the fill.
        fill_hatch (default None) - Hatch type of the fill.
        fill_alpha (default 1) - Transparency of the fill.
        fill_limit (default 0) - Maximum/Minimum value of the fill. It is maximum if it
            is larger than `max(ys)` and is minimum if it is less than `min(ys)`.
            Otherwise it does something silly.
    """
    # Make sure our `label_type` variable is valid
    if label_type not in LABEL_TYPES:
        raise ValueError(
            f'`label_type` is "{label_type}". Should be one of the following: '
            f"{', '.join(LABEL_TYPES)}."
        ) from None

    # `xs` define endpoints of each value in `ys`, hence it should be one longer
    if len(ys) != len(xs) - 1:
        raise ValueError(
            f"Length of `ys` should be {len(xs) - 1} but is instead {len(ys)}."
        )

    # Setting up xaxis
    match label_type:
        case None:
            pass
        case "explicit":
            # Explicitly label every x point and try to guess at minor locators
            ax.xaxis.set_major_locator(FixedLocator(xs))
            minor_locator = kwargs.get("label_type_minor_locator")
            if minor_locator is None:
                # If minor locator (as a multiple) isn't specified, try to find
                # maximum value of difference between points
                xs_diff = np.diff(xs)
                xs_diff_min = np.min(xs_diff)
                minor_locator = gcd(*(xs_diff / xs_diff_min).astype(int)) * xs_diff_min
            ax.xaxis.set_minor_locator(MultipleLocator(minor_locator))

    # Intialize this variable if fill == True
    if fill:
        prev_ymax = 2 * len(ys) * [kwargs.get("fill_limit", 0)]

    # Actually plotting data
    for ind in range(len(ys)):
        y = ys[ind]
        xmin = xs[ind]
        xmax = xs[ind + 1]

        ax.hlines(
            y=y,
            xmin=xmin,
            xmax=xmax,
            lw=kwargs.get("lw", 2),
            ls=kwargs.get("ls", "solid"),
            color=kwargs.get("color", "#000000"),
            alpha=kwargs.get("alpha", 1),
        )

        if ind < len(xs) - 2:
            ymax = ys[ind + 1]
            ax.vlines(
                x=xmax,
                ymin=y,
                ymax=ymax,
                lw=kwargs.get("lw", 2),
                ls=kwargs.get("ls", "solid"),
                color=kwargs.get("color", "#000000"),
                alpha=kwargs.get("alpha", 1),
            )

        # Filling in area above (or below) line depending on `fill_limit``
        if fill:
            ax.fill_between(
                x=np.repeat(xs, 2)[1:-1],
                y1=prev_ymax,
                y2=np.repeat(ys, 2),
                color=kwargs.get("fill_color", "#ffffff"),
                hatch=kwargs.get("fill_hatch", None),
                alpha=kwargs.get("fill_alpha", 1),
            )
            prev_ymax = np.repeat(ys, 2)

    # Vertically cap ends of data
    if capends:
        ax.vlines(
            x=xs[0],
            ymin=kwargs.get("capends_ymin", 0),
            ymax=ys[0],
            lw=kwargs.get("lw", 2),
            ls=kwargs.get("ls", "solid"),
            color=kwargs.get("color", "#000000"),
            alpha=kwargs.get("alpha", 1),
        )
        ax.vlines(
            x=xs[-1],
            ymin=ys[-1],
            ymax=kwargs.get("capends_ymin", 0),
            lw=kwargs.get("lw", 2),
            ls=kwargs.get("ls", "solid"),
            color=kwargs.get("color", "#000000"),
            alpha=kwargs.get("alpha", 1),
        )
