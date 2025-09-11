#!/usr/bin/env python3
"""
Check for missing files between imagesTr and labelsTr folders.
"""

import os
from pathlib import Path

def get_case_numbers_from_images():
    """Extract case numbers from imagesTr folder."""
    images_dir = Path("nnunet_dataset/imagesTr")
    case_numbers = set()
    
    # Check both Axial and Coronal subdirectories
    for subdir in ["Axial", "Coronal"]:
        subdir_path = images_dir / subdir
        if subdir_path.exists():
            for file in subdir_path.glob("*.png"):
                # Extract case number from case002_0000.png -> case002
                case_name = file.stem.replace("_0000", "")
                case_numbers.add(case_name)
    
    return case_numbers

def get_case_numbers_from_labels():
    """Extract case numbers from labelsTr folder."""
    labels_dir = Path("nnunet_dataset/labelsTr")
    case_numbers = set()
    
    # Check both Axial and Coronal subdirectories
    for subdir in ["Axial", "Coronal"]:
        subdir_path = labels_dir / subdir
        if subdir_path.exists():
            for file in subdir_path.glob("*.png"):
                # Extract case number from case002.png -> case002
                case_name = file.stem
                case_numbers.add(case_name)
    
    return case_numbers

def main():
    """Main function to compare files."""
    print("Checking for missing files between imagesTr and labelsTr...\n")
    
    # Get case numbers from both folders
    image_cases = get_case_numbers_from_images()
    label_cases = get_case_numbers_from_labels()
    
    print(f"Total images found: {len(image_cases)}")
    print(f"Total labels found: {len(label_cases)}")
    
    # Find missing labels (images without corresponding labels)
    missing_labels = image_cases - label_cases
    if missing_labels:
        print(f"\nMissing labels ({len(missing_labels)} files):")
        for case in sorted(missing_labels):
            print(f"  {case}.png")
    else:
        print("\nNo missing labels found.")
    
    # Find extra labels (labels without corresponding images)
    extra_labels = label_cases - image_cases
    if extra_labels:
        print(f"\nExtra labels ({len(extra_labels)} files):")
        for case in sorted(extra_labels):
            print(f"  {case}.png")
    else:
        print("\nNo extra labels found.")
    
    # Summary
    if missing_labels or extra_labels:
        print(f"\nSummary: {len(missing_labels)} missing labels, {len(extra_labels)} extra labels")
    else:
        print("\nAll files match perfectly!")
    
    # Also check the original train folder for reference
    train_dir = Path("train")
    if train_dir.exists():
        original_images = len(list(train_dir.glob("*.jpg")))
        print(f"\nOriginal train folder has {original_images} images")
        
        # Check if any original images weren't converted
        if original_images != len(image_cases):
            print(f"Note: {original_images - len(image_cases)} images from train folder may not have been converted")

if __name__ == "__main__":
    main()