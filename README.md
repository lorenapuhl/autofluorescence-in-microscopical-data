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
