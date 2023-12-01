import numpy as np
from pathops import (
    Path,
    OpBuilder,
    PathOp,
)

from matplotlib.path import Path as MPath

def mpl2skia(mpl_path, transform=None):
    if transform is not None:
        mpl_path = transform.transform_path(mpl_path)

    ci = iter(mpl_path.codes)
    vi = iter(mpl_path.vertices)

    path = Path()
    pen = path.getPen()

    for c in ci:
        if c == MPath.MOVETO:
            pen.moveTo(next(vi))
        elif c == MPath.LINETO:
            pen.lineTo(next(vi))
        elif c == MPath.CURVE3:
            pen.qCurveTo(next(vi), next(vi))
            next(ci)
        elif c == MPath.CURVE4:
            pen.curveTo(next(vi), next(vi), next(vi))
            next(ci)
            next(ci)
        elif c == MPath.CLOSEPOLY:
            pen.closePath()
            next(vi)

    return path


def skia2mpl(skia_path):
    codes = []
    verts = []
    for s, cc in skia_path.segments:
        # print(s, cc)
        if s == "moveTo":
            codes.extend([MPath.MOVETO] * len(cc))
            verts.extend(cc)
        elif s == "lineTo":
            codes.extend([MPath.LINETO] * len(cc))
            verts.extend(cc)
        elif s == "qCurveTo":
            if len(cc) == 2:
                codes.extend([MPath.CURVE3, MPath.CURVE3])
                verts.extend(cc)
            elif len(cc) > 2:
                # if len(c) > 2, multiple quad curve points are retuerned with
                # midpoints skipped and concatenated.
                ccc = []
                for i in range(0, len(cc)-2):
                    cc1 = cc[i]
                    cc2 = cc[i+1]
                    cc12 = 0.5*(np.array(cc1) + np.array(cc2)) # make midpoint
                    ccc.extend([cc1, cc12])
                ccc.extend(cc[-2:])

                verts.extend(ccc)
                codes.extend([MPath.CURVE3] * len(ccc))

        elif s == "curveTo":
            codes.extend([MPath.CURVE4] * len(cc))
            verts.extend(cc)
        elif s == "closePath":
            codes.append(MPath.CLOSEPOLY)
            verts.extend([(0, 0)])

    p = MPath(verts, codes=codes)
    return p

def union(path1, path2,
          fix_winding=True, keep_starting_points=False):
    builder = OpBuilder(fix_winding=fix_winding,
                        keep_starting_points=keep_starting_points)
    builder.add(path1, PathOp.UNION)
    builder.add(path2, PathOp.UNION)
    result = builder.resolve()

    return result

def intersection(path1, path2,
                 fix_winding=True, keep_starting_points=False):
    builder = OpBuilder(fix_winding=fix_winding,
                        keep_starting_points=keep_starting_points)
    builder.add(path1, PathOp.UNION)
    builder.add(path2, PathOp.INTERSECTION)
    result = builder.resolve()

    return result

def difference(path1, path2,
               fix_winding=True, keep_starting_points=False):
    builder = OpBuilder(fix_winding=fix_winding,
                        keep_starting_points=keep_starting_points)
    builder.add(path1, PathOp.UNION)
    builder.add(path2, PathOp.DIFFERENCE)
    result = builder.resolve()

    return result

def xor(path1, path2,
        fix_winding=True, keep_starting_points=False):
    builder = OpBuilder(fix_winding=fix_winding,
                        keep_starting_points=keep_starting_points)
    builder.add(path1, PathOp.UNION)
    builder.add(path2, PathOp.XOR)
    result = builder.resolve()

    return result
