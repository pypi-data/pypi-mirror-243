import rasterio
import rioxarray
import geopandas as gpd
import xarray as xr
import json
import numpy as np
from rasterio.warp import calculate_default_transform, reproject, Resampling






# function to convert file format
def convert_format(input_path, output_path, output_format= None ):
    
    # Read in the  file using geopandas
    gdf = gpd.read_file(input_path)
    
    CRS_input = gdf.crs
    
    if output_format is None:
        raise IndexError('Need output_format, it can be ESRI Shapefile or GeoJSON ')
    else: 
        # Write out the GeoDataFrame to a SHP file with the specified CRS and encoding
        gdf.to_file(output_path, driver = output_format, crs= CRS_input, encoding='utf-8')


# function to convert CRS of shp and geojson file  / raster file(tif)     
def convert_crs(input_path, output_path, new_crs):
    
    # init
    is_Raster = False
    is_Vector = False
    
    # Check if the operation involves Raster-Vector (RV) or Vector-Vector (VV) clipping
    if input_path.lower().endswith('.tif') :
        is_Raster = True
    elif (input_path.lower().endswith('.shp') or input_path.lower().endswith('.geojson')):
        is_Vector = True
    
    
    # if input is vector
    if is_Vector is True:
    
        # check defined crs
        if new_crs is None:
            raise IndexError( 'No crs, The crs should define.' )

        if input_path.lower().endswith('geojson'):

            # Read in the GeoJSON file using geopandas
            gdf = gpd.read_file(input_path)

            # Convert the geometry to the desired CRS
            gdf = gdf.to_crs(new_crs)

            # Write out the GeoDataFrame to a  file with the specified CRS and encoding
            gdf.to_file(output_path, driver='GeoJSON', crs=new_crs, encoding='utf-8')

        elif input_path.lower().endswith('shp'):

            # Read in the shp file using geopandas
            gdf = gpd.read_file(input_path)

            # Convert the geometry to the desired CRS
            gdf = gdf.to_crs(new_crs)

            # Write out the GeoDataFrame to a  file with the specified CRS and encoding
            gdf.to_file(output_path, driver='ESRI Shapefile', crs=new_crs, encoding='utf-8')

        else:
            raise IndexError('Input file format should be ESRI Shapefile or GeoJSON. ')
    
    if is_Raster is True:
        
        # Open the source raster dataset
        with rasterio.open(input_path,'r') as src:
            # Define the new CRS
            new_crs = rasterio.crs.CRS.from_epsg(new_crs)

            # Calculate the transformation parameters
            transform, width, height = calculate_default_transform(
                src.crs, new_crs, src.width, src.height, *src.bounds
            )
            
            # Create a new dataset for the reprojected image
            with rasterio.open(
                output_path, 'w',
                driver='GTiff',
                count=src.count,
                crs=new_crs,
                transform=transform,
                width=width,
                height=height,
                dtype=src.dtypes[0]
            ) as reprojected:
                # Reproject the source dataset to the new CRS
                for i in range(1, src.count+1):
                    reproject(
                        source=rasterio.band(src, i),
                        destination=rasterio.band(reprojected, i),
                        src_transform=src.transform,
                        src_crs=src.crs,
                        dst_transform=transform,
                        dst_crs=new_crs,
                        resampling=Resampling.bilinear
                )
    
# fuction to create xarray from raster       
def xarray_ds(tiff_path, rice_model = None):
    with rasterio.open(tiff_path) as src:
        
        # Get spatial information
        transform = src.transform
        crs = src.crs
        
        # count bands
        num_band = src.count
    
        # Initialize a dictionary to store DataArrays
        data_dict = {}
        
        # Create the coordinates for the x and y dimensions
        left, bottom, right, top = src.bounds
        x = np.linspace(left, right, src.width)
        y = np.linspace(top, bottom, src.height)
        

        # Read each band and create a DataArray for it
        for i in range(num_band):
            band_i = src.read(i + 1)  # Add 1 to the band index to match 1-based indexing
            ds_i = xr.DataArray(band_i, dims=('y', 'x'), 
                                coords={"y": y, "x": x})

            # Assign DataArray to a variable based on band index
            band_name = f'band_{i + 1}' 
            data_dict[band_name] = ds_i.astype(float)


        if rice_model is True:    
        # Calculate new bands
            ndvi_band = (data_dict['band_4'] - data_dict['band_1']) / (data_dict['band_4'] + data_dict['band_1'])
            ndwi_band = (data_dict['band_2'] - data_dict['band_4']) / (data_dict['band_4'] + data_dict['band_2'])
            gndvi_band = (data_dict['band_4'] - data_dict['band_2']) / (data_dict['band_4'] + data_dict['band_2'])

                        
            data_dict['NDVI'] = ndvi_band.astype(float)
            data_dict['NDWI'] = ndwi_band.astype(float)
            data_dict['GNDVI'] = gndvi_band.astype(float)
            
            # # Create an xarray Dataset with all the bands
            # dataset = xr.Dataset({'ndvi': ndvi_band, 'ndwi': ndwi_band, 'gndvi': gndvi_band}).astype(float)

        else:
            pass
            # # Create an xarray Dataset with all the bands
            # dataset = xr.Dataset(data_dict).astype(float)
 

        # Create an xarray Dataset with all the bands
        dataset = xr.Dataset(data_dict).astype(float)

        # Add global attributes if needed
        dataset.attrs['crs'] = str(crs)
        dataset.attrs['transform'] = transform

    return dataset

# the function to create new column in geojson file
# to add classtye table for training data
def geojson_add_Newcol(geojson_file_path):
    with open(geojson_file_path, 'r') as f:
        geojson_data = json.load(f)

    # Count the number of rows in the GeoJSON data
    
    num_rows = len(geojson_data['features'])
    print('num of rows: ',num_rows)
  
    # Prompt the user for the new column name and value
    new_column_name = input("Enter the name of the new column: ")
    # new_column_value = int(input("Enter the value for the new column: "))
    
    # Try to get an integer input for the new column value
    while True:
        new_column_value = input("Enter the value for the new column: ")
        try:
            new_column_value = int(new_column_value)
            break
        except ValueError:
            print("Invalid input: Please enter an integer value.")
    
    # Add the new column to each feature in the GeoJSON data
    for feature in geojson_data['features']:
        feature['properties'][new_column_name] = new_column_value

    # Write the updated GeoJSON data back to the file
    with open(geojson_file_path, 'w') as f:
        json.dump(geojson_data, f)

    # Return the number of rows in the GeoJSON data before the new column was added
    return num_rows

    
    
    

    

    
    
        
        
        
    
    
    
         




 