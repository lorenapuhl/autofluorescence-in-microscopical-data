# Comparing Fluorescence and Bioluminescence Microscopy: The Effect of Autofluorescence in *C. elegans*
Bachelor's Thesis conducted at ICFO (Institute of Photonic Sciences), Barcelona.

## Motivation

What is science? It is the art of shedding light on the principles of nature, and understanding our surroundings and the world we live in. Observation was the first step towards science, followed by the attempt to explain and understand what had been witnessed. This idea lead to the development of microscopes. Techniques rapidly improved, until In the 20th century 
**Fluorescence microscopy** became a new powerful tool for studying biological matter. Later, in 2010, the use of **bioluminescence** for depicting features hidden to the bare eyes emerged. It is a fairly new idea, that might in future replace the current standard, i.e. **Fluorescence microscopy**, since the latter technique features several drawbacks, such as so-called **autofluorescence**. This research project aims at shedding light onto the contrasting features of both imaging methods, by giving special attention to **autofluorescence**. For this purpose, **C. elegans** is used as an experimental model. 

<p align="center">

  <img src="https://github.com/user-attachments/assets/be83bb09-d97f-407b-b499-0612c785ff0b" alt="Image 1" width="700"/>
  <br>
  <em>Figure 1: Anatomy of *Caenorhabditis elegans*</em>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/123f4c50-382e-407d-8b3b-ebe24f8aa053" alt="Image 2" width="700"/>
  <br>
  <em>Figure 2: Fluorescence microscopy performed on C. elegans</em>
</p>


## Project Overview

This research project investigates the disturbing effect of autofluorescence (natural emission of light by biological structures other than the labeled feature) over time in microscopy imaging of *Caenorhabditis elegans*. As organisms age, autofluorescence increases and can interfere with the visualization of fluorescent signals, making it challenging to study labeled neurons in aging animals.

- **Model organism**: Two transgenic strains of *C. elegans* with mNeonGreen-labeled touch receptor neurons
- **Imaging techniques**: Fluorescence microscopy vs. bioluminescence microscopy
- **Age progression**: Samples imaged at different developmental stages to assess autofluorescence accumulation
- **Analysis**: Spatial intensity distributions and signal quantification across body parts (extrachromosomal and integrated strains, tails, bodies, mNeonGreen-spectra, and mCherry-spectra)

- <p align="center">

  <img src="https://github.com/user-attachments/assets/e38ba36e-8449-4ba5-843d-ea3198b24855" alt="Image 1" width="700"/>
  <br>
  <em>Figure 3: Fluorescence images of mNeonGreen-labelled neurons for ageing C. elegans samples.</em>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/bdf4aa18-1075-4c71-8560-9544e1812f99" alt="Image 2" width="700"/>
  <br>
  <em>Figure 4: Bioluminescence images of mNeonGreen-labelled neurons for ageing C. elegans samples </em>
</p>

## Analysis Pipeline

This project employs a systematic image processing and quantitative analysis pipeline to evaluate autofluorescence development in *C. elegans* over time. The analysis workflow consists of four main stages:

### 1. Spatial Intensity Distribution Analysis

#### Y-Axis Intensity Profile

The analysis begins by extracting spatial intensity distributions along the y-axis (vertical) of each fluorescence microscopy image. This process is implemented in the `process()` function in `14_FINAL_x_y_time.py`:

- **Column extraction**: The image is read as a numpy array and divided into vertical columns (`columns` array)
- **Zero-value handling**: Columns containing zero-value pixels (artifacts from image straightening) are identified and temporarily excluded to prevent bias in background calculation
- **Column averaging**: All valid columns are averaged to produce a mean intensity profile along the y-axis
- **Gaussian fitting**: A Gaussian curve is fitted to this profile using `scipy.optimize.curve_fit` where `c` represents the baseline background intensity, `x0` indicates the worm's center position, and `sigma` defines the spread

![Spatial intensity distribution](images/spatial_distribution_y.png)

*Figure: Fluorescence image of a worm's body-area near its gonad with a discernible neuron. The spatial distribution of the mean intensity along the y-axis is illustrated.*

![Gaussian fit](images/gaussian_fit.png)

*Figure: Averaged spatial intensity over the y-axis. A Gaussian is fitted to the data to determine the background value and worm position.*

#### Background Determination and Correction

The Gaussian baseline parameter (`popt[3]`) serves as the background value for each image. Zero-value pixels are then replaced with this background value to enable accurate intensity calculations. Background-subtracted intensities are calculated as `(raw_intensity - background) / background`. Negative values are set to zero to eliminate noise artifacts.

#### X-Axis Intensity Profile

After determining the worm's position from the y-axis analysis:

