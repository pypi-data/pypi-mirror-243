import json
import xml.etree.ElementTree as ET
import cairosvg
from picosvg.svg import SVG
import svgpath2mpl
import numpy as np
import re

# 'h' in path data is ignored by cairosvg

# p_namespace = re.compile(r'xmlns="[^"]+"')
p_namespace = re.compile(r"xmlns=\"[^\"]+\"")
# p_namespace_xlink = re.compile(r'xmlns\:xlink="[^"]+"')

def remove_ns(xmlstring):
    xmlstring = p_namespace.sub('', xmlstring, count=1)
    # xmlstring = p_namespace_xlink.sub('xmlns:xlink="xlink"', xmlstring, count=1)
    return xmlstring

def _convert_path(svg_string, slug=None):
    # 2. We process the svg file with cairosvg.
    k = cairosvg.svg2svg(svg_string)

    do_pico = True

    # 3. We process the result with picosvg.
    from itertools import count
    i = count() # incase slug name is not provided.
    if do_pico:
        svg = SVG.fromstring(k)
        svg.topicosvg(inplace=True)
        try:
            svg.clip_to_viewbox(inplace=True)
        except:
            fnroot = f"test{next(i)}" if slug is None else slug
            fn = f"{fnroot}.svg"
            output = svg.tostring(pretty_print=False)
            output = output.replace('</svg>',
                                    '<rect width="100%" height="100%" fill="red"/></svg>')
            open(fn, "w").write(output)
            print(f"path saved as {fn}")
            raise

        output = svg.tostring(pretty_print=False)
        k = output.encode("ascii")

    root = ET.fromstring(remove_ns(k.decode("ascii")))

    path_list = []
    if root[0].tag == "defs": # remove defs element if exists (they usually
                              # containe path elements and interfere with
                              # root.iter('path') in the next section.)
        root[:1] = []

    for el in root.iter("path"):
        d = el.attrib["d"]
        t = el.attrib.get("transform", "")
        path_list.append(dict(d=d, transform=t))

    w_ = root.attrib["width"]
    h_ = root.attrib["height"]
    w = float(w_[:-2] if w_.endswith("pt") else w_)
    h = float(h_[:-2] if h_.endswith("pt") else h_)

    return w, h, path_list


def convert_path(width, height, path_data, mode, stroke_width=1, slug=None):
    """convert path definition from pattern monster to something that matplotlib can easily understand.

    path_data : string from _index.js. Multiple paths are separated by '~'.
    stroke_width : stroke will be converted to fill by picosvg.
    """

    # Some of the path data in pattern_monster cannot be parsed by svgpath2mpl.
    # We preprocess it with cairosvg, whose result can be parsed by
    # svgpath2mpl.

    # However, the path will go beyond the its viewbox. We should clip the path
    # with the viewbox at drawing to get the correct result.

    # To make things simpler, we further process the result with picosvg. With
    # picosvg, we will clip the path withe viewbox. picosvg will also convert
    # any strokes to fills. So stroking the resulting path with different width
    # will be different from stroking them with the original path.

    # 1. We first generate a svg definition containing a path.
    _template = "<svg width='{width}px' height='{height}px'></svg>".format(width=width,
                                                                           height=height)
    root = ET.fromstring(_template)

    for _s in path_data.split("~"):
        el = ET.fromstring(_s)
        if mode.startswith("stroke"):
            el.attrib["fill"] = "none"
            el.attrib["stroke"] = "black" # the actual color does not matter.
            el.attrib["stroke-width"] = f"{stroke_width}"
        else:
            el.attrib["fill"] = "red"
            el.attrib["stroke"] = "none"

        root.append(el)

    s = ET.tostring(root)

    w, h, path_list = _convert_path(s, slug=slug)

    return w, h, path_list


def convert_pattern_monster(fn, slug_converted=None):
    """
    Given a _index.js file from the pattern_monster package, convert it to more useful
    form that matplotlib can easily deal with.
    """

    if slug_converted is None:
        slug_converted = dict()

    l = open(fn).read()
    ll = l.split(";")

    idx = ll[0].index('=')  # location of 1st '=' which marks the start of the json string.
    j = json.loads(ll[0][idx+1:])

    new_j = []
    for i, j1 in enumerate(j):
        j2 = j1.copy()

        if j1["slug"] in slug_converted:
            _s = open(slug_converted[j1["slug"]], "rb").read()
            w, h, new_paths = _convert_path(_s)
        else:
            try:
                w, h, new_paths = convert_path(j1["width"], j1["height"], j1["path"], j1["mode"],
                                               slug=j1["slug"])
            except:
                print(i, j1["slug"], "failed")
                continue
        j2["width"] = w
        j2["height"] = h
        j2["path"] = new_paths
        j2["npath"] = len(new_paths)

        new_j.append(j2)

    return new_j

def main():
    fn = "_index.js"

    # For a single case of "scales-3", picosvg failed to clip the path with
    # viewBox. For such cases, it now saves the svg file with a rect spanning
    # the viewBox added. You can clip the file manually. For example, ppen the
    # file in inkscape (for example), select all path, and do intersection.
    # Then, save the result and provide the name of the files in the dictionary
    # of slug_converted.

    slug_converted = {"scales-3":"scales-3-clipped.svg"}
    new_j = convert_pattern_monster(fn, slug_converted=slug_converted)
    json.dump(new_j, open("pattern_monster.json", "w"), indent=2)

    # save another version w/o path data.
    json.dump([dict((k, v) for k,v in j1.items() if k != "path")
               for j1 in new_j],
              open("pattern_monster_wo_path.json", "w"))

    # convert path data to vertices and codes which are numpy arrays.
    r = {}
    for j1 in new_j:
        # FIXME: The result of cairosvg can have matrix attribute. We should
        # read the matrix and scale the path. but for now, we ignore this.
        # The result of picosvg should not have transform set.
        k = j1["slug"].replace("-", "_")
        for i, _p in enumerate(j1["path"]):
            p = svgpath2mpl.parse_path(_p["d"])
            v = p.vertices
            h = j1["height"]
            v = v*[1, -1] + [0, h]

            r[f"{k}_v{i}"] = v
            r[f"{k}_c{i}"] = p.codes

    np.savez("pattern_monster_vertcies_codes.npz", **r)


if __name__ == '__main__':
    main()


if False:
    # s = open("test0_clipped.svg", "rb").read()
    # w, h, path_list = _convert_path(s)


    j1 = new_j[98]
    do_pico = True
    print(j1["title"], j1["mode"])

    import matplotlib.pyplot as plt
    from matplotlib.patches import PathPatch

    from matplotlib.transforms import Bbox, TransformedBbox, Affine2D

    path_list = j1["path"]
    w, h = j1["width"], j1["height"]

    pp = []
    for i, _p in enumerate(path_list):
        p = svgpath2mpl.parse_path(_p["d"])
        pp.append(p)

    fig, ax = plt.subplots(num=1, clear=True)
    for ox, oy in [[0, 0], [w, 0], [0, h], [w, h]][:]:
        for p in pp:
            v = p.vertices + np.array([ox, oy])
            p = type(p)(vertices=v, codes=p.codes)
            pp1 = PathPatch(p, ec="g", fc="g")
            ax.add_patch(pp1)

    ax.set(xlim=(-w, 3*w), ylim=(-h, 3*h))
    plt.show()

