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

The analysis pipeline (`14_FINAL_x_y_time.py`) uses modular functions to process fluorescence microscopy images and quantify autofluorescence development over time.

### Workflow Overview

1. **Image Loading** → Load TIFF images and convert to numpy arrays
2. **Y-Axis Analysis** → Extract vertical columns, average them, and create intensity profile
3. **Background Determination** → Fit Gaussian to identify background and worm position
4. **Background Correction** → Replace artifacts and subtract background
5. **X-Axis Analysis** → Extract horizontal lines from worm region and create intensity profile
6. **Total Intensity** → Calculate mean intensity per pixel in worm region
7. **Statistical Analysis** → Compute median and MAD for each age group
8. **Visualization** → Generate temporal plots showing autofluorescence trends

### Key Functions

**Data Processing:**
- `load_image()` - Load and convert TIFF images
- `extract_columns()` / `extract_and_crop_lines()` - Extract vertical/horizontal image slices
- `remove_zero_columns()` - Remove artifacts from image straightening
- `average_columns()` / `average_lines()` - Create mean intensity profiles

**Background Analysis:**
- `gauss_function()` - Gaussian model for curve fitting
- `fit_gaussian()` - Fit curve to determine background (baseline parameter) and worm position (center and sigma)
- `replace_zeros_with_background()` - Fill artifacts with background value
- `background_subtraction()` - Normalize intensities: (intensity - background) / background

  <p align="center">

  <img src="https://github.com/user-attachments/assets/60245e4c-61e0-485c-879d-fa47b548d3bf" alt="Image 4" width="500"/>
  <br>
  <em> Figure 4: Averaged spatial intensity over the y-axis. A Gaussian is fitted to the data. Its baseline represents the computed background value. The worm's y-coordinates are determined by the range [x₀ - 3σ, x₀ + 3σ], where x₀ designates the Gaussian's median and σ the standard deviation. </em>
</p>


**Quantification:**
- `calculate_total_intensity()` - Compute mean intensity in worm region (x0 ± 3σ)
- `calculate_statistics()` - Compute median, mean, std, and MAD for age groups

**Visualization:**
- `plot_y_intensity_distribution()` / `plot_x_intensity_distribution()` - Spatial profiles
- `plot_individual_points()` - Scatter plot of all measurements
- `plot_statistics()` - Statistical summary with error bars
- `plot_combined()` - Two-panel view combining both

  <p align="center">

  <img src="https://github.com/user-attachments/assets/d503b15b-d35a-48bf-bbe3-7be7d7d709cb" alt="Image 4" width="700"/>
  <br>
  <em>Figure 5: (left) Fluorescence image of a worm's body-area near its gonad with a discernible neuron. The y-axis is illustrated using a blue arrow. (right) Spatial distribution of the mean intensity along the y-axis. A peak species the neuron's position, marked by a red arrow..</em>
</p>



**Main Orchestration:**
- `process()` - Executes complete analysis pipeline for one image

### Analysis Details

**Gaussian Fitting**: The script fits a bell curve to the y-axis intensity profile. The baseline parameter defines background autofluorescence; the center and width define the worm region (x0 ± 3σ covers ~99.7% of the worm).

**Background Normalization**: Converting absolute intensities to `(intensity - background) / background` allows fair comparison between samples imaged under different conditions.

**Region of Interest**: Cropping to x0 ± 3σ focuses analysis on the worm while excluding most background, improving signal-to-noise ratio.

**Robust Statistics**: Median Absolute Deviation (MAD) provides outlier-resistant variability measures, important given biological variation between individual worms.

### Results Interpretation

The analysis reveals:
- **Progressive accumulation**: Total intensities increase systematically with age
- **Anatomical differences**: Tails and bodies show different autofluorescence patterns
- **Strain variability**: Extrachromosomal strains have larger error bars and more scatter
- **Wavelength effects**: GFP and mCherry filters show different autofluorescence characteristics
- **Ratio decline**: Neuronal signal becomes progressively masked by autofluorescence

![Total intensities](images/total_intensity_comparison.png)

*Figure: Total intensities increase with age across all conditions, with strain-specific variability patterns.*

---

## Repository Structure
