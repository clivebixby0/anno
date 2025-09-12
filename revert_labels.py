#!/usr/bin/env python3

import os
import numpy as np
from PIL import Image

def revert_labels():
    """Revert labelsTr_visible and labelsTr_colored back to original values"""
    
    base_dir = "nnunet_dataset"
    
    # Define the directories and their target mappings
    revert_configs = {
        "labelsTr_visible": {0: 0, 1: 128, 2: 255},  # Revert to grayscale visibility
        "labelsTr_colored": {0: 0, 1: 200, 2: 255}   # Revert to colored visibility
    }
    
    for dir_name, mapping in revert_configs.items():
        dir_path = os.path.join(base_dir, dir_name)
        
        if not os.path.exists(dir_path):
            print(f"Directory {dir_path} does not exist, skipping...")
            continue
            
        print(f"\nReverting {dir_name}...")
        
        # Get all PNG files
        png_files = [f for f in os.listdir(dir_path) if f.endswith('.png')]
        
        for i, filename in enumerate(png_files):
            file_path = os.path.join(dir_path, filename)
            
            try:
                # Load the image
                img = Image.open(file_path)
                img_array = np.array(img)
                
                # Create new array with reverted values
                new_array = np.zeros_like(img_array)
                
                for old_val, new_val in mapping.items():
                    new_array[img_array == old_val] = new_val
                
                # Save the reverted image
                new_img = Image.fromarray(new_array.astype(np.uint8))
                new_img.save(file_path)
                
                if (i + 1) % 50 == 0:
                    print(f"  Processed {i + 1}/{len(png_files)} files")
                    
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue
        
        print(f"Completed reverting {len(png_files)} files in {dir_name}")
    
    # Verify the results
    print("\nVerifying reverted values...")
    for dir_name in revert_configs.keys():
        dir_path = os.path.join(base_dir, dir_name)
        if os.path.exists(dir_path):
            # Check first 3 files
            png_files = sorted([f for f in os.listdir(dir_path) if f.endswith('.png')])[:3]
            for filename in png_files:
                file_path = os.path.join(dir_path, filename)
                img = Image.open(file_path)
                unique_vals = np.unique(np.array(img))
                print(f"  {dir_name}/{filename}: {unique_vals}")

if __name__ == "__main__":
    revert_labels()
    print("\nReversion complete!")