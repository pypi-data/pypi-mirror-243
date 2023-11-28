import matplotlib.pyplot as plt


def plot(*args, **kwargs):
    """Wrapper for pyplot with better defaults.
    """
    fig, ax = plt.subplots(dpi=150)
    ax.plot(*args, **kwargs)
    ax.grid()
    if 'label' in kwargs:
        ax.legend()
    return fig, ax


def multiplot(xx, ydict, styling={}, **kwargs):
    """Plot multiple y values on the same axis.

    Args:
        xx (array): x-axis values.
        ydict (dict[array]): Dictionary of y-values with the keys being the legend labels.
        styling (dict[dict]): Dictionary of additional styling arguments for each y-values.
    """
    fig, ax = None, None
    for k, v in ydict.items():
        if ax is None:
            fig, ax = plot(xx, v, label=k, **styling.get(k, {}), **kwargs)
            continue
        ax.plot(xx, v, **styling.get(k, {}), label=k)
    ax.legend()
    return fig, ax
