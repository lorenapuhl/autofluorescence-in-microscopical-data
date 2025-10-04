"""Script to determine the average intensity over xlength of picture"""
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from statsmodels import robust

"""insert parameters"""
#insert data
names_01Feb = ["01Feb_W01_tail_Gre","01Feb_W02_tail_Gre","01Feb_W03_tail_Gre","01Feb_W04_tail_Gre","01Feb_W05_tail_Gre","01Feb_W06_tail_Gre","01Feb_W07_tail_Gre","01Feb_W08_tail_Gre","01Feb_W09_tail_Gre","01Feb_W10_tail_Gre","01Feb_W11_tail_Gre","01Feb_W12_tail_Gre","01Feb_W13_tail_Gre"]
names_02Feb = ["02Feb_W01_tail_Gre","02Feb_W02_tail_Gre","02Feb_W03_tail_Gre","02Feb_W04_tail_Gre","02Feb_W05_tail_Gre","02Feb_W06_tail_Gre","02Feb_W07_tail_Gre","02Feb_W08_tail_Gre","02Feb_W09_tail_Gre","02Feb_W10_tail_Gre","02Feb_W11_tail_Gre","02Feb_W12_tail_Gre","02Feb_W13_tail_Gre"]
names_04Feb = ["04Feb_W01_tail_Gre","04Feb_W02_tail_Gre","04Feb_W03_tail_Gre","04Feb_W04_tail_Gre","04Feb_W05_tail_Gre","04Feb_W06_tail_Gre","04Feb_W07_tail_Gre","04Feb_W08_tail_Gre","04Feb_W09_tail_Gre","04Feb_W10_tail_Gre","04Feb_W11_tail_Gre","04Feb_W12_tail_Gre","04Feb_W13_tail_Gre"]
names_05Feb = ["05Feb_W01_tail_Gre","05Feb_W02_tail_Gre","05Feb_W03_tail_Gre","05Feb_W04_tail_Gre","05Feb_W05_tail_Gre","05Feb_W06_tail_Gre","05Feb_W07_tail_Gre","05Feb_W08_tail_Gre","05Feb_W09_tail_Gre","05Feb_W10_tail_Gre","05Feb_W11_tail_Gre","05Feb_W12_tail_Gre","05Feb_W13_tail_Gre"]
names_08Feb = ["08Feb_W01_tail_Gre","08Feb_W02_tail_Gre","08Feb_W03_tail_Gre","08Feb_W04_tail_Gre","08Feb_W05_tail_Gre","08Feb_W06_tail_Gre","08Feb_W07_tail_Gre","08Feb_W08_tail_Gre","08Feb_W09_tail_Gre","08Feb_W10_tail_Gre"]
names_12Feb = ["12Feb_W01_tail_Gre","12Feb_W02_tail_Gre","12Feb_W03_tail_Gre","12Feb_W05_tail_Gre","12Feb_W06_tail_Gre","12Feb_W07_tail_Gre","12Feb_W08_tail_Gre","12Feb_W09_tail_Gre","12Feb_W10_tail_Gre","12Feb_W11_tail_Gre","12Feb_W12_tail_Gre"]

name_sets = [names_01Feb,names_02Feb,names_04Feb,names_05Feb, names_08Feb, names_12Feb]

#enter time of image acquisition
time_01Feb = list(np.ones(len(names_01Feb))*72)
time_02Feb = list(np.ones(len(names_02Feb))*93)
time_04Feb = list(np.ones(len(names_04Feb))*48)
time_05Feb = list(np.ones(len(names_05Feb))*167.5)
time_08Feb = list(np.ones(len(names_08Feb))*238)
time_12Feb = list(np.ones(len(names_12Feb))*338)

time_sets = [time_01Feb,time_02Feb,time_04Feb,time_05Feb, time_08Feb, time_12Feb]

"""Prepare time and names list for processing"""
##add times to single list
time_01Feb = [str(t) for t in time_01Feb]
time_02Feb = [str(t) for t in time_02Feb]
time_04Feb = [str(t) for t in time_04Feb]
time_05Feb = [str(t) for t in time_05Feb]
time_08Feb = [str(t) for t in time_08Feb]
time_12Feb = [str(t) for t in time_12Feb]

