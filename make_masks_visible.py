import numpy as np
from PIL import Image
import os

# Create visible versions of all masks
labels_dir = 'nnunet_dataset/labelsTr'
visible_dir = 'nnunet_dataset/labelsTr_visible'

# Create visible directory
os.makedirs(visible_dir, exist_ok=True)

print("Converting all masks to visible format...")

# Process all mask files
mask_files = [f for f in os.listdir(labels_dir) if f.endswith('.png') and not f.endswith('_visible.png')]

for i, mask_file in enumerate(mask_files, 1):
    # Load original mask
    mask_path = os.path.join(labels_dir, mask_file)
    mask = np.array(Image.open(mask_path))
    
    # Create visible version with scaled values
    visible_mask = np.zeros_like(mask, dtype=np.uint8)
    
    # Scale values for visibility:
    # Background (0) -> 0 (black)
    # Cyst (1) -> 128 (gray) 
    # Kidney (2) -> 255 (white)
    visible_mask[mask == 0] = 0    # Background stays black
    visible_mask[mask == 1] = 128  # Cyst -> gray
    visible_mask[mask == 2] = 255  # Kidney -> white
    
    # Save visible version
    visible_path = os.path.join(visible_dir, mask_file)
    Image.fromarray(visible_mask).save(visible_path)
    
    if i % 50 == 0 or i == len(mask_files):
        print(f"Processed {i}/{len(mask_files)} masks")

print(f"\nDone! Visible masks saved to: {visible_dir}")
print("\nIn the visible versions:")
print("- Black = Background (original value 0)")
print("- Gray = Cyst (original value 1)")
print("- White = Kidney (original value 2)")
print("\nThe original masks in labelsTr are CORRECT for nnU-Net training!")
print("They appear black because nnU-Net uses integer values 0,1,2 not RGB colors.")
