import logging
import numpy as np
import matplotlib.patches as mpatches

from matplotlib.text import Text, Annotation
import matplotlib.transforms as mtransforms

_log = logging.getLogger(__name__)

# from .mpl_pathops import mpl2skia, skia2mpl, union
from mpl_skia_pathops import mpl2skia, skia2mpl, union

# from matplotlib.path import Path
# from matplotlib.patches import ConnectionStyle, BoxStyle

from .connectionstyle import Bubble

class AnnotationMergedPatch(Annotation):
    def __init__(self, *kl, **kwargs):
        super().__init__(*kl, **kwargs)

    def _get_bbox_patch_path(self, renderer):

        # copied from Text.draw
        with self._cm_set(text=self._get_wrapped_text()):
            bbox, info, descent = self._get_layout(renderer)
            trans = self.get_transform()

            # don't use self.get_position here, which refers to text
            # position in Text:
            posx = float(self.convert_xunits(self._x))
            posy = float(self.convert_yunits(self._y))
            posx, posy = trans.transform((posx, posy))
            if not np.isfinite(posx) or not np.isfinite(posy):
                _log.warning("posx and posy should be finite values")
                return None, None

            # Update the location and size of the bbox
            # (`.patches.FancyBboxPatch`), and draw it.
            if self._bbox_patch:
                self.update_bbox_position_size(renderer)
                # self._bbox_patch.draw(renderer)
                return (self._bbox_patch.get_path(),
                        self._bbox_patch.get_transform())
                        # self._bbox_patch.get_patch_transform())
            else:
                return None, None


    def draw(self, renderer):
        # docstring inherited
        if renderer is not None:
            self._renderer = renderer
        if not self.get_visible() or not self._check_xy(renderer):
            return
        # Update text positions before `Text.draw` would, so that the
        # FancyArrowPatch is correctly positioned.
        self.update_bbox_position_size(renderer)
        self.update_positions(renderer)
        if self.arrow_patch is not None:  # FancyArrowPatch
            if self.arrow_patch.figure is None and self.figure is not None:
                self.arrow_patch.figure = self.figure

            p1, t1 = self._get_bbox_patch_path(renderer)
            self.arrow_patch._dpi_cor = renderer.points_to_pixels(1.)
            p2, t2 = (self.arrow_patch.get_path(),
                      self.arrow_patch.get_patch_transform())
            s1 = mpl2skia(p1, t1)
            s2 = mpl2skia(p2, t2)

            u = union(s1, s2)
            p12 = skia2mpl(u)

            patch = mpatches.PathPatch(p12, facecolor='w', ec="k")

            patch.update_from(self._bbox_patch)
            patch.set_visible(True)
            patch.set_transform(mtransforms.IdentityTransform())
            patch.draw(renderer)

        # Draw text, including FancyBboxPatch, after FancyArrowPatch.
        # Otherwise, a wedge arrowstyle can land partly on top of the Bbox.
        # self.text_draw(renderer)
        if self._bbox_patch is not None:
            self._bbox_patch.set_visible(False)

        Text.draw(self, renderer)


class AnnotationBubble(AnnotationMergedPatch):
    def __init__(self, text, xy, loc="down", dist=1.5, rotation=0, dx=None, xytext=None,
                 rotation_mode="anchor",
                 arrowstyle="wedge", shrinkB=5,
                 textcoords=None, ha=None, va=None, bbox=None, arrowprops=None, **kwargs):

        bbox = bbox if bbox is not None else dict(boxstyle="round, pad=0.2",
                                                  fc="none", ec="k")
        arrowprops = arrowprops if arrowprops is not None else dict(arrowstyle=arrowstyle,
                                                                    patchA=None, shrinkB=shrinkB)

        super().__init__(text, xy, bbox=bbox, arrowprops=arrowprops,
                         xytext=(0, 1.5), textcoords="offset fontsize", ha="center",
                         rotation_mode=rotation_mode, **kwargs)
        _dx, dy = (None, None) if xytext is None else xytext
        dx = dx if _dx is None else _dx
        self.set_loc(loc, dist, ha=ha, va=va, dx=dx, dy=dy, rotation=rotation,
                     textcoords=textcoords)

        if "connectionstyle" not in arrowprops:
            self.arrow_patch.set_connectionstyle(
                Bubble(self)
            )

    def set_loc(self, loc, offset, ha=None, va=None, textcoords=None, 
                dx=None, dy=None, rotation=None):

        _ha, _va, _dx, _dy = dict(down=("center", "top", 0, -offset),
                                  up=("center", "bottom", 0, offset),
                                  right=("left", "center", offset, 0),
                                  left=("right", "center", -offset, 0))[loc]

        textcoords = "offset fontsize" if textcoords is None else textcoords
        self.set_anncoords(textcoords)

        ha = _ha if ha is None else ha
        va = _va if va is None else va
        dx = _dx if dx is None else dx
        dy = _dy if dy is None else dy

        if rotation is None:
            rotation = self.get_rotation()
        else:
            self.set_rotation(rotation)

        tr = mtransforms.Affine2D().rotate_deg(rotation)
        self.xyann = tr.transform_point((dx, dy))
        self.set_rotation(rotation)
        self.set_ha(ha)
        self.set_va(va)


def annotate_merged(ax, text, xy, xytext=None, xycoords='data',
                    textcoords=None,
                    arrowprops=None, annotation_clip=None, **kwargs):
    # Signature must match Annotation. This is verified in
    # test_annotate_signature().
    a = AnnotationMergedPatch(text, xy, xytext=xytext, xycoords=xycoords,
                              textcoords=textcoords, arrowprops=arrowprops,
                              annotation_clip=annotation_clip, **kwargs)
    a.set_transform(mtransforms.IdentityTransform())
    if 'clip_on' in kwargs:
        a.set_clip_path(ax.patch)
    ax._add_text(a)
    return a


def annotate_bubble(ax, text, xy, loc="down", dist=1.5, xycoords='data',
                    arrowprops=None, annotation_clip=None, **kwargs):
    """
    Use loc and dist instead of xytext and textcoords.
    """
    assert "xytext" not in kwargs
    assert "textcoords" not in kwargs

    a = AnnotationBubble(text, xy, loc=loc, dist=dist, xycoords=xycoords,
                              arrowprops=arrowprops,
                              annotation_clip=annotation_clip, **kwargs)
    a.set_transform(mtransforms.IdentityTransform())
    if 'clip_on' in kwargs:
        a.set_clip_path(ax.patch)
    ax._add_text(a)
    return a

