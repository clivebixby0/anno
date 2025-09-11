import numpy as np
from PIL import Image
import os

# Create colored versions of all masks
labels_dir = 'nnunet_dataset/labelsTr'
colored_dir = 'nnunet_dataset/labelsTr_colored'

# Create colored directory
os.makedirs(colored_dir, exist_ok=True)

print("Converting all masks to colored format...")
print("Color mapping:")
print("- Background: Black (0, 0, 0)")
print("- Kidney: Red (255, 0, 0)")
print("- Cyst: Cyan (0, 200, 255)")

# Process all mask files
mask_files = [f for f in os.listdir(labels_dir) if f.endswith('.png') and not f.endswith('_visible.png')]

for i, mask_file in enumerate(mask_files, 1):
    # Load original mask
    mask_path = os.path.join(labels_dir, mask_file)
    mask = np.array(Image.open(mask_path))
    
    # Create RGB colored version
    height, width = mask.shape
    colored_mask = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Apply color mapping:
    # Background (0) -> Black (0, 0, 0) - already zeros
    # Kidney (1) -> Red (255, 0, 0)
    # Cyst (2) -> Cyan (0, 200, 255)
    
    colored_mask[mask == 1] = [255, 0, 0]    # Kidney -> Red
    colored_mask[mask == 2] = [0, 200, 255]  # Cyst -> Cyan
    
    # Save colored version
    colored_path = os.path.join(colored_dir, mask_file)
    Image.fromarray(colored_mask).save(colored_path)
    
    if i % 50 == 0 or i == len(mask_files):
        print(f"Processed {i}/{len(mask_files)} masks")

print(f"\nDone! Colored masks saved to: {colored_dir}")
print("\nIn the colored versions:")
print("- Black = Background (original value 0)")
print("- Red = Kidney (original value 1)")
print("- Cyan = Cyst (original value 2)")
print("\nNote: Cyst annotations overlay on top of kidney annotations in overlapping regions.")
print("The original masks in labelsTr are still CORRECT for nnU-Net training!")