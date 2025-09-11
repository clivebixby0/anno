import numpy as np
from PIL import Image
import json
import os

# Load COCO annotations
with open('train/_annotations.coco.json', 'r') as f:
    coco_data = json.load(f)

# Create image ID to filename mapping
image_id_to_filename = {img['id']: img['file_name'] for img in coco_data['images']}

# Find images with only cysts, only kidneys, and both
cyst_images = set()
kidney_images = set()

for ann in coco_data['annotations']:
    if ann['category_id'] == 1:  # cyst
        cyst_images.add(ann['image_id'])
    elif ann['category_id'] == 2:  # kidney
        kidney_images.add(ann['image_id'])

only_cyst = cyst_images - kidney_images
only_kidney = kidney_images - cyst_images
both = cyst_images & kidney_images

print(f"Only cyst images: {len(only_cyst)}")
print(f"Only kidney images: {len(only_kidney)}")
print(f"Both cyst and kidney: {len(both)}")

# Check a few specific cases
test_cases = [
    (list(only_cyst)[0] if only_cyst else None, "only_cyst"),
    (list(only_kidney)[0] if only_kidney else None, "only_kidney"),
    (list(both)[0] if both else None, "both")
]

for image_id, case_type in test_cases:
    if image_id is None:
        continue
        
    # Find the corresponding case number
    filename = image_id_to_filename[image_id]
    case_num = int(filename.split('.')[0].replace('image', ''))
    
    mask_path = f"nnUNet_raw/Dataset001_KidneyCyst/labelsTr/case{case_num:03d}.png"
    
    if os.path.exists(mask_path):
        mask = np.array(Image.open(mask_path))
        unique_vals = np.unique(mask)
        non_zero_pixels = np.count_nonzero(mask)
        
        print(f"\n{case_type} - Image ID {image_id} (case{case_num:03d}.png):")
        print(f"  Unique values: {unique_vals}")
        print(f"  Non-zero pixels: {non_zero_pixels}")
        print(f"  Shape: {mask.shape}")
        
        # Count pixels for each value
        for val in unique_vals:
            count = np.sum(mask == val)
            print(f"  Value {val}: {count} pixels")
    else:
        print(f"Mask not found: {mask_path}")

# Also check the annotations for these specific cases
print("\n=== Checking annotations ===")
for image_id, case_type in test_cases:
    if image_id is None:
        continue
        
    print(f"\n{case_type} - Image ID {image_id}:")
    image_annotations = [ann for ann in coco_data['annotations'] if ann['image_id'] == image_id]
    
    for ann in image_annotations:
        category_id = ann['category_id']
        category_name = next(cat['name'] for cat in coco_data['categories'] if cat['id'] == category_id)
        print(f"  Category: {category_name} (ID: {category_id})")
        print(f"  Segmentation type: {type(ann['segmentation'])}")
        if isinstance(ann['segmentation'], list) and len(ann['segmentation']) > 0:
            print(f"  Segmentation length: {len(ann['segmentation'][0]) if ann['segmentation'][0] else 0}")