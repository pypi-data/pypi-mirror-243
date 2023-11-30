import numpy as np
import json
from matplotlib.path import Path
from matplotlib.transforms import Bbox, TransformedBbox, Affine2D
import matplotlib.colors as mcolors
from matplotlib.backend_bases import RendererBase

from matplotlib.artist import Artist
from mpl_visual_context.transform_helper import TR
from mpl_visual_context.patheffects_base  import AbstractPathEffect

DEFAULT_COLOR_CYCLE = [f"C{i}" for i in range(10)]

class FillPattern(AbstractPathEffect):
    """
    Fill the path with the given pattern.
    """

    def __init__(self, pattern, ax, color_cycle=None, alpha=None):
        """

        Keyword Arguments:

        alpha: alpha value for the pattern. If None, the alpha value from the parent artist
               will be used.
        """

        self.pb = PatternBox(pattern, extent=None, bbox=None, coords="figure pixels", axes=ax,
                             color_cycle=color_cycle)
        self._alpha = alpha

    def draw_path(self, renderer, gc, tpath, affine, rgbFace):

        bbox = tpath.get_extents(affine)
        self.pb.set_bbox(bbox)
        self.pb.set_clip_path(tpath, transform=affine)
        self.pb.set_alpha(gc.get_alpha() if self._alpha is None else self._alpha)
        self.pb.draw(renderer)
        # FIXME we may better recover the clip_path?

        renderer.draw_path(gc, tpath, affine, None)


class Pattern:
    def __init__(self, width, height, pathlist, scale=1):
        self.width = width*scale
        self.height = height*scale
        self.pathlist = [type(p)(vertices=p.vertices*scale,
                                 codes=p.codes) for p in pathlist]

    def fill(self, ax, color_cycle=None, alpha=None):
        if color_cycle is not None:
            # We cache the colors in case color_cycle is a generator.
            color_cycle = [c for _, c in zip(self.pathlist, color_cycle)]

        return FillPattern(self, ax,
                           color_cycle=color_cycle, alpha=alpha)


class PatternBox(Artist):
    def _get_bbox_orig(self, extent, bbox):
        """
        Returns a bbox from the extent if extent is not None, otherwise
        returns a bbox itself. If both are None, return s unit bbox.
        """

        if bbox is not None:
            if extent is not None:
                raise ValueError("extent should be None if bbox is given")
            bbox_orig = bbox
        else:
            if extent is None:
                extent = [0, 0, 1, 1]
            bbox_orig = Bbox.from_extents(extent)

        return bbox_orig

    def set_bbox(self, bbox):
        self.bbox = bbox
        self.bbox_orig = self._get_bbox_orig(self.extent, bbox)

    def set_extent(self, extent):
        self.extent = extent
        self.bbox_orig = self._get_bbox_orig(extent, self.bbox)

    default_color_cycle = DEFAULT_COLOR_CYCLE

    def __init__(self, pattern, extent=None, bbox=None, coords="data", axes=None,
                 color_cycle=None,
                 **artist_kw):
        super().__init__(**artist_kw)
        self.pattern = pattern
        self.extent = extent
        self.bbox = bbox
        self.bbox_orig = self._get_bbox_orig(extent, bbox)
        self.coords = coords
        self.axes = axes
        if axes is not None:
            self.set_clip_path(axes.patch)

        self.color_cycle = self.default_color_cycle if color_cycle is None else color_cycle

    def draw(self, renderer):
        if not self.get_visible():
            return

        gc = renderer.new_gc()
        self._set_gc_clip(gc)
        gc.set_alpha(self.get_alpha())
        gc.set_url(self.get_url())

        tr = TR.get_xy_transform(renderer, self.coords, axes=self.axes)
        if callable(self.bbox_orig):
            bbox_orig = self.bbox_orig(renderer)
        else:
            bbox_orig = self.bbox_orig
        trbox = TransformedBbox(bbox_orig, tr)
        x0, y0 = trbox.x0, trbox.y0

        w = self.pattern.width
        h = self.pattern.height

        nx = int(trbox.width // w + 1)
        ny = int(trbox.height // h + 1)

        offsets = [(x0+w*ix, y0+h*iy) for ix in range(nx) for iy in range(ny)]
        for p, fc in zip(self.pattern.pathlist, self.color_cycle):

            rgb = mcolors.to_rgb(fc)

            # FIXME: for now, the pattern will be drawn in the pixel
            # coordinate, so the pattern will be dependent of dpi used.

            _transforms = np.zeros((1, 3, 3))
            _transforms[0, 0, 0] = 1
            _transforms[0, 1, 1] = 1

            kl = (gc, Affine2D().frozen(), [p] * len(offsets),
                  _transforms, # all trans
                  np.array(offsets),
                  Affine2D().frozen(), # offset trans
                  np.array([rgb]), [], # face & edge
                  [], [], # lw, ls
                  [], [], #
                  None)
            RendererBase.draw_path_collection(renderer, *kl)
            # renderer.draw_path_collection(*kl) # FIXME: this fails with ValueError
            # (Expected 2-dimensional array, got 1). Could not figure out why.

        gc.restore()


class PatternMonster:
    def __init__(self):

        import pkg_resources

        fn_json = pkg_resources.resource_filename('mpl_pe_pattern_monster',
                                                  'pattern_monster_wo_path.json')
        fn_npz = pkg_resources.resource_filename('mpl_pe_pattern_monster',
                                                 'pattern_monster_vertcies_codes.npz')

        self._j = json.load(open(fn_json))
        self._vc = np.load(fn_npz)

        slugs = dict()
        tags = {}
        roots = {}
        names = []
        for j1 in self._j:
            slug = j1["slug"]
            slugs[slug] = j1
            for tag in j1["tags"]:
                tags.setdefault(tag.strip(), []).append(slug)
            root = slug.split("-")[0]
            roots.setdefault(root, []).append(slug)
            names.append(slug)

        self._slugs, self.roots, self.tags, self.names = slugs, roots, tags, names

    def get(self, slug, scale=1):
        "return an instance of pattern of a given slug name."
        j1 = self._slugs[slug]

        slug = j1["slug"].replace("-", "_")
        npath = j1["npath"]

        path_list = []
        for i in range(npath):
            kc = f"{slug}_c{i}"
            kv = f"{slug}_v{i}"

            codes = self._vc[kc]
            vertices = self._vc[kv]

            p = Path(vertices=vertices, codes=codes)
            path_list.append(p)

        w, h = j1["width"], j1["height"]

        return Pattern(w, h, path_list, scale=scale)


def test_plot():
    import matplotlib.pyplot as plt
    from matplotlib.text import TextPath
    from matplotlib.patches import PathPatch
    import mpl_visual_context.patheffects as pe

    pm = PatternMonster()
    pattern = pm.get(pm.names[2])

    fig, ax = plt.subplots(num=1, clear=True)
    ax.set_aspect(1)
    p = TextPath((0, 0), "M", size=40)
    patch = PathPatch(p, ec="k", transform=ax.transData, fc="0.9")
    ax.add_patch(patch)

    patch.set_path_effects([pe.FillOnly(),
                            pattern.fill(ax),
                            ])

    ax.set(xlim=(0, 40), ylim=(-5, 32))

    plt.show()


if __name__ == '__main__':
    test_plot()
