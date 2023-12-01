import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame
import numpy as np

import rasterio
from rasterio.crs import CRS
import rasterio.mask
import rasterio.plot

from scipy.ndimage import distance_transform_edt
from affine import Affine
import matplotlib.pyplot as plt

from shapely.geometry import box
from shapely.geometry import LineString
from shapely.geometry import Point

from pathlib import Path
from typing import Tuple
from typing import Any

# Generate expanded bounding box for rasterization
def expand_bounding_box(gdf: GeoDataFrame) -> pd.DataFrame:

    # Generate original bounding box
    bbox = gdf.geometry.bounds

    # Extract bounding box coordinates as floats using iloc[0]
    minx = float(bbox.minx.iloc[0])
    miny = float(bbox.miny.iloc[0])
    maxx = float(bbox.maxx.iloc[0])
    maxy = float(bbox.maxy.iloc[0])

    # Calculate the expansion sizes for height and width
    height_expansion = (maxy - miny) 
    width_expansion = (maxx - minx)  

    # Create new bounding coordinates
    new_minx = minx - width_expansion  # Expanding left
    new_miny = miny - height_expansion  # Expanding bottom
    new_maxx = maxx + width_expansion  # Expanding right
    new_maxy = maxy + height_expansion  # Expanding top

    expanded_bbox = pd.DataFrame({
        'minx': [new_minx],
        'miny': [new_miny],
        'maxx': [new_maxx],
        'maxy': [new_maxy]
    })
        
    return expanded_bbox

# Get Meta data from TIF file
def get_metadata(tif_file_path: Path) -> Tuple[dict, Tuple[int, int], Affine, CRS]:
    
    with rasterio.open(tif_file_path) as src:
        out_meta = src.meta
        shape = src.shape
    
    # Transform Data
    transform = out_meta['transform']
    # Out metadata is exactly the same as our in metadata.
    target_crs = out_meta['crs']
    
    return out_meta, shape, transform, target_crs


# Generate expanded shape and new transform 
def expand_shape_and_transform(original_shape: Tuple[int, int], original_transform: Affine) -> Tuple[Tuple[int, int], Affine]:

    # New shape
    new_shape = (original_shape[0]*3, original_shape[1]*3)

    # New transform
    # Calculate the adjustment considering the resolution
    height = original_shape[0]
    width = original_shape[1]
    
    resolution = original_transform.a
    adjustment_x = resolution * width  # Width adjustment (to the left)
    adjustment_y = resolution * height  # Height adjustment (up)

    # Update the transform by adding adjustments
    new_transform = Affine(original_transform.a, original_transform.b, original_transform.c - adjustment_x,
                        original_transform.d, original_transform.e, original_transform.f + adjustment_y)

    return new_shape, new_transform 


# Rasterize geometeries found in a GDF onto an empty array based on an existing transform
def rasterize(gdf: GeoDataFrame, out_shape: Tuple[int, int], transform: Affine) -> np.ndarray:

    # Rasterize the GeoDataFrame
    rasterized = rasterio.features.rasterize(
        [(geom, 1) for geom in gdf.geometry],
        out_shape=out_shape,
        transform=transform,
        fill=0,
        all_touched=True,
        dtype=rasterio.uint8
    )

    # Switch 1s and 0s
    rasterized = np.logical_not(rasterized).astype(int)
    return rasterized

# Subset expanded distance array to original size
def subset_array(original_shape: Tuple[int, int], computed_array: np.ndarray) -> np.ndarray:

    # Create rows and columns
    start_row = original_shape[0]
    end_row = original_shape[0]*2
    start_col = original_shape[1]
    end_col = original_shape[1]*2

    # Subset original array from expanded distance array
    original_out = computed_array[start_row:end_row, start_col:end_col]

    return original_out

# Used to stamp a country border on an existing raster image
def mask_admin(in_path: Path, admin_path: Path, out_path: Path) -> None:

    with rasterio.open(in_path) as src:
        admin = gpd.read_file(admin_path).to_crs(src.crs)
        kwargs = {
            'all_touched': True,
            'nodata': np.nan,
        }

        out_image, out_transform = rasterio.mask.mask(
            src, 
            admin.geometry.tolist(),
            **kwargs        
        )
        out_meta = src.meta

    out_meta.update({"driver": "GTiff",
                     "nodata": np.nan,
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "transform": out_transform})

    with rasterio.open(out_path, "w", **out_meta) as dest:
        dest.write(out_image)

