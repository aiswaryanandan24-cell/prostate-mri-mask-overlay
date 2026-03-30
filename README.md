# Prostate MRI Mask Overlay and Contour Visualization

## Overview
This project was developed as part of my onboarding task in an AI medical imaging lab. The goal was to process prostate MRI data and corresponding segmentation masks to visualize the region of interest (ROI) and generate contour overlays for better anatomical understanding.

The pipeline uses Python-based medical imaging and computer vision libraries to handle 3D MRI data and convert it into meaningful 2D visual outputs.

---

## Objectives
For each patient MRI dataset:

- Load **T2-weighted (T2W) MRI volume**
- Load **prostate gland segmentation mask**
- Identify the slice with the largest prostate region
- Generate:
  - ROI-only visualization (masked prostate region)
  - Contour overlay on original MRI image
- Save outputs as PNG images

---

## Technologies Used
- **SimpleITK** – Medical image loading (.nii.gz)
- **NumPy** – Array manipulation
- **SciPy** – Mask resizing (if needed)
- **OpenCV** – Contour detection and drawing
- **Matplotlib** – Visualization and image saving

---


## Repository Structure

```
prostate-mri-mask-overlay/
│
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   └── prostate_overlay.py
│
├── outputs/
│   ├── 10005/
│   │   ├── masked_roi.png
│   │   └── prostate_outline.png
│   ├── 10040/
│   │   ├── masked_roi.png
│   │   └── prostate_outline.png
│   ├── 10043/
│   │   ├── masked_roi.png
│   │   └── prostate_outline.png
│   └── 10048/
│       ├── masked_roi.png
│       └── prostate_outline.png
│
└── data/
    └── README.txt

```

## Requirements

```
SimpleITK
numpy
matplotlib
scipy
opencv-python
```

Install all at once:
```bash
pip install SimpleITK numpy matplotlib scipy opencv-python
```

---

## How It Works

### Step 1 — Load NIfTI files
T2w MRI volumes and gland masks are loaded using `SimpleITK` and converted to NumPy arrays.

### Step 2 — Resize mask
The gland mask is often at a different resolution than the T2w image. It is resampled using `scipy.ndimage.zoom` with **nearest-neighbour interpolation** (order=0) to preserve binary label values.

### Step 3 — Select best slice
The axial slice with the **most mask pixels** is automatically chosen — this guarantees the prostate is well-represented in the displayed cross-section.

### Step 4 — Part A: Mask overlay
```python
masked = np.where(mask_slice > 0, t2w_normalized, 0)
```
Pixels outside the prostate are set to black; only the segmented region is shown.

### Step 5 — Part B: Contour overlay
OpenCV's `findContours` + `drawContours` is used to extract and draw the prostate boundary in **red** directly on a colour copy of the T2w slice. The result is saved as a PNG.

---

## Key Libraries

| Library | Purpose |
|---|---|
| `SimpleITK` | Read/write NIfTI medical images |
| `NumPy` | Array operations |
| `SciPy` | 3D mask resampling via zoom |
| `Matplotlib` | Display and save image panels |
| `OpenCV` | Contour detection and drawing |

---

## References & Learning Resources

- [Medical Image Processing with Python — The AI Summer](https://theaisummer.com/medical-image-python/)
- [Image Processing with Python — Coursera](https://www.coursera.org/projects/image-processing-with-python)
- [SimpleITK Documentation](https://simpleitk.readthedocs.io/)
- [OpenCV Documentation](https://docs.opencv.org/)

---

## 👩‍💻 Author

**Aiswarya Perumbilly**  
AI Med Lab -Research Assistant  

---