- **Region of interest selection**: Lines are extracted only from the region containing the worm, defined as `[x0 - 3σ, x0 + 3σ]` based on the Gaussian fit
- **Line averaging**: All lines within this region are averaged to produce a mean intensity profile along the x-axis (horizontal)
- **Background subtraction**: Applied using the same normalization method

![X-axis intensity](images/x_axis_intensity.png)

*Figure: Fluorescence microscopy image of a worm's mid-body area with spatial intensity distribution along the x-axis.*

### 2. Total Intensity Quantification

For each processed image, the total intensity is calculated by:

1. Cropping the background-subtracted y-axis profile to the worm region `[x0 - 3σ, x0 + 3σ]`
2. Summing all intensity values within this region
3. Normalizing by the region length: `total_intensity = sum(intensities) / len(region)`

This value represents the mean intensity per pixel within the worm region and is stored for temporal analysis.

### 3. Statistical Analysis by Age Group

Images are organized into acquisition sets corresponding to different worm ages (48h, 72h, 93h, 167.5h, 238h, 338h post-hatching). For each age group, the script calculates:

- **Individual data points**: Total intensity values for all individual worms
- **Central tendency**: Median using `np.median()`
- **Variability measures**: 
  - Standard deviation using `np.std()`
  - Median absolute deviation (MAD) using `statsmodels.robust.mad()` for robust statistics

![Total intensities extrachromosomal](images/total_intensity_extrachromosomal.png)

*Figure: Total intensities of the extrachromosomal strain MSB557 at different ages, using the GFP filter-cube. Individual data-points, as well as medians and median standard deviations are depicted.*

![Total intensities integrated](images/total_intensity_integrated.png)

*Figure: Total intensities of the integrated strain MSB651 at different ages, using the GFP filter-cube.*

### 4. Temporal Visualization

The analysis generates visualizations showing:

- **Individual data points**: Scatter plot showing total intensity for each individual worm against its age
- **Statistical summary**: Error bar plot displaying median intensity ± median absolute deviation for each age group
- **Combined view**: Two-panel figure showing both perspectives

The general pattern shows an increase in total intensities for aging samples, with body-parts and tails of *C. elegans* both featuring lower intensities than their respective counterparts. Extrachromosomal samples display higher data variability.

![mCherry intensities](images/mcherry_intensity.png)

*Figure: Total intensities of the integrated strain MSB651 at different ages, using the mCherry filter-cube.*

### 5. Neuron-to-Autofluorescence Ratio Analysis

Finally, autofluorescence and signal strength are simultaneously assessed by evaluating the neuron-to-autofluorescence-ratio over time. The ratio is determined by evaluating the neuron's intensity and dividing it by the previously calculated total autofluorescence of the area.

![Ratio extrachromosomal](images/ratio_extrachromosomal.png)

*Figure: Autofluorescence-to-noise ratios for the extrachromosomal strain MSB557 at different ages.*

![Ratio integrated](images/ratio_integrated.png)

*Figure: Autofluorescence-to-noise ratios for the integrated strain MSB651 at different ages.*

The general trend illustrates a decrease over time, showing that autofluorescence increases more rapidly than the neuronal signal in aging samples.

## Analysis Pipeline

This project employs a systematic image processing and quantitative analysis pipeline to evaluate autofluorescence development in *C. elegans* over time. The complete implementation can be found in `14_FINAL_x_y_time.py`. The analysis workflow consists of multiple modular functions organized into main stages:

### 1. Image Loading and Preprocessing

**Function: `load_image(imname)`**

The pipeline begins by loading TIFF images using PIL and converting them to numpy arrays for numerical processing. This function extracts basic image properties including dimensions and pixel data types, providing the foundation for subsequent analysis steps.

### 2. Spatial Intensity Distribution Analysis - Y-Axis

**Function: `extract_columns(impixels, xsize)`**

The image is divided into vertical columns for y-axis intensity analysis

### 3. Handling Image Artifacts
**Function: `remove_zero_columns(columns, amount_columns, length_columns)`**

Columns containing zero-value pixels (artifacts from image straightening) are temporarily removed to prevent bias in background calculation

### 4. Column Averaging
**Function: `average_columns(columns, amount_columns, length_columns)`**

All valid columns are averaged to produce a mean intensity profile along the y-axis

## Conclusion

- **Autofluorescence behavior**: Autofluorescence increases with age in fluorescence microscopy, creating a "veil" that obscures neuronal signals
- **Bioluminescence advantage**: Bioluminescence methods maintain consistently visible neuronal signals regardless of sample age
- **Signal-to-autofluorescence ratio**: Decreases over time in fluorescence imaging, demonstrating the progressive interference
- **Strain differences**: Extrachromosomal strains show higher data variability compared to integrated strains
- **Optimal conditions**: mCherry wavelength range and tail tissue analysis provide better fluorescence imaging results

