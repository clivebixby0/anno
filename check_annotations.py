#!/usr/bin/env python3
"""
Check which images have annotations and which don't.
"""

import json
from pathlib import Path

def main():
    """Check annotation coverage."""
    print("Checking annotation coverage...\n")
    
    # Load COCO data
    with open("train/_annotations.coco.json", "r") as f:
        coco_data = json.load(f)
    
    # Get all images
    all_images = {img['id']: img['file_name'] for img in coco_data['images']}
    print(f"Total images in COCO data: {len(all_images)}")
    
    # Get images with annotations
    images_with_annotations = set()
    for ann in coco_data['annotations']:
        images_with_annotations.add(ann['image_id'])
    
    print(f"Images with annotations: {len(images_with_annotations)}")
    
    # Find images without annotations
    images_without_annotations = set(all_images.keys()) - images_with_annotations
    print(f"Images without annotations: {len(images_without_annotations)}")
    
    if images_without_annotations:
        print("\nImages without annotations:")
        for img_id in sorted(images_without_annotations):
            filename = all_images[img_id]
            print(f"  ID {img_id}: {filename}")
    
    # Check if files exist in train folder
    train_dir = Path("train")
    missing_files = []
    for img_id, filename in all_images.items():
        if not (train_dir / filename).exists():
            missing_files.append((img_id, filename))
    
    if missing_files:
        print(f"\nMissing files in train folder ({len(missing_files)}):")
        for img_id, filename in missing_files:
            print(f"  ID {img_id}: {filename}")
    else:
        print("\nAll files exist in train folder.")

if __name__ == "__main__":
    main()