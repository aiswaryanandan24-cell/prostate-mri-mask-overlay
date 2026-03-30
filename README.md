# 🧠 Prostate MRI Segmentation Visualizer

> **AI Med Lab — Task 1** | Medical Image Processing with SimpleITK & OpenCV

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://www.python.org/)
[![SimpleITK](https://img.shields.io/badge/SimpleITK-medical%20imaging-green)](https://simpleitk.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-vision-red)](https://opencv.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Overview

This project is my first task at the **AI Med Lab**, focused on working with real prostate MRI data. The goal is to:

- **Load** T2-weighted (T2w) MRI volumes and their corresponding prostate gland segmentation masks (NIfTI format)
- **Part A** — Overlay the segmentation mask to isolate and display only the prostate region
- **Part B** — Draw a red contour outline of the prostate boundary on the original T2w image and save it as a PNG

The pipeline is run on **4 patient datasets** (IDs: 10005, 10040, 10043, 10048).

---

## 🖼️ Sample Results

| (a) Original T2w Slice | (b) Prostate Region Only | (B) Contour Outline |
|:---:|:---:|:---:|
| Full axial MRI slice | Masked to show prostate | Red outline on T2w |

> *Images are auto-selected as the axial slice with the largest prostate cross-section.*

---

## 🗂️ Repository Structure

```
prostate-mri-segmentation/
│
├── prostate_mri_visualizer.py   # Main script (clean, refactored)
├── README.md
├── requirements.txt
│
└── outputs/                     # Auto-created on first run
    ├── 10005_part_a_mask_overlay.png
    ├── 10005_part_b_contour.png
    ├── 10040_part_a_mask_overlay.png
    ├── 10040_part_b_contour.png
    └── ...
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/prostate-mri-segmentation.git
cd prostate-mri-segmentation
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Download the data
Get the prostate MRI dataset (4 patients) from the link provided by the lab.  
Place it so your folder structure looks like:

```
aimed/task_1/
├── 10005-20260310T144531Z-1-001/
│   └── 10005/
│       ├── 10005_t2w.nii.gz
│       └── 10005_gland.nii.gz
├── 10040-.../
│   └── 10040/
│       ├── 10040_t2w.nii.gz
│       └── 10040_gland.nii.gz
...
```

### 4. Update the base path
In `prostate_mri_visualizer.py`, update:
```python
BASE_DIR = "C:/path/to/your/aimed/task_1"
```

### 5. Run
```bash
python prostate_mri_visualizer.py
```

---

## 📦 Requirements

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

## 🔬 How It Works

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

## 🧪 Key Libraries

| Library | Purpose |
|---|---|
| `SimpleITK` | Read/write NIfTI medical images |
| `NumPy` | Array operations |
| `SciPy` | 3D mask resampling via zoom |
| `Matplotlib` | Display and save image panels |
| `OpenCV` | Contour detection and drawing |

---

## 📚 References & Learning Resources

- [Medical Image Processing with Python — The AI Summer](https://theaisummer.com/medical-image-python/)
- [Image Processing with Python — Coursera](https://www.coursera.org/projects/image-processing-with-python)
- [SimpleITK Documentation](https://simpleitk.readthedocs.io/)
- [OpenCV Documentation](https://docs.opencv.org/)

---

## 👩‍💻 Author

**Aiswarya**  
AI Med Lab Intern  

---

*First task completed ✅ — Prostate MRI segmentation visualization across 4 patient datasets.*
