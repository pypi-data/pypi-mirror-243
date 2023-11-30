# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2019)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

"""
Formats:
    DeltaVision
        dv, r3d, rcpnl
        https://docs.openmicroscopy.org/bio-formats/6.9.1/formats/deltavision.html

imageio:
    See https://imageio.readthedocs.io/en/stable/reference/index.html#plugins-backend-libraries

Using VTK seems too complicated. See
https://stackoverflow.com/questions/25230541/how-to-convert-a-vtkimage-into-a-numpy-array
for a 3-D example.
"""
import importlib as mprt
import itertools as ittl
import sys as sstm
from functools import partial as partial_t
from types import ModuleType as module_t
from typing import Callable, Sequence, Tuple

import numpy as nmpy

from im_tools_36.path import path_h, path_t

array_t = nmpy.ndarray


def _WithAICS(aics: module_t, path: str, /) -> array_t:
    """
    Arrangement: TCZYX
    """
    return aics.AICSImage(path).data


def _WithCziTools(czit: module_t, path: str, /) -> array_t:
    """"""
    output, *_ = czit.read_6darray(path)
    return output


def _WithMRC(mrci: module_t, path: str, /) -> array_t:
    """
    If output.ndim == 5, probably time x channel x Z x Y x X, while sequences are:
        time x channel   x (Z=1 x)             Y x X.
    So one gets:
        time x channel=1 x Z=actual channels x Y x X. Then, use: output[:, 0, :, :]
    numpy.array: Because the returned value seems to be a read-only memory map
    """
    return nmpy.array(mrci.imread(path))


def _WithNibabel(nbbl: module_t, path: str, /) -> array_t:
    """"""
    image = nbbl.load(path)

    return image.get_fdata()


def _WithPillow(pllw: module_t, path: str, /) -> array_t:
    """"""
    image_t = getattr(pllw, "Image")
    with image_t.open(path) as image:
        image.load()

    return nmpy.asarray(image)


# Key:   Pypi-name of toplevel package on Pypi.
# Value: Name of (sub)-package to be imported ("": Same as key).
IMPORT_FOR_MODULE = {
    "aicsimageio": ("", _WithAICS),
    "czifile": ("", "imread"),
    "czitools": ("czitools.read_tools", _WithCziTools),
    "imageio": ("imageio.v3", "imread"),
    "itk": ("", "imread"),
    "mrc": ("", _WithMRC),
    "nibabel": ("", _WithNibabel),
    "opencv": ("cv2", "imread"),
    "pillow": ("PIL", _WithPillow),
    "scikit-image": ("skimage.io", "imread"),
    "tifffile": ("", "imread"),
}
# Aliases
IMPORT_FOR_MODULE["skimage"] = IMPORT_FOR_MODULE["scikit-image"]

# Modules must be ordered from general to specific.
# czifile and czitools are placed first (i.e. less important) because they add a
# spurious row or column on a test sequence (is the sequence corrupted? in any case,
# aics opens it, but with the last few frames corrupted, and Fiji opens it normally).
ORDERED_MODULES_PER_TYPE = {
    (): ("imageio", "itk", "pillow", "opencv", "scikit-image", "nibabel"),
    ("tif", "tiff"): ("aicsimageio", "tifffile"),
    ("dv",): ("aicsimageio", "mrc"),
    ("mrc",): ("mrc",),
    ("czi", "lif", "nd2"): ("aicsimageio", "czitools", "czifile"),
}


def _Module(name: str, /) -> module_t | None:
    """"""
    if name in sstm.modules:
        return sstm.modules[name]

    # https://docs.python.org/3/library/importlib.html#checking-if-a-module-can-be-imported
    if (spec := mprt.util.find_spec(name)) is None:
        return None

    output = mprt.util.module_from_spec(spec)
    sstm.modules[name] = output
    spec.loader.exec_module(output)

    return output


def _ImportDictionaries(
    import_for_module: dict[
        str, tuple[str | module_t, str | Callable[[module_t, path_h], array_t]]
    ]
) -> tuple[dict[str, module_t], dict[str, Callable[[path_h], array_t]]]:
    """"""
    module_with_name = {}
    function_of_module = {}

    for pypi_name, (import_name, Function) in import_for_module.items():
        if import_name == "":
            import_name = pypi_name
        module = _Module(import_name)
        if module is None:
            continue

        if isinstance(Function, str):
            Function = getattr(module, Function)
        else:
            # lambda functions are not adapted here (to be investigated some day).
            Function = partial_t(Function, module)

        module_with_name[pypi_name] = module
        function_of_module[pypi_name] = Function

    return module_with_name, function_of_module