**Bioluminescence microscopy demonstrates superior suitability for imaging aging *C. elegans* samples**, as it avoids the autofluorescence interference that progressively degrades fluorescence imaging quality over time.

---

## Repository Contents

*[Add sections here describing your code, data, analysis scripts, etc.]*

```markdown
# Comparing Fluorescence and Bioluminescence Microscopy: The Effect of Autofluorescence in *C. elegans*

## Introduction

This research project investigates the disturbing effect of autofluorescence over time in microscopy imaging of *Caenorhabditis elegans*. As organisms age, autofluorescence—the natural emission of light by biological structures when exposed to light—increases and can interfere with the visualization of fluorescent signals, making it challenging to study labeled neurons in aging animals.

## Project Overview

This bachelor's thesis compares fluorescence and bioluminescence microscopy techniques to determine which method better handles the interference from autofluorescence in aging *C. elegans* samples.

### Research Focus

- **Model organism**: Two transgenic strains of *C. elegans* with mNeonGreen-labeled touch receptor neurons
- **Imaging techniques**: Fluorescence microscopy vs. bioluminescence microscopy
- **Age progression**: Samples imaged at different developmental stages to assess autofluorescence accumulation
- **Analysis**: Spatial intensity distributions and signal quantification across body parts (extrachromosomal and integrated strains, tails, bodies, mNeonGreen-spectra, and mCherry-spectra)

### Key Findings

- **Autofluorescence behavior**: Autofluorescence increases with age in fluorescence microscopy, creating a "veil" that obscures neuronal signals
- **Bioluminescence advantage**: Bioluminescence methods maintain consistently visible neuronal signals regardless of sample age
- **Signal-to-autofluorescence ratio**: Decreases over time in fluorescence imaging, demonstrating the progressive interference
- **Strain differences**: Extrachromosomal strains show higher data variability compared to integrated strains
- **Optimal conditions**: mCherry wavelength range and tail tissue analysis provide better fluorescence imaging results

### Main Conclusion

**Bioluminescence microscopy demonstrates superior suitability for imaging aging *C. elegans* samples**, as it avoids the autofluorescence interference that progressively degrades fluorescence imaging quality over time.

---

## Analysis Pipeline

This project employs a systematic image processing and quantitative analysis pipeline to evaluate autofluorescence development in *C. elegans* over time. The complete implementation can be found in `14_FINAL_x_y_time.py`. The analysis workflow consists of multiple modular functions organized into main stages:

### 1. Image Loading and Preprocessing

**Function: `load_image(imname)`**

The pipeline begins by loading TIFF images using PIL and converting them to numpy arrays for numerical processing:

```python
def load_image(imname):
    """Load TIFF image and convert to numpy array"""
    im = Image.open(imname+".tif")
    impixels = np.array(im)
    xsize = int(impixels.shape[1])
    ysize = int(impixels.shape[0])
    return impixels, xsize, ysize
```

This function extracts basic image properties including dimensions and pixel data types, providing the foundation for subsequent analysis steps.

### 2. Spatial Intensity Distribution Analysis - Y-Axis

#### Column Extraction

**Function: `extract_columns(impixels, xsize)`**

The image is divided into vertical columns for y-axis intensity analysis:

```python
def extract_columns(impixels, xsize):
    """Extract vertical columns from image"""
    columns = []
    for i in range(0, xsize):
        columns.append(impixels[:,i])
    columns = np.array(columns)
    return columns, amount_columns, length_columns
```

#### Handling Image Artifacts

**Function: `remove_zero_columns(columns, amount_columns, length_columns)`**

Columns containing zero-value pixels (artifacts from image straightening) are temporarily removed to prevent bias in background calculation:

```python
def remove_zero_columns(columns, amount_columns, length_columns):
    """Remove columns containing zero values"""
    x = []
    for i in range(0, amount_columns):
        for j in range(0, length_columns):
            if columns[i,j] == 0:
                break
            elif j == length_columns - 1:
                x.append(columns[i])
    return cropped_columns, cropped_amount_columns
```

#### Column Averaging

**Function: `average_columns(columns, amount_columns, length_columns)`**

All valid columns are averaged to produce a mean intensity profile along the y-axis:

```python
def average_columns(columns, amount_columns, length_columns):
    """Average all columns to get mean intensity profile"""
    sum_array = []
    for j in range(0, length_columns):
        x = columns[0,j]
        for i in range(1, amount_columns-1):
            x = x + columns[i,j]
        sum_array.append(x)
    avercolumn = np.array(sum_array) / amount_columns
    return avercolumn
