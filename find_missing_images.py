#!/usr/bin/env python3
"""
Find which specific images from the train folder were not converted.
"""

import os
import json
from pathlib import Path

def get_converted_image_names():
    """Get the original image names that were converted."""
    # Load the COCO annotations to see which images were processed
    with open("train/_annotations.coco.json", "r") as f:
        coco_data = json.load(f)
    
    # Get all image filenames from COCO data
    coco_images = {img["file_name"] for img in coco_data["images"]}
    
    return coco_images

def get_all_train_images():
    """Get all image files in the train folder."""
    train_dir = Path("train")
    all_images = set()
    
    for file in train_dir.glob("*.jpg"):
        all_images.add(file.name)
    
    return all_images

def get_converted_cases():
    """Get case numbers that were actually converted to nnU-Net format."""
    images_dir = Path("nnunet_dataset/imagesTr")
    converted_cases = set()
    
    # Check both Axial and Coronal subdirectories
    for subdir in ["Axial", "Coronal"]:
        subdir_path = images_dir / subdir
        if subdir_path.exists():
            for file in subdir_path.glob("*.png"):
                # Extract case number from case002_0000.png -> case002
                case_name = file.stem.replace("_0000", "")
                converted_cases.add(case_name)
    
    return converted_cases

def main():
    """Main function to find missing images."""
    print("Finding missing images from train folder...\n")
    
    # Get all images in train folder
    all_train_images = get_all_train_images()
    print(f"Total images in train folder: {len(all_train_images)}")
    
    # Get images that are in COCO annotations
    coco_images = get_converted_image_names()
    print(f"Images in COCO annotations: {len(coco_images)}")
    
    # Get cases that were actually converted
    converted_cases = get_converted_cases()
    print(f"Cases converted to nnU-Net: {len(converted_cases)}")
    
    # Find images not in COCO annotations
    missing_from_coco = all_train_images - coco_images
    if missing_from_coco:
        print(f"\nImages in train folder but NOT in COCO annotations ({len(missing_from_coco)}):")
        for img in sorted(missing_from_coco):
            print(f"  {img}")
    
    # Find images in COCO but not converted
    # First, map COCO images to expected case names
    coco_case_mapping = {}
    for img_name in coco_images:
        # Extract case number from filename (assuming format like Cyst-X-...)
        if img_name.startswith("Cyst-"):
            parts = img_name.split("-")
            if len(parts) >= 2:
                case_num = int(parts[1])
                case_name = f"case{case_num:03d}"
                coco_case_mapping[case_name] = img_name
    
    expected_cases = set(coco_case_mapping.keys())
    missing_conversions = expected_cases - converted_cases
    
    if missing_conversions:
        print(f"\nImages in COCO annotations but NOT converted to nnU-Net ({len(missing_conversions)}):")
        for case in sorted(missing_conversions):
            original_name = coco_case_mapping.get(case, "unknown")
            print(f"  {case} (original: {original_name})")
    
    print(f"\nSummary:")
    print(f"  - {len(missing_from_coco)} images not in COCO annotations")
    print(f"  - {len(missing_conversions)} images not converted to nnU-Net")
    print(f"  - Total missing: {len(missing_from_coco) + len(missing_conversions)}")

if __name__ == "__main__":
    main()