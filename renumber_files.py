import os
import shutil
from pathlib import Path

def renumber_files():
    root = Path("/Users/carlmacabales/Downloads/Kidney Cyst Coco Segmentation/nnunet_dataset")
    
    # Process both Axial and Coronal folders
    for folder_type in ["Axial", "Coronal"]:
        print(f"\nProcessing {folder_type} folder...")
        
        # Get paths
        images_path = root / "imagesTr" / folder_type
        labels_path = root / "labelsTr" / folder_type
        
        if not images_path.exists() or not labels_path.exists():
            print(f"Skipping {folder_type} - missing directories")
            continue
            
        # Get all label files (these will be our reference for numbering)
        label_files = sorted([f for f in labels_path.glob("*.png")])
        
        if not label_files:
            print(f"No label files found in {folder_type}")
            continue
            
        print(f"Found {len(label_files)} label files in {folder_type}")
        
        # Create temporary directories for renaming
        temp_images_path = images_path.parent / f"{folder_type}_temp_images"
        temp_labels_path = labels_path.parent / f"{folder_type}_temp_labels"
        
        temp_images_path.mkdir(exist_ok=True)
        temp_labels_path.mkdir(exist_ok=True)
        
        # Renumber files starting from 1
        for i, label_file in enumerate(label_files, 1):
            # Extract the case number from the label file
            case_name = label_file.stem  # e.g., "case002"
            
            # Find corresponding image file
            image_file = images_path / f"{case_name}_0000.png"
            
            if not image_file.exists():
                print(f"Warning: No corresponding image file for {label_file.name}")
                continue
                
            # New names following nnU-Net convention
            new_case_number = f"{i:03d}"  # 001, 002, 003, etc.
            new_image_name = f"case{new_case_number}_0000.png"
            new_label_name = f"case{new_case_number}.png"
            
            # Copy to temp directories with new names
            shutil.copy2(image_file, temp_images_path / new_image_name)
            shutil.copy2(label_file, temp_labels_path / new_label_name)
            
            print(f"Renamed: {case_name} -> case{new_case_number}")
        
        # Remove original files and replace with renamed ones
        print(f"Replacing original files in {folder_type}...")
        
        # Clear original directories
        for f in images_path.glob("*.png"):
            f.unlink()
        for f in labels_path.glob("*.png"):
            f.unlink()
            
        # Move renamed files back
        for f in temp_images_path.glob("*.png"):
            shutil.move(str(f), images_path / f.name)
        for f in temp_labels_path.glob("*.png"):
            shutil.move(str(f), labels_path / f.name)
            
        # Remove temp directories
        temp_images_path.rmdir()
        temp_labels_path.rmdir()
        
        print(f"Completed renumbering for {folder_type}")
    
    print("\nRenumbering complete!")

if __name__ == "__main__":
    renumber_files()