```

![Spatial intensity distribution](images/spatial_distribution_y.png)

*Figure: Fluorescence image of a worm's body-area near its gonad with a discernible neuron. The spatial distribution of the mean intensity along the y-axis is illustrated.*

### 3. Background Determination via Gaussian Fitting

#### Gaussian Function

**Function: `gauss_function(x, a, x0, sigma, c)`**

The Gaussian function used for curve fitting:

```python
def gauss_function(x, a, x0, sigma, c):
    """Gaussian function for curve fitting"""
    return a*np.exp(-(x-x0)**2/(2*sigma**2)) + c
```

Where:
- `a`: Peak amplitude (maximum intensity above baseline)
- `x0`: Center position (worm's vertical position in image)
- `sigma`: Standard deviation (worm width indicator)
- `c`: Baseline offset (**background intensity**)

#### Fitting Process

**Function: `fit_gaussian(avercolumn, length_columns, imname)`**

The script fits a Gaussian curve to the averaged y-axis intensity profile using `scipy.optimize.curve_fit`:

```python
def fit_gaussian(avercolumn, length_columns, imname):
    """Fit Gaussian to determine background and worm position"""
    x = np.arange(0, length_columns)
    y = avercolumn
    
    # Initial parameter estimates
    a = np.max(y)
    x0 = length_columns/2
    sigma = 100
    c = np.min(y)
    
    popt, pcov = curve_fit(gauss_function, x, y, p0=[a, x0, sigma, c])
    bg = popt[3]  # Background is the baseline parameter
    return popt, bg
```

The fitted baseline parameter `popt[3]` represents the background autofluorescence level, which is crucial for normalization. The center position `popt[1]` and spread `popt[2]` define the region of interest containing the worm.

![Gaussian fit](images/gaussian_fit.png)

*Figure: Averaged spatial intensity over the y-axis. A Gaussian is fitted to the data to determine the background value and worm position.*

### 4. Background Correction

#### Replacing Zero Values

**Function: `replace_zeros_with_background(columns, amount_columns, length_columns, bg)`**

Zero-value pixels (from image straightening) are replaced with the determined background value:

```python
def replace_zeros_with_background(columns, amount_columns, length_columns, bg):
    """Replace zero-value pixels with background value"""
    for i in range(0, amount_columns):
        for j in range(0, length_columns):
            if columns[i,j] == 0:
                columns[i,j] = bg
    return columns
```

#### Background Subtraction and Normalization

**Function: `background_subtraction(avercolumn, bg, length)`**

After replacing zeros, columns are re-averaged and background-subtracted:

```python
def background_subtraction(avercolumn, bg, length):
    """Subtract and normalize by background"""
    avercolumn = (avercolumn - bg) / bg
    
    # Set negative pixels to zero
    for i in range(0, length):
        if avercolumn[i] < 0:
            avercolumn[i] = 0
    return avercolumn
```

This normalization step `(intensity - background) / background` converts absolute intensities to relative values, accounting for variations in imaging conditions between samples.

#### Visualization

**Function: `plot_y_intensity_distribution(avercolumn, length_columns, imname, index_acquisitionset, bg)`**

Optional plotting of y-axis intensity distributions, controlled by the `plot_y_inten` flag.

### 5. Spatial Intensity Distribution Analysis - X-Axis

#### Line Extraction and ROI Cropping

**Function: `extract_and_crop_lines(impixels, ysize, popt)`**

Horizontal lines are extracted and cropped to the region of interest defined by the Gaussian fit:

```python
def extract_and_crop_lines(impixels, ysize, popt):
    """Extract horizontal lines and crop to worm region"""
    lines = []
    for i in range(0, ysize):
        lines.append(impixels[i,:])
    lines = np.array(lines)
    
    # Crop to worm region [x0 - 3σ, x0 + 3σ]
    lines = lines[int(popt[1]-3*popt[2]):int(popt[1]+popt[2])]
    return lines, amount_lines, length_lines
```

The ROI is defined as `x0 ± 3σ`, capturing approximately 99.7% of the Gaussian distribution (essentially the entire worm).

#### Line Averaging

**Function: `average_lines(lines, amount_lines, length_lines)`**

Lines within the ROI are averaged to produce a mean intensity profile along the x-axis:

```python
def average_lines(lines, amount_lines, length_lines):
    """Average all lines to get mean intensity profile along x-axis"""
    sum_array = []
    for j in range(0, length_lines):
        x = lines[0,j]
        for i in range(1, amount_lines-1):
            x = x + lines[i,j]
        sum_array.append(x)
    averline = np.array(sum_array) / amount_lines
    return averline
