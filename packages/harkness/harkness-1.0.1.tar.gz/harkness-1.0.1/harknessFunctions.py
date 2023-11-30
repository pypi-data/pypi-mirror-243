# functions for visualization of data from pandas dataframes

# Importing packages
import pandas as pd
import matplotlib.pyplot as plt

def create_ply(df, filename, C = 'C', X = 'X', Y = 'Y', Z = 'Z', cmap = 'viridis', is_verbose = False):

    """
    Create a PLY file from a pandas DataFrame with columns X, Y, Z, and C.

    Parameters:
    df (pandas.DataFrame): The DataFrame containing the point cloud data.
    filename (str): The filename for the PLY file.
    C: The column of df associated with color; can be numeric or categorical.
    X, Y, Z: column names associated with X, Y and Z. XYZ by default.
    cmap: The matplotlib colormap used for the .ply file. 'viridis' by default.
    is_verbose: Boolean for printing debug text.
    """

    with open(filename, 'w') as f:
        f.write('ply\n')
        f.write('format ascii 1.0\n')
        f.write('element vertex %d\n' % len(df))
        f.write('property float x\n')
        f.write('property float y\n')
        f.write('property float z\n')
        f.write('property uchar red\n')
        f.write('property uchar green\n')
        f.write('property uchar blue\n')
        f.write('end_header\n')

        # Check if the column 'C' is numeric
        if pd.api.types.is_numeric_dtype(df[C]):
            for i in range(len(df)):
                row = df.iloc[i]
                cmap = plt.get_cmap(cmap)
                norm = plt.Normalize(min(df[C]), max(df[C]))
                color = cmap(norm(row[C]))

                # Calculate the RGB color for each point in the pointcloud
                color = [int(x * 255) for x in cmap(norm(row[C]))[:3]]

                # Write the coordinates and color values to the PLY file
                f.write('%f %f %f %d %d %d\n' % (row[X], row[Y], row[Z], int(color[0]), int(color[1]), int(color[2])))

        else:
            # Handle non-numeric values in column 'C'
            unique_values = df[C].unique()
            num_colors = len(unique_values)
            if(is_verbose): print("Color column is non-numeric. Mapping %d values to colors..." % num_colors)
            cmap = plt.cm.tab10
            norm = plt.Normalize(0, num_colors - 1)

            for i in range(len(df)):
                row = df.iloc[i]
                color_index = unique_values.tolist().index(row[C])
                color = cmap(norm(color_index))

                # Calculate the RGB color for each point in the pointcloud
                color = [int(x * 255) for x in cmap(norm(color_index))[:3]]

                # Write the coordinates and color values to the PLY file
                f.write('%f %f %f %d %d %d\n' % (row[X], row[Y], row[Z], int(color[0]), int(color[1]), int(color[2])))

    if(is_verbose): print("Saved file: %s" % filename)
