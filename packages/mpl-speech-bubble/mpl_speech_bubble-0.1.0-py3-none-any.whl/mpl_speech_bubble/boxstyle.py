from matplotlib.path import Path
from matplotlib.patches import BoxStyle

# define new boxstyle

class FixedCircle(BoxStyle.Circle):
    """A circular box whose size is fixed (only scales with fontsize)."""

    def __init__(self, scale=1, pad=0.3):
        """
        Parameters
        ----------
        scale : float, default 1
        pad : float, default: 0.3
            The amount of padding around the original box.
        """
        self.scale = scale
        self.pad = pad


    def __call__(self, x0, y0, width, height, mutation_size):
        return Path.circle((x0 + width / 2, y0 + height / 2),
                            mutation_size*(0.5*self.scale+self.pad))

BoxStyle._style_list["fixed_circle"] = FixedCircle


class FixedSquare(BoxStyle.Square):
    """A square box whose size is fixed (only scales with fontsize)."""

    def __init__(self, scale=1, pad=0.3):
        """
        Parameters
        ----------
        scale : float, default 1
        pad : float, default: 0.3
            The amount of padding around the original box.
        """
        self.scale = scale
        self.pad = pad

    def __call__(self, x0, y0, width, height, mutation_size):
        pad = mutation_size * (0.5*self.scale + self.pad)
        x0 = x0 + width * 0.5
        y0 = y0 + height * 0.5
        x1, y1 = x0 - pad, y0 - pad
        x2, y2 = x0 + pad, y0 + pad
        return Path._create_closed(
            [(x1, y1), (x2, y1), (x2, y2), (x1, y2)])

BoxStyle._style_list["fixed_square"] = FixedSquare