```

The same background subtraction function is then applied to this x-axis profile.

#### Visualization

**Function: `plot_x_intensity_distribution(averline, length_lines, imname, index_acquisitionset, bg)`**

Optional plotting of x-axis intensity distributions, controlled by the `plot_x_inten` flag.

![X-axis intensity](images/x_axis_intensity.png)

*Figure: Fluorescence microscopy image of a worm's mid-body area with spatial intensity distribution along the x-axis.*

### 6. Total Intensity Quantification

**Function: `calculate_total_intensity(avercolumn, popt)`**

The final intensity metric for each image is calculated by:

```python
def calculate_total_intensity(avercolumn, popt):
    """Calculate total intensity in worm region"""
    # Crop to worm region [x0 - 3σ, x0 + 3σ]
    x = avercolumn[int(popt[1]-3*popt[2]):int(popt[1]+popt[2])]
    
    # Calculate mean intensity per pixel
    tot_inten_value = np.sum(x) / float(len(x))
    return tot_inten_value
```

This normalized value represents the average background-subtracted intensity per pixel within the worm region. By normalizing by region length, the metric accounts for size variations between worms and allows fair comparison across samples.

### 7. Main Processing Function

**Function: `process(imname, index_acquisitionset)`**

The main processing function orchestrates all analysis steps in sequence:

```python
def process(imname, index_acquisitionset):
    """Main processing function orchestrating all analysis steps"""
    # 1. Load image
    impixels, xsize, ysize = load_image(imname)
    
    # 2. Extract and process columns (y-axis)
    columns, amount_columns, length_columns = extract_columns(impixels, xsize)
    cropped_columns, cropped_amount_columns = remove_zero_columns(columns, amount_columns, length_columns)
    cropped_avercolumn = average_columns(cropped_columns, cropped_amount_columns, length_columns)
    
    # 3. Fit Gaussian to determine background
    popt, bg = fit_gaussian(cropped_avercolumn, length_columns, imname)
    
    # 4. Replace zeros and re-average
    columns = replace_zeros_with_background(columns, amount_columns, length_columns, bg)
    avercolumn = average_columns(columns, amount_columns, length_columns)
    avercolumn = background_subtraction(avercolumn, bg, length_columns)
    
    # 5. Plot y-axis distribution
    plot_y_intensity_distribution(avercolumn, length_columns, imname, index_acquisitionset, bg)
    
    # 6. Process lines (x-axis)
    lines, amount_lines, length_lines = extract_and_crop_lines(impixels, ysize, popt)
    averline = average_lines(lines, amount_lines, length_lines)
    averline = background_subtraction(averline, bg, length_lines)
    
    # 7. Plot x-axis distribution
    plot_x_intensity_distribution(averline, length_lines, imname, index_acquisitionset, bg)
    
    # 8. Calculate total intensity
    tot_inten_value = calculate_total_intensity(avercolumn, popt)
    
    return tot_inten_value
```

### 8. Statistical Analysis by Age Group

**Function: `calculate_statistics(calc_stats)`**

For each age group (acquisition set), statistical measures are computed:

```python
def calculate_statistics(calc_stats):
    """Calculate statistical measures for an acquisition set"""
    median = np.median(calc_stats)
    mean = np.mean(calc_stats)
    std = np.std(calc_stats)
    meddev = robust.mad(calc_stats)  # Median Absolute Deviation
    return median, mean, std, meddev
```

The use of Median Absolute Deviation (MAD) via `statsmodels.robust.mad()` provides a robust measure of variability that is less sensitive to outliers than standard deviation. This is particularly important when analyzing biological samples where individual worms may exhibit natural variation.

#### Data Organization

Images are organized into acquisition sets by age:

```python
# Example: Define image sets
names_01Feb = ["01Feb_W01_tail_Gre", "01Feb_W02_tail_Gre", ...]
time_01Feb = list(np.ones(len(names_01Feb)) * 72)  # 72 hours post-hatching

name_sets = [names_01Feb, names_02Feb, names_04Feb, names_05Feb, names_08Feb, names_12Feb]
time_sets = [time_01Feb, time_02Feb, time_04Feb, time_05Feb, time_08Feb, time_12Feb]
```

The main execution loop processes each set:

```python
for index_acquisitionset in range(0, len(name_sets)):
    for j in range(0, len(name_sets[index_acquisitionset])):
        imname = name_sets[index_acquisitionset][j]
        tot_inten_value = process(imname, index_acquisitionset)
        totintensity.append(tot_inten_value)
        calc_stats.append(tot_inten_value)
        
    # Calculate statistics for completed set
    if imname == name_sets[index_acquisitionset][-1]:
        median, mean, std_val, meddev = calculate_statistics(calc_stats)
        stats_acquisitions.append(median)
        stats_acquisitions.append(meddev)
        calc_stats = []
