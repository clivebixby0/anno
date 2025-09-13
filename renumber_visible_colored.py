#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

def renumber_directory(base_dir, subfolder):
    """
    Renumber files in a directory to start from case001.png
    """
    dir_path = os.path.join(base_dir, subfolder)
    
    if not os.path.exists(dir_path):
        print(f"Directory {dir_path} does not exist, skipping...")
        return
    
    # Get all PNG files and sort them
    png_files = [f for f in os.listdir(dir_path) if f.endswith('.png')]
    png_files.sort()
    
    if not png_files:
        print(f"No PNG files found in {dir_path}")
        return
    
    print(f"Processing {len(png_files)} files in {dir_path}")
    
    # Create temporary directory for renaming
    temp_dir = os.path.join(dir_path, 'temp_rename')
    os.makedirs(temp_dir, exist_ok=True)
    
    try:
        # Move files to temp directory with new names
        for i, filename in enumerate(png_files, 1):
            old_path = os.path.join(dir_path, filename)
            new_filename = f"case{i:03d}.png"
            temp_path = os.path.join(temp_dir, new_filename)
            
            shutil.move(old_path, temp_path)
            print(f"Renamed {filename} -> {new_filename}")
        
        # Move files back to original directory
        for filename in os.listdir(temp_dir):
            temp_path = os.path.join(temp_dir, filename)
            final_path = os.path.join(dir_path, filename)
            shutil.move(temp_path, final_path)
        
        # Remove temporary directory
        os.rmdir(temp_dir)
        print(f"Successfully renumbered {len(png_files)} files in {subfolder}")
        
    except Exception as e:
        print(f"Error processing {dir_path}: {e}")
        # Try to clean up temp directory if it exists
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

def main():
    # Base directories to process
    base_dirs = [
        'nnunet_dataset/labelsTr_visible',
        'nnunet_dataset/labelsTr_colored'
    ]
    
    subfolders = ['Axial', 'Coronal']
    
    for base_dir in base_dirs:
        print(f"\n=== Processing {base_dir} ===")
        for subfolder in subfolders:
            print(f"\n--- Processing {subfolder} subfolder ---")
            renumber_directory(base_dir, subfolder)
    
    print("\nRenumbering complete for visible and colored labels!")

if __name__ == "__main__":
    main()