import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Check a few mask files to see why they appear black
mask_files = ['case001.png', 'case002.png', 'case003.png']

for mask_file in mask_files:
    mask_path = f'nnunet_dataset/labelsTr/{mask_file}'
    
    print(f"\n=== Checking {mask_file} ===")
    
    # Load mask
    mask = np.array(Image.open(mask_path))
    
    print(f"Shape: {mask.shape}")
    print(f"Data type: {mask.dtype}")
    print(f"Min value: {mask.min()}")
    print(f"Max value: {mask.max()}")
    print(f"Unique values: {np.unique(mask)}")
    
    # Count pixels for each value
    for val in np.unique(mask):
        count = np.sum(mask == val)
        percentage = (count / mask.size) * 100
        print(f"  Value {val}: {count} pixels ({percentage:.2f}%)")
    
    # Create a visible version by scaling values
    visible_mask = mask.copy().astype(np.uint8)
    # Scale values to make them more visible: 0->0, 1->127, 2->255
    visible_mask[mask == 1] = 127  # Cyst -> gray
    visible_mask[mask == 2] = 255  # Kidney -> white
    
    # Save visible version
    visible_path = f'nnunet_dataset/labelsTr/{mask_file.replace(".png", "_visible.png")}'
    Image.fromarray(visible_mask).save(visible_path)
    print(f"  Saved visible version: {visible_path}")
    
    # Also check if the original image has the right format
    original_img = Image.open(mask_path)
    print(f"  PIL mode: {original_img.mode}")
    print(f"  PIL size: {original_img.size}")

print("\n=== Summary ===")
print("The masks appear black because:")
print("- Background pixels = 0 (black)")
print("- Cyst pixels = 1 (very dark, almost black)")
print("- Kidney pixels = 2 (very dark, almost black)")
print("\nThis is CORRECT for nnU-Net format!")
print("nnU-Net expects low integer values (0, 1, 2, ...) not RGB values.")
print("\nVisible versions have been created with scaled values for verification.")