```

![Total intensities extrachromosomal](images/total_intensity_extrachromosomal.png)

*Figure: Total intensities of the extrachromosomal strain MSB557 at different ages, using the GFP filter-cube. Individual data-points, medians, and median standard deviations are depicted.*

![Total intensities integrated](images/total_intensity_integrated.png)

*Figure: Total intensities of the integrated strain MSB651 at different ages, using the GFP filter-cube.*

### 9. Temporal Visualization

Three visualization functions generate different views of the temporal data:

#### Individual Data Points

**Function: `plot_individual_points(totintensity, time, imname)`**

Displays all individual measurements as scatter points:

```python
def plot_individual_points(totintensity, time, imname):
    """Plot individual intensity measurements over time"""
    plt.figure(fig_tot_inten_points)
    totintensity = np.array(totintensity)
    plt.errorbar(time, totintensity, linestyle='None', marker='x')
    plt.xlabel("time[hrs]")
    plt.ylabel("total intensity")
    plt.title("total intensity of over time")
    plt.savefig("total_intensity_over_time_points_"+imname[0:6]+imname[10:22])
```

#### Statistical Summary

**Function: `plot_statistics(stats_acquisitions, time_sets, imname)`**

Creates an error bar plot with median ± MAD for each age group:

```python
def plot_statistics(stats_acquisitions, time_sets, imname):
    """Plot statistical summary of intensities over time"""
    means = np.array(stats_acquisitions[0:len(stats_acquisitions):2])
    std = np.array(stats_acquisitions[1:len(stats_acquisitions):2])
    
    t = []
    for i in range(0, len(time_sets)):
        t.append(float(time_sets[i][0]))
    t = np.array(t)
    
    plt.figure(fig_tot_inten_stats)
    plt.errorbar(t, means, std, linestyle='None', marker='x')
    plt.xlabel("time[hrs]")
    plt.ylabel("total intensity")
    plt.savefig("total_intensity_over_time_stats_"+imname[0:6]+imname[10:22])
```

#### Combined View

**Function: `plot_combined(totintensity, time, stats_acquisitions, time_sets, imname)`**

Creates a two-panel figure showing both individual points and statistical summary:

```python
def plot_combined(totintensity, time, stats_acquisitions, time_sets, imname):
    """Plot both individual points and statistics in one figure"""
    plt.figure(fig_tot_inten)
    
    plt.subplot(2, 1, 1)
    plt.errorbar(time, totintensity, linestyle='None', marker='x')
    plt.ylabel("total intensity")
    plt.title("total intensity of over time")
    
    plt.subplot(2, 1, 2)
    plt.errorbar(t, means, std, linestyle='None', marker='x')
    plt.xlabel("time[hrs]")
    plt.ylabel("total intensity")
    
    plt.savefig("total_intensity_over_time_"+imname[0:6]+imname[10:22])
```

![mCherry intensities](images/mcherry_intensity.png)

*Figure: Total intensities of the integrated strain MSB651 at different ages, using the mCherry filter-cube.*

### 10. Analysis Results and Interpretation

The analysis reveals several key patterns:

**Increasing Autofluorescence with Age**: Total intensities increase for aging samples across all conditions, indicating accumulation of autofluorescent compounds over time.

**Body Region Differences**: Both tails and bodies of *C. elegans* show increasing autofluorescence, though with different baseline levels and rates of increase.

**Strain Variability**: Extrachromosomal strains (e.g., MSB557) display significantly higher data variability compared to integrated strains (e.g., MSB651), visible in the larger error bars and greater scatter of individual data points.

**Filter Cube Effects**: mCherry wavelength range shows different intensity profiles compared to GFP, suggesting wavelength-dependent autofluorescence characteristics.

### 11. Neuron-to-Autofluorescence Ratio

While the provided code focuses on total intensity quantification, the thesis also analyzes the neuron-to-autofluorescence ratio. This would involve:

1. Separately quantifying neuronal signal intensity (from labeled touch receptors)
2. Calculating the ratio: `neuron_intensity / total_autofluorescence`
3. Tracking how this ratio changes over time

![Ratio extrachromosomal](images/ratio_extrachromosomal.png)

*Figure: Autofluorescence-to-noise ratios for the extrachromosomal strain MSB557 at different ages.*

![Ratio integrated](images/ratio_integrated.png)

*Figure: Autofluorescence-to-noise ratios for the integrated strain MSB651 at different ages.*

The general trend shows a steady decrease in signal-to-autofluorescence ratio over time, demonstrating that autofluorescence increases more rapidly than the neuronal signal in aging samples. This progressive masking effect is the core problem that bioluminescence microscopy aims to solve.

---

## Code Configuration

The script uses boolean flags for flexible control of analysis and visualization:

```python
# Y-axis spatial intensity distribution
plot_y_inten = False        # Generate y-axis intensity plots
same_graph_y = False        # Combine all plots in one figure

# Gaussian fitting visualization
plotgauss = False           # Show Gaussian fits

# X-axis spatial intensity distribution
plot_x_inten = False        # Generate x-axis intensity plots
same_graph_x = False        # Combine all plots in one figure