# Create Diagnostic Plots
def generate_plots(admin_gdf: GeoDataFrame, vector_gdf: GeoDataFrame, out_path: Path, save_path: Path) -> None:

    fig, axs = plt.subplots(1, 3, figsize=(30, 10))
    # Read in New Raster
    with rasterio.open(out_path) as src:
        combined_raster = src.read(1, masked=True)
        transform = src.transform
    log_combined_raster = np.log(1 + combined_raster)

    # Plot 1: Original vector geometries and admin boundary
    vector_gdf.plot(ax=axs[0], edgecolor='red', facecolor='none')
    admin_gdf.boundary.plot(ax=axs[0], color='k')
    axs[0].set_title('Original Vector Geometries and Admin Boundary')

    # Plot 2: Combined raster with admin boundary overlay
    im = axs[1].imshow(combined_raster, extent=(transform[2], transform[2] + transform[0]*combined_raster.shape[1],
                                       transform[5] + transform[4]*combined_raster.shape[0], transform[5]), cmap='viridis')
    fig.colorbar(im, ax=axs[1])
    axs[1].set_title('Distance with Country Overlay')
    admin_gdf.boundary.plot(ax=axs[1], color='red')
    # Plot 3: Log-transformed raster with admin boundary overlay
    im = axs[2].imshow(log_combined_raster, extent=(transform[2], transform[2] + transform[0]*combined_raster.shape[1],
                                       transform[5] + transform[4]*combined_raster.shape[0], transform[5]), cmap='viridis')
    fig.colorbar(im, ax=axs[2])
    axs[2].set_title('Log Distance with Country Overlay')
    admin_gdf.boundary.plot(ax=axs[2], color='red')

    plt.tight_layout()
    plt.savefig(save_path)

    return

# Main function that takes in path files and processes through all the steps to compute distance
def compute_distance(admin0_path: Path, vector_file_path: Path, meta_data_path: Path, out_path: Path, image_save_path: Path) -> None:

    # Step 1:Read in admin0 file
    admin0_path = admin0_path
    admin0 = gpd.read_file(admin0_path)

    # Step 2:Generate Expanded Bounding Box
    expanded_bbox = expand_bounding_box(admin0)

    # Step 3:Read in vector file
    vector_file_path = vector_file_path
    vector_gdf = gpd.read_file(vector_file_path)
    vector_gdf = vector_gdf.to_crs(admin0.crs)

    # Step 4:Subest Vector file path with Expanded Bounding Box
    vector_gdf_subset = vector_gdf.cx[expanded_bbox.iloc[0]['minx']:expanded_bbox.iloc[0]['maxx'],
                              expanded_bbox.iloc[0]['miny']:expanded_bbox.iloc[0]['maxy']]

    # Step 5:Read in TIF file for metadata
    out_meta, shape, transform, target_crs = get_metadata(meta_data_path)

    # Step 6:Generate new transform and shape
    new_shape, new_transform = expand_shape_and_transform(shape, transform)

    # Step 7:Align files to target_crs
    admin0 = admin0.to_crs(target_crs)
    vector_gdf_subset = vector_gdf_subset.to_crs(target_crs)

    # Step 8:Rasterize vector file
    rasterized = rasterize(vector_gdf_subset, new_shape, new_transform)

    # Step 9:Compute Distance
    out = distance_transform_edt(rasterized)
    print("Distance computed")

    # Step 10:Subset original array shape from computed distances
    original_out = subset_array(shape, out)

    # Step 11:Write out tif file
    original_out = original_out.astype(out_meta['dtype'])
    with rasterio.open(out_path, "w", **out_meta) as dest:
        dest.write(original_out.reshape((1, *original_out.shape)))

    # Step 12:Stamp out border 
    mask_admin(out_path, admin0_path, out_path)

    # Step 13:Create Diagnostic Plots
    generate_plots(admin0, vector_gdf_subset, out_path, image_save_path)
    print('TIF saved at', out_path)
    print('Plots saved at', image_save_path)
    return
