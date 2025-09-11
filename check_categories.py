import numpy as np
from PIL import Image
import json

# Load COCO data to find images with different categories
with open('train/_annotations.coco.json', 'r') as f:
    data = json.load(f)

# Find images with cyst (category_id=1) and kidney (category_id=2) annotations
cyst_images = set()
kidney_images = set()

for ann in data['annotations']:
    if ann['category_id'] == 1:  # cyst
        cyst_images.add(ann['image_id'])
    elif ann['category_id'] == 2:  # kidney
        kidney_images.add(ann['image_id'])

print(f"Images with cyst annotations: {len(cyst_images)}")
print(f"Images with kidney annotations: {len(kidney_images)}")

# Check a few masks from each category
print("\nChecking cyst masks:")
for i, img_id in enumerate(list(cyst_images)[:3]):
    mask_path = f'nnunet_dataset/labelsTr/case{img_id+1:03d}.png'
    try:
        mask = np.array(Image.open(mask_path))
        unique_vals = np.unique(mask)
        print(f"  Image {img_id+1}: unique values = {unique_vals}, non-zero = {np.count_nonzero(mask)}")
    except Exception as e:
        print(f"  Error reading {mask_path}: {e}")

print("\nChecking kidney masks:")
for i, img_id in enumerate(list(kidney_images)[:3]):
    mask_path = f'nnunet_dataset/labelsTr/case{img_id+1:03d}.png'
    try:
        mask = np.array(Image.open(mask_path))
        unique_vals = np.unique(mask)
        print(f"  Image {img_id+1}: unique values = {unique_vals}, non-zero = {np.count_nonzero(mask)}")
    except Exception as e:
        print(f"  Error reading {mask_path}: {e}")

# Check if any masks have value 1 (which should be kidney in our mapping)
print("\nLooking for masks with value 1 (kidney):")
found_kidney = False
for case_num in range(1, 21):  # Check first 20 cases
    mask_path = f'nnunet_dataset/labelsTr/case{case_num:03d}.png'
    try:
        mask = np.array(Image.open(mask_path))
        if 1 in mask:
            print(f"  Case {case_num:03d}: has value 1 (kidney), unique values = {np.unique(mask)}")
            found_kidney = True
            break
    except:
        continue

if not found_kidney:
    print("  No masks found with value 1 in first 20 cases")