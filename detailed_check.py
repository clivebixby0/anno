import json
import numpy as np
from PIL import Image
from collections import defaultdict

# Load COCO annotations
with open('train/_annotations.coco.json', 'r') as f:
    coco_data = json.load(f)

# Create mappings
image_id_to_filename = {img['id']: img['file_name'] for img in coco_data['images']}

# Group annotations by image
image_annotations = defaultdict(list)
for ann in coco_data['annotations']:
    image_annotations[ann['image_id']].append(ann)

# Analyze images by their actual annotations
cyst_only_images = []
kidney_only_images = []
both_images = []

for img_id, annotations in image_annotations.items():
    has_cyst = any(ann['category_id'] == 1 for ann in annotations)
    has_kidney = any(ann['category_id'] == 2 for ann in annotations)
    
    if has_cyst and has_kidney:
        both_images.append(img_id)
    elif has_cyst:
        cyst_only_images.append(img_id)
    elif has_kidney:
        kidney_only_images.append(img_id)

print(f"Images with only cyst: {len(cyst_only_images)}")
print(f"Images with only kidney: {len(kidney_only_images)}")
print(f"Images with both cyst and kidney: {len(both_images)}")

# Check some sample masks to verify correct labeling
def check_mask_values(img_ids, category_name, max_samples=3):
    print(f"\n=== Checking {category_name} Images ===")
    
    for i, img_id in enumerate(img_ids[:max_samples]):
        # Find corresponding case number
        filename = image_id_to_filename[img_id]
        
        # Extract case number from filename (this is tricky with the current naming)
        # Let's use a different approach - find the mask file
        case_found = False
        for case_num in range(1, 400):  # Check reasonable range
            case_id = f"{case_num:03d}"
            mask_path = f"nnunet_dataset/labelsTr/{case_id}.png"
            
            try:
                mask = np.array(Image.open(mask_path))
                # Check if this mask corresponds to our image by checking annotations
                unique_vals = np.unique(mask)
                
                # Get expected categories for this image
                annotations = image_annotations[img_id]
                expected_categories = set(ann['category_id'] for ann in annotations)
                
                print(f"  Image {img_id} (filename: {filename[:30]}...)")
                print(f"    Expected categories: {expected_categories}")
                print(f"    Case {case_num} mask unique values: {unique_vals}")
                
                for val in unique_vals:
                    if val > 0:  # Skip background
                        count = np.sum(mask == val)
                        print(f"      Value {val} pixels: {count}")
                
                case_found = True
                break
                
            except FileNotFoundError:
                continue
        
        if not case_found:
            print(f"  Image {img_id}: No corresponding mask found")

# Check samples from each category
if cyst_only_images:
    check_mask_values(cyst_only_images, "Only Cyst")
if kidney_only_images:
    check_mask_values(kidney_only_images, "Only Kidney")
if both_images:
    check_mask_values(both_images, "Both Categories")

print("\n=== nnU-Net Label Mapping ===")
print("0: background")
print("1: cyst")
print("2: kidney")