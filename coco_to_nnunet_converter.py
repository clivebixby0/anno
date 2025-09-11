#!/usr/bin/env python3
"""
COCO to nnU-Net v2 Converter
Converts COCO segmentation format to nnU-Net v2 format for 2D medical image segmentation
"""

import json
import os
import shutil
from pathlib import Path
try:
    import numpy as np
except ImportError:
    print("Installing numpy...")
    os.system("pip3 install numpy")
    import numpy as np

try:
    from PIL import Image
except ImportError:
    print("Installing Pillow...")
    os.system("pip3 install Pillow")
    from PIL import Image

def load_coco_data(json_path):
    """Load and parse COCO JSON file"""
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data

def examine_coco_structure(data):
    """Examine the structure of COCO data"""
    print("=== COCO Dataset Structure ===")
    print(f"Categories: {len(data.get('categories', []))}")
    for cat in data.get('categories', []):
        print(f"  - ID: {cat['id']}, Name: {cat['name']}")
    
    print(f"\nImages: {len(data.get('images', []))}")
    print(f"Annotations: {len(data.get('annotations', []))}")
    
    # Check if annotations exist
    if 'annotations' in data and len(data['annotations']) > 0:
        sample_ann = data['annotations'][0]
        print(f"\nSample annotation keys: {list(sample_ann.keys())}")
        if 'segmentation' in sample_ann:
            print(f"Segmentation type: {type(sample_ann['segmentation'])}")
    else:
        print("\nNo annotations found in the dataset!")
    
    return data

def decode_rle_mask(segmentation, height, width):
    """
    Decode polygon segmentation to binary mask without external dependencies
    """
    mask = np.zeros((height, width), dtype=np.uint8)
    
    if isinstance(segmentation, list):
        # Handle polygon segmentation
        for polygon in segmentation:
            if len(polygon) >= 6:  # At least 3 points (x,y pairs)
                # Convert to PIL polygon format
                from PIL import Image, ImageDraw
                img = Image.new('L', (width, height), 0)
                draw = ImageDraw.Draw(img)
                
                # Convert flat list to list of tuples
                points = [(polygon[i], polygon[i+1]) for i in range(0, len(polygon), 2)]
                draw.polygon(points, fill=1)
                
                # Convert PIL image to numpy array and add to mask
                polygon_mask = np.array(img)
                mask = np.maximum(mask, polygon_mask)
    
    elif isinstance(segmentation, dict):
        # Handle RLE format (not expected in this dataset but kept for compatibility)
        if 'counts' in segmentation:
            counts = segmentation['counts']
            if isinstance(counts, str):
                print("Warning: Compressed RLE format detected. This simple decoder may not work correctly.")
                return mask
            else:
                # Uncompressed RLE
                pixel_position = 0
                for i, count in enumerate(counts):
                    if i % 2 == 1:  # Odd indices are foreground
                        end_position = pixel_position + count
                        while pixel_position < end_position and pixel_position < height * width:
                            row = pixel_position // width
                            col = pixel_position % width
                            if row < height and col < width:
                                mask[row, col] = 1
                            pixel_position += 1
                    else:
                        pixel_position += count
    
    return mask

def create_nnunet_structure(output_dir):
    """Create nnU-Net v2 directory structure"""
    output_path = Path(output_dir)
    
    # Create main directories
    images_dir = output_path / "imagesTr"
    labels_dir = output_path / "labelsTr"
    
    images_dir.mkdir(parents=True, exist_ok=True)
    labels_dir.mkdir(parents=True, exist_ok=True)
    
    return images_dir, labels_dir

