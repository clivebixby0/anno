import cv2
import os
from pathlib import Path

# Set the root directory to the nnunet_dataset folder
root = Path("/Users/carlmacabales/Downloads/Kidney Cyst Coco Segmentation/nnunet_dataset")

# Process imagesTr directory with both Axial and Coronal subdirectories
for sub in ["Axial", "Coronal"]:
    images_path = root / "imagesTr" / sub
    if not images_path.exists():
        print(f"Directory {images_path} does not exist, skipping...")
        continue
        
    print(f"Processing {sub} images...")
    
    for f in images_path.glob("*.png"):
        img = cv2.imread(str(f), cv2.IMREAD_UNCHANGED)
        if img is None:
            print(f"Could not read image: {f}")
            continue
            
        if img.ndim == 3:  # RGB or RGBA
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(str(f), gray)
            print(f"Converted: {f}")
        else:
            print(f"Already greyscale: {f}")
            
print("Conversion complete!")