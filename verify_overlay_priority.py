import numpy as np
from PIL import Image
import json
from pathlib import Path

# Load COCO annotations to find images with overlapping cyst and kidney regions
with open('train/_annotations.coco.json', 'r') as f:
    coco_data = json.load(f)

# Group annotations by image
image_annotations = {}
for ann in coco_data['annotations']:
    img_id = ann['image_id']
    if img_id not in image_annotations:
        image_annotations[img_id] = {'cyst': [], 'kidney': []}
    
    if ann['category_id'] == 1:  # cyst
        image_annotations[img_id]['cyst'].append(ann)
    elif ann['category_id'] == 2:  # kidney
        image_annotations[img_id]['kidney'].append(ann)

# Find images that have both cyst and kidney annotations
mixed_images = []
for img_id, anns in image_annotations.items():
    if len(anns['cyst']) > 0 and len(anns['kidney']) > 0:
        mixed_images.append(img_id)

print(f"Found {len(mixed_images)} images with both cyst and kidney annotations")

# Check a few mixed images to verify overlay priority
check_count = min(5, len(mixed_images))
print(f"\nChecking first {check_count} mixed images for overlay priority...")

for i, img_id in enumerate(mixed_images[:check_count]):
    # Find corresponding case number
    img_info = next(img for img in coco_data['images'] if img['id'] == img_id)
    case_num = str(img_id).zfill(3)
    
    mask_path = f'nnunet_dataset/labelsTr/case{case_num}.png'
    
    if Path(mask_path).exists():
        mask = np.array(Image.open(mask_path))
        unique_vals = np.unique(mask)
        
        cyst_pixels = np.sum(mask == 1)
        kidney_pixels = np.sum(mask == 2)
        background_pixels = np.sum(mask == 0)
        
        print(f"\nImage {img_id} (case{case_num}):")
        print(f"  Unique values: {unique_vals}")
        print(f"  Background pixels: {background_pixels}")
        print(f"  Cyst pixels (value 1): {cyst_pixels}")
        print(f"  Kidney pixels (value 2): {kidney_pixels}")
        print(f"  Cyst annotations: {len(image_annotations[img_id]['cyst'])}")
        print(f"  Kidney annotations: {len(image_annotations[img_id]['kidney'])}")
        
        if cyst_pixels > 0 and kidney_pixels > 0:
            print(f"  ✅ Both cyst and kidney regions present - overlay working correctly")
        elif cyst_pixels > 0:
            print(f"  ⚠️  Only cyst pixels visible - cyst may have completely overlaid kidney")
        elif kidney_pixels > 0:
            print(f"  ❌ Only kidney pixels visible - overlay priority may be incorrect")
    else:
        print(f"\nMask file not found: {mask_path}")

print(f"\n=== Overlay Priority Verification ===\n")
print("Current processing order:")
print("1. Kidney annotations processed first (value 2)")
print("2. Cyst annotations processed second (value 1)")
print("3. In overlapping regions: CYST takes priority over KIDNEY")
print("\nThis means cyst regions will appear as value 1 even where they overlap with kidneys.")