# Temporal analysis
plot_points = True          # Show individual data points
plot_stats = True           # Show statistical summary
plot_both = True            # Show combined view
```

This modular configuration allows researchers to:
- Generate only needed visualizations
- Reduce processing time for large datasets
- Focus on specific analysis aspects
- Customize output for different presentation needs

---

## Repository Structure

```
├── 14_FINAL_x_y_time.py          # Main analysis script (refactored with functions)
├── data/
│   ├── raw_images/                # Original TIFF images (*.tif)
│   │   ├── 01Feb_W01_tail_Gre.tif
│   │   ├── 01Feb_W02_tail_Gre.tif
│   │   └── ...
│   └── processed/                 # Processed data and intermediate results
├── results/
│   ├── spatial_distributions/     # Y and X axis intensity profiles
│   │   ├── y_intensity_distribution_*.png
│   │   └── x_intensity_distribution_*.png
│   ├── gaussian_fits/             # Gaussian fitting visualizations
│   │   └── *_average_intensity_gaussian.png
│   ├── total_intensity_plots/     # Temporal analysis figures
│   │   ├── total_intensity_over_time_points_*.png
│   │   ├── total_intensity_over_time_stats_*.png
│   │   └── total_intensity_over_time_*.png
│   └── statistics/                # Statistical summaries (CSV or text files)
├── images/                        # Figures for README
└── README.md
```

---

## Requirements

### Python Dependencies

```
Python 3.x
PIL (Pillow) >= 8.0.0
numpy >= 1.19.0
matplotlib >= 3.3.0
scipy >= 1.5.0
statsmodels >= 0.12.0
```

### Installation

```bash
pip install pillow numpy matplotlib scipy statsmodels
```

Or using a requirements.txt file:

```bash
pip install -r requirements.txt
```

---

## Usage

### 1. Prepare Your Data

Place TIFF images in the data directory. Images should be named systematically to indicate:
- Acquisition date
- Worm identifier
- Body region (tail or body)
- Filter cube (Gre for GFP, mCherry, etc.)

Example: `01Feb_W01_tail_Gre.tif`

### 2. Configure the Script

Edit the beginning of `14_FINAL_x_y_time.py`:

```python
# Define image sets
names_01Feb = ["01Feb_W01_tail_Gre", "01Feb_W02_tail_Gre", ...]
names_02Feb = ["02Feb_W01_tail_Gre", "02Feb_W02_tail_Gre", ...]

# Define acquisition times (hours post-hatching)
time_01Feb = list(np.ones(len(names_01Feb)) * 72)
time_02Feb = list(np.ones(len(names_02Feb)) * 93)

