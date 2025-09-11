import json
import numpy as np
from PIL import Image
from collections import defaultdict

# Load COCO annotations
with open('train/_annotations.coco.json', 'r') as f:
    coco_data = json.load(f)

# Create mappings
image_id_to_filename = {img['id']: img['file_name'] for img in coco_data['images']}
filename_to_image_id = {img['file_name']: img['id'] for img in coco_data['images']}

# Group annotations by image
image_annotations = defaultdict(list)
for ann in coco_data['annotations']:
    image_annotations[ann['image_id']].append(ann)

# Analyze specific problematic cases
problematic_cases = {
    'cyst_only_but_shows_kidney': [20, 24, 37],  # These should only have cyst (1) but show kidney (2)
    'kidney_only_but_shows_cyst': [50, 60]      # These should only have kidney (2) but show cyst (1)
}

print("=== Analyzing Problematic Cases ===")

for case_type, case_numbers in problematic_cases.items():
    print(f"\n{case_type.upper()}:")
    
    for case_num in case_numbers:
        # Find the image ID for this case number
        case_id = f"{case_num:03d}"
        
        # Look for matching image
        matching_images = []
        for img_id, filename in image_id_to_filename.items():
            if case_id in filename or str(case_num) in filename:
                matching_images.append((img_id, filename))
        
        if matching_images:
            img_id, filename = matching_images[0]
            print(f"  Case {case_num} -> Image ID {img_id}, Filename: {filename}")
            
            # Check annotations for this image
            annotations = image_annotations[img_id]
            print(f"    Annotations: {len(annotations)}")
            
            for ann in annotations:
                cat_id = ann['category_id']
                cat_name = next(cat['name'] for cat in coco_data['categories'] if cat['id'] == cat_id)
                print(f"      - Category ID: {cat_id}, Name: {cat_name}")
            
            # Check the generated mask
            mask_path = f"nnunet_dataset/labelsTr/{case_id}.png"
            try:
                mask = np.array(Image.open(mask_path))
                unique_vals = np.unique(mask)
                print(f"    Mask unique values: {unique_vals}")
                for val in unique_vals:
                    count = np.sum(mask == val)
                    print(f"      Value {val}: {count} pixels")
            except FileNotFoundError:
                print(f"    Mask file not found: {mask_path}")
        else:
            print(f"  Case {case_num}: No matching image found")

print("\n=== Category Mapping Reference ===")
for cat in coco_data['categories']:
    print(f"Category ID {cat['id']}: {cat['name']}")

print("\nExpected nnU-Net mapping:")
print("0: background")
print("1: cyst")
print("2: kidney")