#!/usr/bin/env python3
"""
Organize label folders into Axial and Coronal subdirectories
to match the imagesTr folder structure.
"""

import os
import shutil
from pathlib import Path

def get_image_organization():
    """Get the organization of images from imagesTr folder."""
    images_dir = Path("nnunet_dataset/imagesTr")
    
    axial_files = set()
    coronal_files = set()
    
    # Get axial files
    axial_dir = images_dir / "Axial"
    if axial_dir.exists():
        for file in axial_dir.glob("*.png"):
            # Convert from case002_0000.png to case002.png format
            case_name = file.stem.replace("_0000", "") + ".png"
            axial_files.add(case_name)
    
    # Get coronal files
    coronal_dir = images_dir / "Coronal"
    if coronal_dir.exists():
        for file in coronal_dir.glob("*.png"):
            # Convert from case001_0000.png to case001.png format
            case_name = file.stem.replace("_0000", "") + ".png"
            coronal_files.add(case_name)
    
    return axial_files, coronal_files

def organize_label_folder(label_folder_name, axial_files, coronal_files):
    """Organize a specific label folder into Axial and Coronal subdirectories."""
    label_dir = Path(f"nnunet_dataset/{label_folder_name}")
    
    if not label_dir.exists():
        print(f"Folder {label_folder_name} does not exist, skipping...")
        return
    
    print(f"\nOrganizing {label_folder_name}...")
    
    # Create Axial and Coronal subdirectories
    axial_dir = label_dir / "Axial"
    coronal_dir = label_dir / "Coronal"
    
    axial_dir.mkdir(exist_ok=True)
    coronal_dir.mkdir(exist_ok=True)
    
    # Move files to appropriate subdirectories
    axial_count = 0
    coronal_count = 0
    unmatched_count = 0
    
    for file in label_dir.glob("*.png"):
        if file.name in axial_files:
            shutil.move(str(file), str(axial_dir / file.name))
            axial_count += 1
        elif file.name in coronal_files:
            shutil.move(str(file), str(coronal_dir / file.name))
            coronal_count += 1
        else:
            print(f"Warning: {file.name} not found in either Axial or Coronal images")
            unmatched_count += 1
    
    print(f"  Moved {axial_count} files to Axial/")
    print(f"  Moved {coronal_count} files to Coronal/")
    if unmatched_count > 0:
        print(f"  {unmatched_count} files could not be matched")

def main():
    """Main function to organize all label folders."""
    print("Organizing label folders to match imagesTr structure...")
    
    # Get the organization pattern from imagesTr
    axial_files, coronal_files = get_image_organization()
    
    print(f"Found {len(axial_files)} axial cases and {len(coronal_files)} coronal cases")
    
    # Organize each label folder
    label_folders = ["labelsTr", "labelsTr_colored", "labelsTr_visible"]
    
    for folder in label_folders:
        organize_label_folder(folder, axial_files, coronal_files)
    
    print("\nLabel organization complete!")
    print("\nFinal structure:")
    for folder in label_folders:
        folder_path = Path(f"nnunet_dataset/{folder}")
        if folder_path.exists():
            print(f"  {folder}/")
            axial_path = folder_path / "Axial"
            coronal_path = folder_path / "Coronal"
            if axial_path.exists():
                axial_count = len(list(axial_path.glob("*.png")))
                print(f"    Axial/ ({axial_count} files)")
            if coronal_path.exists():
                coronal_count = len(list(coronal_path.glob("*.png")))
                print(f"    Coronal/ ({coronal_count} files)")

if __name__ == "__main__":
    main()