# Organize into sets
name_sets = [names_01Feb, names_02Feb, ...]
time_sets = [time_01Feb, time_02Feb, ...]
```

### 3. Set Analysis Parameters

Configure which analyses and visualizations to generate:

```python
plot_y_inten = False    # Set to True to generate y-axis profiles
plotgauss = False       # Set to True to visualize Gaussian fits
plot_x_inten = False    # Set to True to generate x-axis profiles
plot_points = True      # Individual data points over time
plot_stats = True       # Statistical summary over time
plot_both = True        # Combined view
```

### 4. Run the Script

```bash
python 14_FINAL_x_y_time.py
```

The script will:
1. Load each image sequentially
2. Extract and analyze spatial intensity distributions
3. Perform Gaussian fitting to determine background and worm position
4. Calculate background-subtracted total intensities
5. Compute statistics for each age group
6. Generate requested visualizations
7. Save all figures with descriptive filenames

### 5. Interpret Results

Output files will be saved in the working directory:
- `*_y_intensity_distribution.png`: Y-axis spatial profiles
- `*_x_intensity_distribution.png`: X-axis spatial profiles
- `*_average_intensity_gaussian.png`: Gaussian fits
- `total_intensity_over_time_points_*.png`: Individual measurements
- `total_intensity_over_time_stats_*.png`: Statistical summary
- `total_intensity_over_time_*.png`: Combined view

---

## Key Implementation Details

### Modular Function Architecture

The refactored code organizes the analysis into discrete functions:

1. **Image I/O**: `load_image()`
2. **Column operations**: `extract_columns()`, `remove_zero_columns()`, `average_columns()`
3. **Background determination**: `gauss_function()`, `fit_gaussian()`
4. **Preprocessing**: `replace_zeros_with_background()`, `background_subtraction()`
5. **Line operations**: `extract_and_crop_lines()`, `average_lines()`
6. **Quantification**: `calculate_total_intensity()`
7. **Statistics**: `calculate_statistics()`
8. **Visualization**: `plot_y_intensity_distribution()`, `plot_x_intensity_distribution()`, `plot_individual_points()`, `plot_statistics()`, `plot_combined()`
9. **Orchestration**: `process()`

### Benefits of Modular Design

- **Testability**: Each function can be tested independently
- **Readability**: Clear function names and docstrings explain purpose
- **Reusability**: Functions can be imported and used in other scripts
- **Maintainability**: Bugs can be isolated to specific functions
- **Extensibility**: New analysis steps can be added as new functions

### Technical Highlights

- **Robust background estimation**: Gaussian fitting on zero-excluded data prevents bias
- **Region of interest selection**: Automatic ±3σ cropping ensures consistent worm capture
- **Normalized metrics**: Background-subtracted and area-normalized values enable fair comparison
- **Robust statistics**: MAD provides outlier-resistant variability measure
- **Batch processing**: Nested loops handle multiple acquisition sets automatically
- **Automatic naming**: Figures named based on strain, body part, and filter for organization

### Analysis Workflow Summary

```
Image Loading → Column Extraction → Zero Removal → Column Averaging →
Gaussian Fitting → Background Determination → Zero Replacement →
Re-averaging → Background Subtraction → Y-axis Plotting →
Line Extraction → ROI Cropping → Line Averaging →
Background Subtraction → X-axis Plotting → Total Intensity Calculation →
Statistical Analysis → Temporal Visualization
```

This pipeline enables systematic comparison of autofluorescence development between:
- **Different strains**: Extrachromosomal (MSB557) vs. integrated (MSB651)
- **Different body regions**: Tails vs. bodies
- **Different wavelengths**: GFP filter cube vs. mCherry filter cube
- **Different ages**: From 48h to 338h post-hatching

---

## Extending the Analysis

### Adding New Analysis Steps

To add a new analysis function:

1. Define the function with clear parameters and return values
2. Add appropriate docstrings
3. Call the function from `process()` or the main execution block
4. Add configuration flags if the analysis is optional

Example:

```python
def calculate_peak_intensity(avercolumn, popt):
    """
    Calculate peak intensity at worm center
    
    Parameters:
    -----------
    avercolumn : numpy array
        Background-subtracted averaged column
    popt : array
        Gaussian fit parameters
    
    Returns:
    --------
    peak_intensity : float
        Maximum intensity value
    """
    center_idx = int(popt[1])
    peak_intensity = avercolumn[center_idx]
    return peak_intensity
```

### Analyzing Different Conditions

To analyze different experimental conditions:

1. Prepare new image sets with systematic naming
2. Update the `names_*` and `time_*` lists
3. Update `name_sets` and `time_sets` accordingly
4. Run the script with the same configuration

### Batch Processing Multiple Strains

For processing multiple strains separately:

```python
strains = ['MSB557', 'MSB651']
body_parts = ['tail', 'body']
filter_cubes = ['Gre', 'mCherry']

for strain in strains:
    for body_part in body_parts:
        for filter_cube in filter_cubes:
            # Configure name_sets and time_sets for this combination
            # Run analysis
            # Save results with appropriate naming
```

---

## Troubleshooting

### Common Issues

**Issue**: `FileNotFoundError: [Errno 2] No such file or directory`
- **Solution**: Ensure TIFF files are in the correct directory and filenames match exactly

**Issue**: Gaussian fit fails with `OptimizeWarning: Covariance of the parameters could not be estimated`
- **Solution**: Check that images contain visible worms with clear intensity peaks
- **Solution**: Adjust initial parameter estimates in `fit_gaussian()`

**Issue**: Memory error with large datasets
- **Solution**: Process images in smaller batches
- **Solution**: Set visualization flags to `False` to reduce memory usage

**Issue**: Plots not saving
- **Solution**: Ensure write permissions in the working directory
- **Solution**: Check that figure numbers don't conflict

### Getting Help

For issues specific to:
- **Image processing**: Check PIL/Pillow documentation
- **Statistical analysis**: Consult scipy and statsmodels documentation
- **Plotting**: Refer to matplotlib documentation
- **Numerical operations**: See numpy documentation

---

## Citation

If you use this code or methodology in your research, please cite:

```
[Your Name]. (2024). Comparing Fluorescence and Bioluminescence Microscopy: 
The Effect of Autofluorescence in C. elegans. [Bachelor's Thesis]. 
[Your Institution].
```

---

## License

[Add your chosen license here, e.g., MIT, GPL-3.0, CC-BY-4.0, etc.]

Example:

```
MIT License

Copyright (c) 2024 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

[Full license text...]
```

---

## Acknowledgments

[Add acknowledgments for:
- Thesis supervisors
- Lab members
- Funding sources
- Software/tools used
- etc.]

---

## Contact

**Author**: [Your Name]  
**Email**: [your.email@institution.edu]  
**Institution**: [Your Institution]  
**Department**: [Your
