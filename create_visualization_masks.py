#!/usr/bin/env python3

import os
import numpy as np
from PIL import Image

def create_visualization_masks():
    """Create proper grayscale and colored RGB versions from labelsTr"""
    
    base_dir = "nnunet_dataset"
    source_dir = os.path.join(base_dir, "labelsTr")
    
    # Define output directories and their configurations
    configs = {
        "labelsTr_visible": {
            "type": "grayscale",
            "mapping": {0: 0, 1: 128, 2: 255},  # Background: black, Class1: gray, Class2: white
            "description": "Grayscale visibility version"
        },
        "labelsTr_colored": {
            "type": "rgb",
            "mapping": {
                0: [0, 0, 0],       # Background: black
                1: [255, 0, 0],     # Class 1 (kidney): flat red
                2: [0, 200, 255]    # Class 2 (cyst): cyan
            },
            "description": "Colored RGB version"
        }
    }
    
    if not os.path.exists(source_dir):
        print(f"Source directory {source_dir} does not exist!")
        return
    
    # Get all PNG files from source
    png_files = [f for f in os.listdir(source_dir) if f.endswith('.png')]
    print(f"Found {len(png_files)} PNG files in {source_dir}")
    
    for config_name, config in configs.items():
        output_dir = os.path.join(base_dir, config_name)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\nCreating {config['description']} in {config_name}...")
        
        for i, filename in enumerate(png_files):
            source_path = os.path.join(source_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            try:
                # Load source mask
                source_img = Image.open(source_path)
                source_array = np.array(source_img)
                
                if config["type"] == "grayscale":
                    # Create grayscale version
                    output_array = np.zeros_like(source_array, dtype=np.uint8)
                    
                    for class_id, gray_value in config["mapping"].items():
                        output_array[source_array == class_id] = gray_value
                    
                    # Save as grayscale
                    output_img = Image.fromarray(output_array, mode='L')
                    
                elif config["type"] == "rgb":
                    # Create RGB version
                    h, w = source_array.shape
                    output_array = np.zeros((h, w, 3), dtype=np.uint8)
                    
                    for class_id, rgb_color in config["mapping"].items():
                        mask = source_array == class_id
                        output_array[mask] = rgb_color
                    
                    # Save as RGB
                    output_img = Image.fromarray(output_array, mode='RGB')
                
                output_img.save(output_path)
                
                if (i + 1) % 50 == 0:
                    print(f"  Processed {i + 1}/{len(png_files)} files")
                    
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue
        
        print(f"Completed creating {len(png_files)} files in {config_name}")
    
    # Verify the results
    print("\nVerifying created visualization masks...")
    for config_name in configs.keys():
        output_dir = os.path.join(base_dir, config_name)
        if os.path.exists(output_dir):
            # Check first 3 files
            png_files_check = sorted([f for f in os.listdir(output_dir) if f.endswith('.png')])[:3]
            for filename in png_files_check:
                file_path = os.path.join(output_dir, filename)
                img = Image.open(file_path)
                img_array = np.array(img)
                
                if len(img_array.shape) == 2:  # Grayscale
                    unique_vals = np.unique(img_array)
                    print(f"  {config_name}/{filename}: {unique_vals} (grayscale)")
                else:  # RGB
                    # Show unique RGB combinations
                    unique_colors = np.unique(img_array.reshape(-1, 3), axis=0)
                    print(f"  {config_name}/{filename}: {len(unique_colors)} unique colors (RGB)")
                    for color in unique_colors:
                        print(f"    RGB: {color}")

if __name__ == "__main__":
    create_visualization_masks()
    print("\nVisualization mask creation complete!")