time = time_01Feb + time_02Feb + time_04Feb + time_05Feb + time_08Feb + time_12Feb

#convert elements back into floats
time = [np.float(t) for t in time]

"""Configuration flags"""
#Plot intensity profiles?
plot_y_inten = False
fig_y_inten_distr = 1
same_graph_y = False

plotgauss = False

plot_x_inten = False
fig_x_inten_distr = 2
same_graph_x = False

plot_points = True
fig_tot_inten_points = 3
plot_stats = True
fig_tot_inten_stats = 4
plot_both = True
fig_tot_inten = 5


"""FUNCTION DEFINITIONS"""

def load_image(imname):
    """
    Load TIFF image and convert to numpy array
    
    Parameters:
    -----------
    imname : str
        Image filename without extension
    
    Returns:
    --------
    impixels : numpy array
        Image as numpy array
    xsize : int
        Width of image
    ysize : int
        Height of image
    """
    im = Image.open(imname+".tif")
    impixels = np.array(im)
    
    xsize = int(impixels.shape[1])
    ysize = int(impixels.shape[0])
    
    print("xsize", xsize, "ysize", ysize)
    print("type", impixels.dtype)
    print("maximum", np.max(impixels))
    print("minimum", np.min(impixels))
    
    return impixels, xsize, ysize


def extract_columns(impixels, xsize):
    """
    Extract vertical columns from image
    
    Parameters:
    -----------
    impixels : numpy array
        Image as numpy array
    xsize : int
        Width of image
    
    Returns:
    --------
    columns : numpy array
        Array of columns
    amount_columns : int
        Number of columns
    length_columns : int
        Length of each column
    """
    columns = []
    for i in range(0, xsize):
        columns.append(impixels[:,i])
    
    columns = np.array(columns)
    amount_columns = int(columns.shape[0])
    length_columns = int(columns.shape[1])
    
    print("amount of columns", amount_columns)
    print("length of columns", length_columns)
    
    return columns, amount_columns, length_columns


def remove_zero_columns(columns, amount_columns, length_columns):
    """
    Remove columns containing zero values (artifacts from straightening)
    
    Parameters:
    -----------
    columns : numpy array
        Array of columns
    amount_columns : int
        Number of columns
    length_columns : int
        Length of each column
    
    Returns:
    --------
    cropped_columns : numpy array
        Columns without zeros
    cropped_amount_columns : int
        Number of valid columns
    """
    x = []
    for i in range(0, amount_columns):
        for j in range(0, length_columns):
            if columns[i,j] == 0:
                break
            elif j == length_columns - 1:
                x.append(columns[i])
            else:
                continue
    
    cropped_columns = np.array(x)
    cropped_amount_columns = int(cropped_columns.shape[0])
    
    return cropped_columns, cropped_amount_columns


def average_columns(columns, amount_columns, length_columns):
    """
    Average all columns to get mean intensity profile
    
    Parameters:
    -----------
    columns : numpy array
        Array of columns
    amount_columns : int
        Number of columns
    length_columns : int
        Length of each column
    
    Returns:
    --------
    avercolumn : numpy array
        Averaged column profile
    """
    sum_array = []
    for j in range(0, length_columns):
        x = columns[0,j]
        for i in range(1, amount_columns-1):
            x = x + columns[i,j]
        sum_array.append(x)
    
    sum_array = np.array(sum_array)
    avercolumn = sum_array / amount_columns
    
    return avercolumn


def gauss_function(x, a, x0, sigma, c):
    """
    Gaussian function for curve fitting
    
    Parameters:
    -----------
    x : array
        x values
    a : float
        Amplitude
    x0 : float
        Center position
    sigma : float
        Standard deviation
    c : float
        Baseline offset
    
    Returns:
    --------
    y : array
        Gaussian values
    """
    return a*np.exp(-(x-x0)**2/(2*sigma**2)) + c


