"""
Prostate MRI Segmentation Visualizer
Author: Aiswarya
Lab: AI Med Lab
"""

import os
import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.ndimage import zoom
import cv2


# Configuration — edit patient IDs and base path

BASE_DIR = "C:/Users/AISWARYA/Desktop/aimed/task_1"

PATIENTS = [
    {"id": "10005", "folder": "10005-20260310T144531Z-1-001"},
    {"id": "10040", "folder": "10040-20260310T144526Z-1-001"},
    {"id": "10043", "folder": "10043-20260310T144526Z-1-001"},
    {"id": "10048", "folder": "10048-20260310T144526Z-1-001"},
]

OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)


# Helper functions

def load_nifti(path: str) -> np.ndarray:
    """Load a NIfTI file and return as a NumPy array."""
    img = sitk.ReadImage(path)
    return sitk.GetArrayFromImage(img)


def resize_mask(mask: np.ndarray, target_shape: tuple) -> np.ndarray:
    """
    Resize a binary mask to match a target shape using nearest-neighbour
    interpolation (preserves label values).
    """
    zoom_factors = tuple(t / s for t, s in zip(target_shape, mask.shape))
    resized = zoom(mask, zoom_factors, order=0)
    return (resized > 0.5).astype(np.uint8)


def normalize_to_uint8(img: np.ndarray) -> np.ndarray:
    """Min-max normalize a 2-D slice to the 0–255 range."""
    img = img.astype(np.float32)
    img = (img - img.min()) / (img.max() - img.min() + 1e-8) * 255
    return img.astype(np.uint8)


def best_slice(mask_3d: np.ndarray) -> int:
    """Return the axial slice index with the most mask pixels."""
    return int(np.argmax([mask_3d[i].sum() for i in range(mask_3d.shape[0])]))


def draw_contour_overlay(gray_slice: np.ndarray,
                         mask_slice: np.ndarray,
                         color_bgr=(0, 0, 255),
                         thickness=2) -> np.ndarray:
    """Draw a coloured contour of *mask_slice* on top of *gray_slice*."""
    color_img = cv2.cvtColor(gray_slice, cv2.COLOR_GRAY2BGR)
    mask_u8 = (mask_slice > 0).astype(np.uint8) * 255
    contours, _ = cv2.findContours(mask_u8, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(color_img, contours, -1, color_bgr, thickness)
    return color_img


# Per-patient processing

def process_patient(patient: dict) -> None:
    pid = patient["id"]
    data_dir = os.path.join(BASE_DIR, patient["folder"], pid)

    print(f"\n{'='*50}")
    print(f"Processing patient: {pid}")
    print(f"{'='*50}")

    # Load volumes
    t2w = load_nifti(os.path.join(data_dir, f"{pid}_t2w.nii.gz"))
    gland = load_nifti(os.path.join(data_dir, f"{pid}_gland.nii.gz"))

    print(f"  T2w shape  : {t2w.shape}")
    print(f"  Gland shape: {gland.shape}")

    # Align mask to T2w resolution
    gland_r = resize_mask(gland, t2w.shape)
    print(f"  Gland (resized): {gland_r.shape}")

    # Select most informative axial slice
    sl = best_slice(gland_r)
    print(f"  Best slice index: {sl}")

    t2w_sl = normalize_to_uint8(t2w[sl])
    mask_sl = gland_r[sl]

    # ── Part A: mask overlay (prostate only) 
    masked = np.where(mask_sl > 0, t2w_sl, 0)

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    fig.suptitle(f"Patient {pid} — T2w Prostate Segmentation", fontsize=13)

    axes[0].imshow(t2w_sl, cmap="gray")
    axes[0].set_title("(a) Original Image")
    axes[0].axis("off")

    axes[1].imshow(masked, cmap="gray")
    axes[1].set_title("(b) Mask overlaid — prostate only")
    axes[1].axis("off")

    plt.tight_layout()
    part_a_path = os.path.join(OUTPUT_DIR, f"{pid}_part_a_mask_overlay.png")
    plt.savefig(part_a_path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"  Saved Part A → {part_a_path}")

    # ── Part B: red contour outline 
    contour_img = draw_contour_overlay(t2w_sl, mask_sl)

    plt.figure(figsize=(5, 5))
    plt.imshow(cv2.cvtColor(contour_img, cv2.COLOR_BGR2RGB))
    plt.title(f"Patient {pid} — Prostate Outline on T2w Image")
    plt.axis("off")

    part_b_path = os.path.join(OUTPUT_DIR, f"{pid}_part_b_contour.png")
    cv2.imwrite(part_b_path, contour_img)
    plt.show()
    print(f"  Saved Part B → {part_b_path}")


# Main

if __name__ == "__main__":
    for patient in PATIENTS:
        process_patient(patient)

    print("\n All patients processed. Outputs saved to:", OUTPUT_DIR)
