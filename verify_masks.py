import numpy as np
from PIL import Image
import os

# Check the first few mask files to verify correct labeling
mask_dir = "nnunet_dataset/labelsTr"

print("=== Verifying nnU-Net Mask Labels ===")
print("Expected mapping: 0=background, 1=cyst, 2=kidney")
print()

# Get list of mask files
mask_files = sorted([f for f in os.listdir(mask_dir) if f.endswith('.png')])

print(f"Total mask files: {len(mask_files)}")
print("\nChecking first 10 masks:")

for i, mask_file in enumerate(mask_files[:10]):
    mask_path = os.path.join(mask_dir, mask_file)
    mask = np.array(Image.open(mask_path))
    
    unique_vals = np.unique(mask)
    print(f"\n{mask_file}:")
    print(f"  Unique values: {unique_vals}")
    
    for val in unique_vals:
        count = np.sum(mask == val)
        if val == 0:
            print(f"    Background (0): {count} pixels")
        elif val == 1:
            print(f"    Cyst (1): {count} pixels")
        elif val == 2:
            print(f"    Kidney (2): {count} pixels")
        else:
            print(f"    Unknown value ({val}): {count} pixels")

# Check for any unexpected values across all masks
print("\n=== Checking all masks for unexpected values ===")
all_values = set()
for mask_file in mask_files:
    mask_path = os.path.join(mask_dir, mask_file)
    mask = np.array(Image.open(mask_path))
    all_values.update(np.unique(mask))

print(f"All unique values across dataset: {sorted(all_values)}")

if all_values <= {0, 1, 2}:
    print("✓ All masks contain only expected values (0, 1, 2)")
else:
    unexpected = all_values - {0, 1, 2}
    print(f"✗ Found unexpected values: {unexpected}")

# Count distribution of label combinations
print("\n=== Label Combination Statistics ===")
combinations = {}
for mask_file in mask_files:
    mask_path = os.path.join(mask_dir, mask_file)
    mask = np.array(Image.open(mask_path))
    unique_vals = tuple(sorted(np.unique(mask)))
    combinations[unique_vals] = combinations.get(unique_vals, 0) + 1

for combo, count in sorted(combinations.items()):
    labels = []
    for val in combo:
        if val == 0:
            labels.append("background")
        elif val == 1:
            labels.append("cyst")
        elif val == 2:
            labels.append("kidney")
        else:
            labels.append(f"unknown({val})")
    
    print(f"  {combo} ({', '.join(labels)}): {count} images")