def fit_gaussian(avercolumn, length_columns, imname):
    """
    Fit Gaussian to intensity profile to determine background and worm position
    
    Parameters:
    -----------
    avercolumn : numpy array
        Averaged column profile
    length_columns : int
        Length of column
    imname : str
        Image name for saving plot
    
    Returns:
    --------
    popt : array
        Optimized parameters [a, x0, sigma, c]
    bg : float
        Background intensity (baseline)
    """
    x = np.arange(0, length_columns)
    y = avercolumn
    
    # Initial parameters
    a = np.max(y)
    x0 = length_columns/2
    sigma = 100
    c = np.min(y)
    
    popt, pcov = curve_fit(gauss_function, x, y, p0=[a, x0, sigma, c])
    
    # Optional plotting
    if plotgauss == True:
        plt.figure()
        plt.plot(x, y, 'b-', label='aver y-inten')
        plt.plot(x, gauss_function(x, *popt), 'r-', label='fit')
        plt.legend()
        plt.title('Fit of worm position')
        plt.xlabel('height of image from top to bottom')
        plt.ylabel('Intensity')
        plt.savefig(str(imname)+"_average_intensity_gaussian")
        plt.close()
    
    bg = popt[3]
    return popt, bg


def replace_zeros_with_background(columns, amount_columns, length_columns, bg):
    """
    Replace zero-value pixels with background value
    
    Parameters:
    -----------
    columns : numpy array
        Array of columns
    amount_columns : int
        Number of columns
    length_columns : int
        Length of each column
    bg : float
        Background value
    
    Returns:
    --------
    columns : numpy array
        Columns with zeros replaced
    """
    for i in range(0, amount_columns):
        for j in range(0, length_columns):
            if columns[i,j] == 0:
                columns[i,j] = bg
    
    return columns


def background_subtraction(avercolumn, bg, length):
    """
    Subtract and normalize by background
    
    Parameters:
    -----------
    avercolumn : numpy array
        Averaged intensity profile
    bg : float
        Background value
    length : int
        Length of profile
    
    Returns:
    --------
    avercolumn : numpy array
        Background-subtracted profile
    """
    avercolumn = (avercolumn - bg) / bg
    
    # Set negative pixels to zero
    for i in range(0, length):
        if avercolumn[i] < 0:
            avercolumn[i] = 0
    
    return avercolumn


def plot_y_intensity_distribution(avercolumn, length_columns, imname, index_acquisitionset, bg):
    """
    Plot spatial intensity distribution along y-axis
    
    Parameters:
    -----------
    avercolumn : numpy array
        Averaged column profile
    length_columns : int
        Length of column
    imname : str
        Image name
    index_acquisitionset : int
        Index of acquisition set
    bg : float
        Background value
    """
    if plot_y_inten == True:
        if same_graph_y == True:
            plt.figure(fig_y_inten_distr)
            x = np.arange(0, length_columns)
            y = avercolumn
            plt.plot(x, y, label=imname[6:9]+" bg= "+str(int(bg)))
            plt.xlabel("ypixel from top to bottom of image")
            plt.ylabel("average intensity")
            plt.title("average intensity over y-axis for "+imname[0:5]+imname[9:22])
            plt.legend()
            plt.savefig("y_intensity_distribution"+imname[0:4]+imname[9:22])
            if imname == name_sets[index_acquisitionset][-1]:
                plt.close(fig_y_inten_distr)
        else:
            fig = plt.figure()
            x = np.arange(0, length_columns)
            y = avercolumn
            plt.plot(x, y, label=imname[6:8])
            plt.xlabel("ypixel from top to bottom of image")
            plt.ylabel("average intensity")
            plt.title("average intensity over y-axis of "+imname)
            plt.figtext(.7, .8, "bg= "+str(int(bg)))
            plt.savefig(str(imname)+"_y_intensity_distribution")
            plt.close(fig)