def convert_coco_to_nnunet(coco_json_path, images_dir_path, output_dir):
    """Convert COCO dataset to nnU-Net v2 format"""
    
    # Load COCO data
    print("Loading COCO data...")
    coco_data = load_coco_data(coco_json_path)
    
    # Examine structure
    examine_coco_structure(coco_data)
    
    # Create output structure
    print("\nCreating nnU-Net v2 directory structure...")
    images_out_dir, labels_out_dir = create_nnunet_structure(output_dir)
    
    # Create mappings
    image_id_to_info = {img['id']: img for img in coco_data['images']}
    category_id_to_name = {cat['id']: cat['name'] for cat in coco_data['categories']}
    
    print(f"\nCategory mapping: {category_id_to_name}")
    
    # Process images and annotations
    processed_images = set()
    
    if 'annotations' not in coco_data or len(coco_data['annotations']) == 0:
        print("\nNo annotations found! Converting images only...")
        # Convert images without annotations
        for i, img_info in enumerate(coco_data['images']):
            case_id = f"case{i+1:03d}"
            
            # Copy and rename image
            src_img_path = Path(images_dir_path) / img_info['file_name']
            dst_img_path = images_out_dir / f"{case_id}_0000.png"
            
            if src_img_path.exists():
                # Convert to PNG if needed
                img = Image.open(src_img_path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.save(dst_img_path, 'PNG')
                
                # Create empty mask
                mask = np.zeros((img_info['height'], img_info['width']), dtype=np.uint8)
                mask_img = Image.fromarray(mask)
                mask_img.save(labels_out_dir / f"{case_id}.png", 'PNG')
                
                processed_images.add(img_info['id'])
    else:
        # Group annotations by image
        annotations_by_image = {}
        for ann in coco_data['annotations']:
            img_id = ann['image_id']
            if img_id not in annotations_by_image:
                annotations_by_image[img_id] = []
            annotations_by_image[img_id].append(ann)
        
        print(f"\nProcessing {len(annotations_by_image)} images with annotations...")
        
        for i, (img_id, annotations) in enumerate(annotations_by_image.items()):
            if img_id not in image_id_to_info:
                continue
                
            img_info = image_id_to_info[img_id]
            case_id = f"case{i+1:03d}"
            
            # Copy and rename image
            src_img_path = Path(images_dir_path) / img_info['file_name']
            dst_img_path = images_out_dir / f"{case_id}_0000.png"
            
            if not src_img_path.exists():
                print(f"Warning: Image {src_img_path} not found")
                continue
            
            # Convert image to PNG
            img = Image.open(src_img_path)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(dst_img_path, 'PNG')
            
            # Create segmentation mask
            height, width = img_info['height'], img_info['width']
            combined_mask = np.zeros((height, width), dtype=np.uint8)
            
            # Group annotations by category
            kidney_annotations = [ann for ann in annotations if ann.get('category_id') == 2]
            cyst_annotations = [ann for ann in annotations if ann.get('category_id') == 1]
            
            # First process kidney annotations (value 2)
            for ann in kidney_annotations:
                if 'segmentation' in ann:
                    mask = decode_rle_mask(ann['segmentation'], height, width)
                    combined_mask[mask > 0] = 2  # kidney = 2
            
            # Then process cyst annotations (value 1, overwrites kidney where they overlap)
            for ann in cyst_annotations:
                if 'segmentation' in ann:
                    mask = decode_rle_mask(ann['segmentation'], height, width)
                    combined_mask[mask > 0] = 1  # cyst = 1
            
            # Save mask as PNG
            mask_img = Image.fromarray(combined_mask)
            mask_img.save(labels_out_dir / f"{case_id}.png", 'PNG')
            
            processed_images.add(img_id)
    
    # Create dataset.json for nnU-Net v2
    # Updated mapping: 0=background, 1=cyst, 2=kidney
    dataset_json = {
        "channel_names": {
            "0": "image"
        },
        "labels": {
            "background": 0,
            "cyst": 1,
            "kidney": 2
        },
        "numTraining": len(processed_images),
        "file_ending": ".png",
        "dataset_name": "KidneyCyst",
        "reference": "Converted from COCO format",
        "description": "Kidney cyst segmentation dataset"
    }
    
    # Save dataset.json
    with open(Path(output_dir) / "dataset.json", 'w') as f:
        json.dump(dataset_json, f, indent=2)
    
    print(f"\n=== Conversion Complete ===")
    print(f"Processed images: {len(processed_images)}")
    print(f"Output directory: {output_dir}")
    print(f"Images directory: {images_out_dir}")
    print(f"Labels directory: {labels_out_dir}")
    print(f"Dataset JSON: {Path(output_dir) / 'dataset.json'}")
    
    return len(processed_images)

if __name__ == "__main__":
    # Configuration
    coco_json_path = "/Users/carlmacabales/Downloads/Kidney Cyst Coco Segmentation/train/_annotations.coco.json"
    images_dir_path = "/Users/carlmacabales/Downloads/Kidney Cyst Coco Segmentation/train"
    output_dir = "/Users/carlmacabales/Downloads/Kidney Cyst Coco Segmentation/nnunet_dataset"
    
    # Run conversion
    try:
        num_processed = convert_coco_to_nnunet(coco_json_path, images_dir_path, output_dir)
        print(f"\nSuccessfully converted {num_processed} images to nnU-Net v2 format!")
    except Exception as e:
        print(f"Error during conversion: {e}")
        import traceback
        traceback.print_exc()