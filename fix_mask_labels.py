import numpy as np
from PIL import Image
import os

# Script to fix mask labels that may have grayscale values instead of class IDs

def check_and_fix_mask(mask_path):
    """Check a mask file and fix any grayscale values to proper class IDs"""
    try:
        # Load the mask
        mask = np.array(Image.open(mask_path))
        
        # Get unique values
        unique_vals = np.unique(mask)
        print(f"Checking {os.path.basename(mask_path)}: unique values = {unique_vals}")
        
        # Check if we have unexpected values
        expected_values = {0, 1, 2}
        unexpected_values = set(unique_vals) - expected_values
        
        if unexpected_values:
            print(f"  Found unexpected values: {unexpected_values}")
            
            # Create a fixed mask
            fixed_mask = np.zeros_like(mask, dtype=np.uint8)
            
            # Map values to proper class IDs
            # Background (0 or very low values) -> 0
            # Medium values (around 128) -> 1 (kidney)
            # High values (around 255) -> 2 (cyst)
            
            fixed_mask[mask == 0] = 0  # Background stays 0
            
            # Handle grayscale values
            if 128 in mask or any(120 <= val <= 135 for val in unique_vals):
                # Map grayscale 128 (or similar) to kidney (1)
                for val in unique_vals:
                    if 120 <= val <= 135:
                        fixed_mask[mask == val] = 1
                        print(f"    Mapped {val} -> 1 (kidney)")
            
            if 255 in mask or any(250 <= val <= 255 for val in unique_vals):
                # Map grayscale 255 (or similar) to cyst (2)
                for val in unique_vals:
                    if 250 <= val <= 255:
                        fixed_mask[mask == val] = 2
                        print(f"    Mapped {val} -> 2 (cyst)")
            
            # Handle any other unexpected values
            for val in unexpected_values:
                if val not in [128, 255] and not (120 <= val <= 135) and not (250 <= val <= 255):
                    if val < 64:
                        fixed_mask[mask == val] = 0  # Low values -> background
                        print(f"    Mapped {val} -> 0 (background)")
                    elif val < 192:
                        fixed_mask[mask == val] = 1  # Medium values -> kidney
                        print(f"    Mapped {val} -> 1 (kidney)")
                    else:
                        fixed_mask[mask == val] = 2  # High values -> cyst
                        print(f"    Mapped {val} -> 2 (cyst)")
            
            # Save the fixed mask
            Image.fromarray(fixed_mask).save(mask_path)
            print(f"  Fixed and saved: {mask_path}")
            
            # Verify the fix
            verify_mask = np.array(Image.open(mask_path))
            verify_unique = np.unique(verify_mask)
            print(f"  After fix: unique values = {verify_unique}")
            
            return True
        else:
            print(f"  ✓ Mask is correct (values: {unique_vals})")
            return False
            
    except Exception as e:
        print(f"Error processing {mask_path}: {e}")
        return False

# Check and fix all masks in both Axial and Coronal directories
labels_dir = "nnunet_dataset/labelsTr"
fixed_count = 0
total_count = 0

print("=== Checking and Fixing Mask Labels ===")
print("Expected values: 0 (background), 1 (kidney), 2 (cyst)")
print()

for subdir in ["Axial", "Coronal"]:
    subdir_path = os.path.join(labels_dir, subdir)
    if os.path.exists(subdir_path):
        print(f"Processing {subdir} directory...")
        
        mask_files = [f for f in os.listdir(subdir_path) if f.endswith('.png')]
        
        for mask_file in sorted(mask_files):
            mask_path = os.path.join(subdir_path, mask_file)
            total_count += 1
            
            if check_and_fix_mask(mask_path):
                fixed_count += 1
        
        print()

print(f"=== Summary ===")
print(f"Total masks checked: {total_count}")
print(f"Masks fixed: {fixed_count}")
print(f"Masks already correct: {total_count - fixed_count}")

if fixed_count > 0:
    print("\n✓ All masks now contain only values 0, 1, 2 as required by nnU-Net")
else:
    print("\n✓ All masks were already in correct format")