def extract_and_crop_lines(impixels, ysize, popt):
    """
    Extract horizontal lines and crop to region of interest (worm region)
    
    Parameters:
    -----------
    impixels : numpy array
        Image as numpy array
    ysize : int
        Height of image
    popt : array
        Gaussian fit parameters
    
    Returns:
    --------
    lines : numpy array
        Cropped lines in ROI
    amount_lines : int
        Number of lines
    length_lines : int
        Length of each line
    """
    lines = []
    for i in range(0, ysize):
        lines.append(impixels[i,:])
    
    lines = np.array(lines)
    
    print("amount of lines", int(lines.shape[0]))
    print("length of lines", int(lines.shape[1]))
    
    # Crop to worm region [x0-3σ, x0+3σ]
    lines = lines[int(popt[1]-3*popt[2]):int(popt[1]+popt[2])]
    amount_lines = int(lines.shape[0])
    length_lines = int(lines.shape[1])
    
    return lines, amount_lines, length_lines


def average_lines(lines, amount_lines, length_lines):
    """
    Average all lines to get mean intensity profile along x-axis
    
    Parameters:
    -----------
    lines : numpy array
        Array of lines
    amount_lines : int
        Number of lines
    length_lines : int
        Length of each line
    
    Returns:
    --------
    averline : numpy array
        Averaged line profile
    """
    sum_array = []
    for j in range(0, length_lines):
        x = lines[0,j]
        for i in range(1, amount_lines-1):
            x = x + lines[i,j]
        sum_array.append(x)
    
    sum_array = np.array(sum_array)
    averline = sum_array / amount_lines
    
    return averline


def plot_x_intensity_distribution(averline, length_lines, imname, index_acquisitionset, bg):
    """
    Plot spatial intensity distribution along x-axis
    
    Parameters:
    -----------
    averline : numpy array
        Averaged line profile
    length_lines : int
        Length of line
    imname : str
        Image name
    index_acquisitionset : int
        Index of acquisition set
    bg : float
        Background value
    """
    if plot_x_inten == True:
        if same_graph_x == True:
            plt.figure(fig_x_inten_distr)
            x = np.arange(0, length_lines)
            y = averline
            plt.plot(x, y, label=imname[6:9]+" bg= "+str(int(bg)))
            plt.xlabel("xpixel from left to right")
            plt.ylabel("average intensity")
            plt.title("average intensity over x-axis for "+imname[0:5]+imname[9:22])
            plt.legend()
            plt.savefig("x_intensity_distribution"+imname[0:4]+imname[9:22])
            if imname == name_sets[index_acquisitionset][-1]:
                plt.close(fig_x_inten_distr)
        else:
            fig = plt.figure()
            x = np.arange(length_lines)
            y = averline
            plt.plot(x, y, label=imname[6:8])
            plt.xlabel("xpixel from left to right")
            plt.ylabel("average intensity")
            plt.title("average intensity over x-axis of "+imname)
            plt.figtext(.7, .8, "bg= "+str(int(bg)))
            plt.savefig(str(imname)+"_x_intensity_distribution")
            plt.close(fig)


def calculate_total_intensity(avercolumn, popt):
    """
    Calculate total intensity in worm region
    
    Parameters:
    -----------
    avercolumn : numpy array
        Background-subtracted averaged column
    popt : array
        Gaussian fit parameters
    
    Returns:
    --------
    tot_inten_value : float
        Mean intensity per pixel in worm region
    """
    # Crop to worm region [x0-3σ, x0+3σ]
    x = avercolumn[int(popt[1]-3*popt[2]):int(popt[1]+popt[2])]
    
    # Calculate mean intensity per pixel
    tot_inten_value = np.sum(x) / float(len(x))
    
    return tot_inten_value


def process(imname, index_acquisitionset):
    """
    Main processing function that orchestrates all analysis steps
    
    Parameters:
    -----------
    imname : str
        Image filename without extension
    index_acquisitionset : int
        Index of acquisition set
    
    Returns:
    --------
    tot_inten_value : float
        Total intensity value for this image
    """
    # Step 1: Load image
    impixels, xsize, ysize = load_image(imname)
    
    # Step 2: Extract columns for y-axis analysis
    columns, amount_columns, length_columns = extract_columns(impixels, xsize)
    
    # Step 3: Remove columns with zeros for background calculation
    cropped_columns, cropped_amount_columns = remove_zero_columns(columns, amount_columns, length_columns)
    
    # Step 4: Average cropped columns
    cropped_avercolumn = average_columns(cropped_columns, cropped_amou

