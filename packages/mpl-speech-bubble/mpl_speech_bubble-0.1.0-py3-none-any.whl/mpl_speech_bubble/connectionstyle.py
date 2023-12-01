import matplotlib.transforms as mtransforms
from matplotlib.path import Path
from matplotlib.patches import ConnectionStyle

# define new connectionstyle

class Bubble(ConnectionStyle._Base):
    """
    Connect the point and the closest point on the bbox of the text.
    """

    def __init__(self, text, shrink_w=0.05, shrink_h=0.05):
        """
        Parameters
        ----------
        rad : float
          Curvature of the curve.
        """
        self._text = text
        self._shrink_w = shrink_w
        self._shrink_h = shrink_h

    def connect(self, posA, posB):
        x1, y1 = posA
        x2, y2 = posB

        # cx, cy = x2, y1

        from matplotlib.text import _get_textbox
        renderer = self._text.figure.canvas.renderer

        x_box, y_box, w_box, h_box = _get_textbox(self._text, renderer)

        # posA is center of the textbox, regardless of the va or ha.
        # On the other hand, x_box is 0 for va=left, -0.5*w for va=center, for example.
        # So, posB should be rotated around the anchor(respecting va and ha), not around posA.

        a = self._text.get_rotation()
        tr = mtransforms.Affine2D().rotate_deg(-a)

        dx, dy = tr.inverted().transform_point([-0.5*w_box, -0.5*h_box])
        x0 = x1 + dx - x_box
        y0 = y1 + dy - y_box

        # print(x_box, y_box, x0, y0)
        x_boxt, y_boxt = tr.transform_point([x_box, y_box])
        x2t, y2t = tr.transform_point([x2-x0, y2-y0])

        dw = w_box * self._shrink_w
        dh = h_box * self._shrink_h

        cxt = sorted([x_boxt+dw, x_boxt+w_box-2*dw, x2t])[1]
        cyt = sorted([y_boxt+dh, y_boxt+h_box-2*dh, y2t])[1]

        cx, cy = tr.inverted().transform_point([cxt, cyt]) + (x0, y0)

        # vertices = [(x1, y1),
        #             (cx, cy),
        #             (x2, y2)]
        # codes = [Path.MOVETO,
        #          Path.LINETO,
        #          Path.LINETO]
        vertices = [(cx, cy),
                    (0.5*(cx+x2), 0.5*(cy+y2)),
                    (x2, y2)]
        codes = [Path.MOVETO,
                 Path.CURVE3,
                 Path.CURVE3]

        return Path(vertices, codes)

    def __call__(self, posA, posB,
                 shrinkA=2., shrinkB=2., patchA=None, patchB=None):
        return super().__call__(posA, posB, shrinkA, shrinkB, patchA, patchB)

# Bubble connection sytle reuiqres Text instance as its first argument, and it
# is not useful to add it to ConnectionStyle._style_list.
