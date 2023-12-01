"""Module for rasterizing a geopackage to a raster."""
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union

import geopandas as gpd
import matplotlib.cm
import numpy as np
import pandas as pd
import rasterio
from rasterio import features

logger = logging.getLogger(__name__)


def rasterize_multilabel(
    gpkg_path: Path,
    reference_image: Path,
    class_column: str,
    classes: List[Union[str, int]],
    include_background_class: bool = True,
    dense: bool = True,
) -> np.ndarray:
    """Rasterize a geopackage into a dense encoded one-hot array.

    The first class will be the background, if background class is true. The following
    classes are numbered from 1 ... n, where n is de number of elements in the "classes"
    list. The order of the numbers corresponds to the order of the classes in the list.

    Parameters
    ----------
    gpkg_path : Path
        Path to geopackage file to rasterize.
    reference_image : Path
        Path to reference image to extract transform and shape from.
    class_column
        Column in the geopackage that indicates class type
    classes
        List that indicates the possible classes and order of the classes. E.g., for a
        three class model with possible classes 1, 2, 3, the classes list should be:
        [1, 2, 3]. If classes in the class column are named as strings it could be:
        ["Schoolzone", "Pedestrian crossing", "Speedbump"].
    include_background_class
        Indicate if background class is included in the one hot array. True by default.
        If set to False this may result in -9999 values for missing class in dense
        encoding, or an empty array for one-hot encoding.
    dense : bool
        Indicate if the array should be densely encoded. Meaning axis 1 will be size 1,
        and the integer value indicates the class.

    Returns
    -------
    One-hot array
    """
    rasters: List[np.ndarray] = [
        rasterize(
            gpkg_path=gpkg_path,
            reference_image=reference_image,
            filters={class_column: [c]},
        )
        for c in classes
    ]
    raster: np.ndarray = np.array(rasters)

    if include_background_class:
        background = (~raster.any(axis=0)).astype("uint8")
        raster = np.concatenate((background[np.newaxis, ...], raster), axis=0)

    if dense:
        missing = (~raster.any(axis=0))[np.newaxis, ...]
        raster = raster.argmax(axis=0)[np.newaxis, ...]
        if missing.any():
            raster[missing] = -9999
            logger.warning(
                "include_background_class is set to False, but there were "
                "background pixels found. Background pixels were set to "
                "-9999. If this is not intended, set "
                "include_background_class=True"
            )

    return raster


def rasterize(
    gpkg_path: Path,
    reference_image: Path,
    filters: Optional[Dict[str, List[Union[str, int]]]] = None,
) -> np.ndarray:
    """Rasterize a geopackage into a boolean array.

    Parameters
    ----------
    gpkg_path : Path
        Path to geopackage file to rasterize.
    reference_image : Path
        Path to reference image to extract transform and shape from.
    filters : dict
        Filters to indicate which column / values pairs to include. For example:
        {"surfaceMaterial": ["gesloten verharding"]} to only include rows with a
        "gesloten verharding" value on the "surfaceMaterial" column

    Returns
    -------
    rasterized image as numpy array, where 1 indicates an object, and 0 indicates
    no object.
    """
    ref = rasterio.open(reference_image)
    gdf = gpd.read_file(gpkg_path, bounding_box=ref.bounds)

    if filters:
        gdfs = [
            gdf[gdf[column] == filter_value]
            for column, filter_values in filters.items()
            for filter_value in filter_values
            if column in gdf.columns
        ]
        gdf = pd.concat(gdfs).drop_duplicates() if gdfs else None

    if len(gdf) > 0:
        raster = features.rasterize(
            shapes=gdf["geometry"], out_shape=ref.shape, fill=0, transform=ref.transform
        )
    else:
        raster = np.zeros(ref.shape)

    return raster


def raster_to_geotif(
    raster: np.ndarray,
    reference: Path,
    output: Path,
) -> None:
    """Convert a raster to a geotiff that matches refence image.

    Parameters
    ----------
    raster : np.ndarray
        Numpy array with raster to convert to geotif
    reference : Path
        Reference image the output geometry is be based upon.
    output : Path
        Path to the output geotiff
    """
    channels = raster.shape[0]

    # load reference image
    rst = rasterio.open(reference)
    meta = rst.meta
    meta.update(compress="lzw")
    meta.update(count=channels)

    with rasterio.open(output, "w+", **meta) as out:
        out.write(raster)

    return None


def dense_rasters_to_rgb(
    raster: np.ndarray,
    num_classes: Optional[int] = None,
    alpha: bool = False,
    cmap: str = "tab10",
) -> np.ndarray:
    """Convert list of boolean rasters to an 8-bit RGB(a) raster.

    Parameters
    ----------
    raster : np.ndarray
        Densely encoded one-hot array. Each index indicates the presence of its
        corresponding class.
    num_classes : int, optional
        Indicate the maximum number of classes, excluding background. Defaults to the
        maximum index that is found in the given raster. If this is not set the colors
        may be inconsistent for instances where not all classes are present in the
        image.
    alpha : bool
        Indicate if alpha channel should be included. If True the background will be
        fully transparent, while the classes will be fully opaque.
    cmap : str
        A matplotlib colormap name to draw colors from for assignment to the classes.

    Returns
    -------
    A 3d RGB or 4D RGBA array with color values between 0 and 255, with class
    colors drawn from the matplotlib colormap. The array is returned as a
    channels-first array.
    """
    raster = raster.squeeze()
    if num_classes and num_classes < raster.max():
        raise ValueError(
            f"num_classes cannot be lower than the max index in the raster\n"
            f"num_classes is {num_classes}, but the maximum index in raster "
            f"is {raster.max()}"
        )
    num_classes = num_classes or raster.max()
    mapping: dict[int, tuple[float, ...]] = {
        cat: matplotlib.cm.get_cmap(cmap)(
            (matplotlib.colors.Normalize(1, num_classes)(cat))
        )
        for cat in range(1, num_classes + 1)
    }
    mapping.update({0: (0.0, 0.0, 0.0, 0.0)})

    if not alpha:
        channels = 3
        mapping = {key: val[:channels] for key, val in mapping.items()}

    # vectorize the dict get function to apply to each element in cat_raster
    vfunc = np.vectorize(
        mapping.get,
    )

    rgb_raster = np.stack(vfunc(raster))
    rgb_raster = (rgb_raster * 255).astype(np.uint8)

    return rgb_raster
