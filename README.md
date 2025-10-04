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

- **Model organism**: Transgenic strains of *C. elegans* with mNeonGreen-labelled touch receptor neurons. Ideally, fluorescence microsocopy should only reveal labelled features, i.e. in this case, touch-receptor neurons
- **Imaging techniques**: Fluorescence microscopy vs. bioluminescence microscopy
- **Age progression**: Samples imaged at different developmental stages to assess autofluorescence accumulation. Autofluorescence denotes the noise effect of other biological features emitting the same light wavelengths as the labelled neurons. Therefore, the neuron's signal is blurred and covered.
- **Analysis**: Spatial intensity distributions and signal quantification across body parts.



- <p align="center">

  <img src="https://github.com/user-attachments/assets/1d87646f-eb5d-4ad8-a851-a4bcb8f8afaf" alt="Image 1" width="700"/>
  <br>
  <em>Figure 3: Fluorescence microscopy images of mNeonGreen-labelled C. elegans samples at different ages. The maturity levels are denoted in hours, and using the respective stage's names L2, young adult (yound ad) and adult (ad). The left pictures show the anterior neurons in the worms' bodies, whereas the right images depict the posterior neurons in the worms' tails. While young worms clearly reveal the labelled neurons, older worms feature higher autofluorescence, which increasingly covers the neuron's signals.</em>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/bdf4aa18-1075-4c71-8560-9544e1812f99" alt="Image 2" width="700"/>
  <br>
  <em>Figure 4: Bioluminescence images of mNeonGreen-labelled neurons for samples of different ages. The maturity is given in hours and the respective stages L1, L2, young adult and adult. Bioluminescence microscopy techniques are more subtle, but do not face the problem of autofluorescence. </em>
</p>

---

## Analysis Pipeline

The analysis pipeline (`main.py`) uses modular functions to process fluorescence microscopy images and quantify autofluorescence development over time.

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

  <p align="center">

  <img src="https://github.com/user-attachments/assets/f12aa9d3-9fff-4a27-81ba-7134f1f0f86c" alt="Image 4" width="500"/>
  <br>
  <em> Figure 5: Not every column is utilised to determine the average spatial intensity, used for the Gaussian fit. The red arrows indicate those, which contain zero-value pixels. These are provisionally excluded from the calculations.</em>
</p>


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
- `plot_combined()` - Two-panel view combining both - scatter plots and statistical summary with errorbars

  <p align="center">

  <img src="https://github.com/user-attachments/assets/d503b15b-d35a-48bf-bbe3-7be7d7d709cb" alt="Image 4" width="700"/>
  <br>
  <em>Figure 6: (left) Fluorescence image of a worm's body-area near its gonad with a discernible neuron. The y-axis is illustrated using a blue arrow. (right) Spatial distribution of the mean intensity along the y-axis. A peak species the neuron's position, marked by a red arrow..</em>
</p>

  <p align="center">

  <img src="https://github.com/user-attachments/assets/46a7045e-67bf-47ee-8b8a-061737263188" alt="Image 4" width="700"/>
  <br>
  <em> Figure 7: (left) Fluorescence microscopy image of a worm's mid-body area. Using a blue arrow, the image's x-axis is denoted, while a red arrows marks the touch-receptor neuron. (right) Respective spatial intensity distribution over the x-axis. The x-axis is denoted using a blue. A signicant peak, at the the neuron's x-coordinate is marked by a red arrow.</em>
</p>


**Main Orchestration:**
- `process()` - Executes complete analysis pipeline for one image

---

## Code Structure and Configuration

The refactored script uses boolean flags for flexible control:

- `plot_y_inten`: Generate y-axis spatial intensity distribution plots
- `same_graph_y`: Combine multiple y-axis plots in one figure
- `plotgauss`: Visualize Gaussian fits
- `plot_x_inten`: Generate x-axis spatial intensity distribution plots
- `same_graph_x`: Combine multiple x-axis plots in one figure
- `plot_points`: Show scatter plot of individual intensity measurements
- `plot_stats`: Show statistical summary with error bars
- `plot_both`: Show combined view of points and statistics