MODULE_WITH_NAME, FUNCTION_OF_MODULE = _ImportDictionaries(IMPORT_FOR_MODULE)


def ImageVolumeOrSequence(
    path: path_h,
    /,
    *,
    should_squeeze: bool = True,
    expected_dim: int = None,
    expected_shape: Sequence[int | None] = None,
    with_module: str = None,
    should_print_module: bool = False,
) -> array_t | Tuple[str, ...]:
    """"""
    # Potential outputs
    image = None
    issues = []

    if isinstance(path, str):
        path_str = path
        path_lib = path_t(path)
    else:
        path_str = str(path)
        path_lib = path
    if (expected_dim is None) and (expected_shape is not None):
        expected_dim = expected_shape.__len__()

    if with_module is None:
        reading_functions = list(
            FUNCTION_OF_MODULE.get(_elm) for _elm in ORDERED_MODULES_PER_TYPE[()]
        )

        img_format = path_lib.suffix[1:].lower()
        for formats, modules in ORDERED_MODULES_PER_TYPE.items():
            if img_format in formats:
                reading_functions.extend(
                    FUNCTION_OF_MODULE.get(_elm) for _elm in modules
                )

        reading_functions = tuple(
            _elm for _elm in reading_functions if _elm is not None
        )
        if reading_functions.__len__() == 0:
            return (f"No modules available for image format {img_format}.",)
    elif with_module in FUNCTION_OF_MODULE:
        reading_functions = [FUNCTION_OF_MODULE[with_module]]
    else:
        return (
            f"{with_module}: Invalid module. "
            f"Expected={str(tuple(FUNCTION_OF_MODULE.keys()))[1:-1]}",
        )

    failure = True
    for Read in reversed(reading_functions):
        try:
            image = Read(path_str)
            # A module might return None, for example, in case of a failure instead of
            # raising an exception. Hence the test below.
            if isinstance(image, array_t):
                failure = False
                if should_print_module:
                    if isinstance(Read, partial_t):
                        Read = Read.func
                    print(
                        f'{path_str}: Read with function "{Read.__module__}.{Read.__name__}".'
                    )
                break
        except Exception as exception:
            if isinstance(Read, partial_t):
                Read = Read.func
            issues.append(
                f'Cannot open image with function "{Read.__module__}.{Read.__name__}".\n'
                f"Error:\n{exception}"
            )

    if failure:
        if issues.__len__() > 0:
            return tuple(issues)
        return ("Silent Exception",)

    if should_squeeze:
        image = nmpy.squeeze(image)

    if (expected_dim is not None) and (image.ndim != expected_dim):
        return (
            f"{image.ndim}: Invalid dimension (shape={image.shape}). "
            f"Expected={expected_dim}",
        )
    if expected_shape is None:
        return image

    shape = image.shape
    if _ShapeMatches(shape, expected_shape):
        return image

    shape_as_array = nmpy.array(shape)
    for order in ittl.permutations(range(image.ndim)):
        if _ShapeMatches(shape_as_array[nmpy.array(order)], expected_shape):
            return nmpy.moveaxis(image, order, range(image.ndim))

    return (
        f"{shape}: Invalid shape. "
        f"Expected={tuple(expected_shape)}, or a permutation of it.",
    )


def _ShapeMatches(
    actual: Tuple[int, ...] | array_t, expected: Sequence[int | None], /
) -> bool:
    """"""
    return all((_ctl == _xpt) or (_xpt is None) for _ctl, _xpt in zip(actual, expected))


def AvailableModules(
    *, as_modules: bool = False
) -> Tuple[module_t, ...] | Tuple[Tuple[str, str, str, str], ...]:
    """
    Tuple[str, str, str, str]:
        name for "with_module" parameter of ImageVolumeOrSequence,
        module Python name,
        module version,
        reading function name
    """
    if as_modules:
        return tuple(MODULE_WITH_NAME.values())

    output = []
    for pypi_name, module in MODULE_WITH_NAME.items():
        import_name = getattr(module, "__name__", "???")
        if "." in import_name:
            parent = import_name.split(sep=".", maxsplit=1)[0]
            version = getattr(sstm.modules[parent], "__version__", "???")
        else:
            version = getattr(module, "__version__", "???")
        function = FUNCTION_OF_MODULE[pypi_name]
        if isinstance(function, partial_t):
            function = function.func
        output.append((pypi_name, import_name, version, function.__name__))

    return tuple(output)
