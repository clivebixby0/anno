import numpy as np
from PIL import Image
import os

# Final verification script for nnU-Net dataset

def verify_nnunet_dataset():
    """Verify that the dataset is properly formatted for nnU-Net training"""
    
    print("=== nnU-Net Dataset Verification ===")
    print()
    
    # Check directory structure
    required_dirs = ['nnunet_dataset/imagesTr', 'nnunet_dataset/labelsTr']
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            print(f"❌ Missing required directory: {dir_path}")
            return False
        else:
            print(f"✓ Found directory: {dir_path}")
    
    print()
    
    # Check file counts
    images_dir = 'nnunet_dataset/imagesTr'
    labels_dir = 'nnunet_dataset/labelsTr'
    
    image_files = [f for f in os.listdir(images_dir) if f.endswith('.png')]
    label_files = [f for f in os.listdir(labels_dir) if f.endswith('.png')]
    
    print(f"Image files: {len(image_files)}")
    print(f"Label files: {len(label_files)}")
    
    if len(image_files) != len(label_files):
        print(f"❌ Mismatch: {len(image_files)} images vs {len(label_files)} labels")
        return False
    else:
        print(f"✓ File count match: {len(image_files)} pairs")
    
    print()
    
    # Check file naming convention
    print("Checking file naming convention...")
    image_cases = set()
    label_cases = set()
    
    for img_file in image_files:
        if img_file.startswith('case') and img_file.endswith('_0000.png'):
            case_id = img_file.replace('_0000.png', '')
            image_cases.add(case_id)
        else:
            print(f"❌ Invalid image filename: {img_file}")
            return False
    
    for lbl_file in label_files:
        if lbl_file.startswith('case') and lbl_file.endswith('.png') and '_0000' not in lbl_file:
            case_id = lbl_file.replace('.png', '')
            label_cases.add(case_id)
        else:
            print(f"❌ Invalid label filename: {lbl_file}")
            return False
    
    if image_cases != label_cases:
        missing_images = label_cases - image_cases
        missing_labels = image_cases - label_cases
        if missing_images:
            print(f"❌ Missing images for: {missing_images}")
        if missing_labels:
            print(f"❌ Missing labels for: {missing_labels}")
        return False
    else:
        print(f"✓ All {len(image_cases)} cases have matching image-label pairs")
    
    print()
    
    # Check label values
    print("Checking label values...")
    invalid_labels = []
    
    for i, label_file in enumerate(sorted(label_files)[:10]):  # Check first 10 files
        label_path = os.path.join(labels_dir, label_file)
        try:
            mask = np.array(Image.open(label_path))
            unique_vals = np.unique(mask)
            
            # Check if all values are in expected range [0, 1, 2]
            if not all(val in [0, 1, 2] for val in unique_vals):
                invalid_labels.append((label_file, unique_vals))
                
        except Exception as e:
            print(f"❌ Error reading {label_file}: {e}")
            return False
    
    if invalid_labels:
        print(f"❌ Found {len(invalid_labels)} files with invalid label values:")
        for filename, values in invalid_labels:
            print(f"  {filename}: {values}")
        return False
    else:
        print("✓ Label values are correct (0, 1, 2) in sampled files")
    
    print()
    
    # Check for subdirectories (should be none)
    print("Checking for subdirectories...")
    for dir_name in ['imagesTr', 'labelsTr']:
        dir_path = f'nnunet_dataset/{dir_name}'
        subdirs = [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]
        if subdirs:
            print(f"❌ Found subdirectories in {dir_name}: {subdirs}")
            print("  nnU-Net expects files directly in the directory, not in subdirectories")
            return False
    
    print("✓ No subdirectories found - files are directly in parent directories")
    print()
    
    # Summary
    print("=== Verification Summary ===")
    print("✅ Dataset is properly formatted for nnU-Net training!")
    print()
    print("Dataset details:")
    print(f"  - {len(image_files)} image-label pairs")
    print(f"  - Images: case001_0000.png to case{len(image_files):03d}_0000.png")
    print(f"  - Labels: case001.png to case{len(label_files):03d}.png")
    print(f"  - Label classes: 0 (background), 1 (kidney), 2 (cyst)")
    print()
    print("Ready for nnU-Net training! 🚀")
    
    return True

if __name__ == "__main__":
    verify_nnunet_dataset()