---

### Analysis Details

**Gaussian Fitting**: The script fits a bell curve to the y-axis intensity profile. The baseline parameter defines background autofluorescence; the center and width define the worm region (x0 ± 3σ covers ~99.7% of the worm).

**Background Normalization**: Converting absolute intensities to `(intensity - background) / background` allows fair comparison between samples imaged under different conditions.

**Region of Interest**: Cropping to x0 ± 3σ focuses analysis on the worm while excluding most background, improving signal-to-noise ratio.

**Robust Statistics**: Median Absolute Deviation (MAD) provides outlier-resistant variability measures, important given biological variation between individual worms.

---

## Evaluation

The analysis pipeline consistently reveals several key patterns across experimental conditions:

**Progressive Autofluorescence Accumulation**: Total intensities increase systematically with age across all samples. This demonstrates that autofluorescent compounds accumulate in aging worms, progressively increasing the background fluorescence signal. The rate of increase varies between conditions but the trend is universal.



  <p align="center">

  <img src="https://github.com/user-attachments/assets/0fb61e44-5ce1-482c-9d53-ea24f6e5791e" alt="Image 4" width="700"/>
  <br>
  <em> Figure 8: Spatial intensity distributions over the y-axis for worms of increasing ages using fluorescence microscopy. One can qualitiatively infer, that while young worms mainly showcase high intensities in the neuron's region, older worms feature higher overall intensities (autofluorescence) </em>
</p>


  <p align="center">

  <img src="https://github.com/user-attachments/assets/af611764-7947-4aba-b340-4e7352c776b2" alt="Image 4" width="700"/>
  <br>
  <em> Figure 9: Total intensities at different ages, using the GFP filtercube. Individual data-points, as well as medians and median standard deviations are depicted. (right) Intensities in the tails. (left) Intensities in the bodies.
Figure </em>
</p>



  <p align="center">

  <img src= "https://github.com/user-attachments/assets/85dae11f-46e1-498b-867e-7ee86b421205" alt="Image 4" width="700"/>
  <br>
  <em> Figure 10: Spatial intensity distributions over the y-axis for worms of increasing ages using bioluminescence microsocopy. While fluorescence microscopy features increasing autofluorescence, intensity distributions using bioluminescence microscopy stay concentrated around the labelled neuron. </em>
</p>



### 11. Neuron-to-Autofluorescence Ratio

We further examine how autofluorescence affects the visibility of intentionally labeled neuronal signals. The neuron-to-autofluorescence ratio analysis involves:

1. Separately quantifying the fluorescence intensity from labeled touch receptor neurons
2. Calculating the ratio between neuronal signal and total autofluorescence
3. Tracking how this ratio changes as worms age

This ratio directly measures signal visibility: a high ratio means the neuronal signal stands out clearly against background autofluorescence, while a low ratio indicates the signal is increasingly masked by autofluorescence.


  <p align="center">

  <img src= "https://github.com/user-attachments/assets/96ae548f-df51-4639-ad8a-7d159dd44d93" alt="Image 4" width="700"/>
  <br>
  <em> Figure 11: Autofluorescence-to-noise ratios for the extrachromosomal strain MSB557 at different ages. Individual data-points, as well as medians and median standard deviations are depicted. (right) Autofluorescence-to-noise ratios in tails. (left) Autofluorescence-to-noise ratios in bodies.</em>
</p>

The results show a steady decrease in signal-to-autofluorescence ratio over time. This demonstrates that autofluorescence accumulates more rapidly than any changes in neuronal signal intensity, progressively masking the labeled neurons. This progressive signal loss is the core problem that motivates the search for alternative imaging approaches like bioluminescence microscopy.


---

## Repository Structure
