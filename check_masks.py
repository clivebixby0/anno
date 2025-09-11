import numpy as np
from PIL import Image

# Check a few mask files
for case_num in [1, 10, 50]:
    mask_path = f'nnunet_dataset/labelsTr/case{case_num:03d}.png'
    try:
        mask = np.array(Image.open(mask_path))
        print(f'\nCase {case_num:03d}:')
        print(f'  Mask shape: {mask.shape}')
        print(f'  Unique values: {np.unique(mask)}')
        print(f'  Non-zero pixels: {np.count_nonzero(mask)}')
        print(f'  Value distribution:')
        for val in np.unique(mask):
            print(f'    Value {val}: {np.sum(mask == val)} pixels')
    except Exception as e:
        print(f'Error reading {mask_path}: {e}')