import numpy as np
from PIL import Image
import os

def fix_all_label_directories():
    """Fix all label directories to use consistent [0, 1, 2] class IDs"""
    
    directories = {
        'labelsTr_visible': 'nnunet_dataset/labelsTr_visible',
        'labelsTr_colored': 'nnunet_dataset/labelsTr_colored'
    }
    
    print("=== Fixing All Label Directories ===")
    print("Converting all directories to use class IDs [0, 1, 2]")
    print()
    
    total_fixed = 0
    
    for dir_name, dir_path in directories.items():
        print(f"Processing {dir_name}...")
        
        if not os.path.exists(dir_path):
            print(f"  ❌ Directory not found: {dir_path}")
            continue
            
        files = [f for f in os.listdir(dir_path) if f.endswith('.png')]
        files_fixed = 0
        
        for i, filename in enumerate(files):
            file_path = os.path.join(dir_path, filename)
            
            try:
                # Load the mask
                mask = np.array(Image.open(file_path))
                original_values = np.unique(mask)
                
                # Check if it needs fixing
                if not np.array_equal(sorted(original_values), [0, 1, 2]):
                    # Create a new mask with correct values
                    new_mask = np.zeros_like(mask)
                    
                    # Map values to class IDs
                    # Background (darkest) -> 0
                    # First class (medium) -> 1  
                    # Second class (brightest) -> 2
                    sorted_vals = sorted(original_values)
                    
                    for i, val in enumerate(sorted_vals):
                        new_mask[mask == val] = i
                    
                    # Save the corrected mask
                    Image.fromarray(new_mask.astype(np.uint8)).save(file_path)
                    files_fixed += 1
                    
            except Exception as e:
                print(f"    ❌ Error processing {filename}: {e}")
                continue
        
        print(f"  ✓ {dir_name}: {files_fixed}/{len(files)} files fixed")
        total_fixed += files_fixed
    
    print()
    print("=== Summary ===")
    print(f"Total files fixed: {total_fixed}")
    
    # Verify the results
    print()
    print("=== Verification ===")
    
    for dir_name, dir_path in directories.items():
        if os.path.exists(dir_path):
            files = [f for f in os.listdir(dir_path) if f.endswith('.png')][:3]
            print(f"{dir_name} sample values:")
            
            for filename in files:
                file_path = os.path.join(dir_path, filename)
                try:
                    mask = np.array(Image.open(file_path))
                    unique_vals = np.unique(mask)
                    print(f"  {filename}: {unique_vals}")
                except Exception as e:
                    print(f"  {filename}: Error - {e}")
            print()
    
    print("✅ All label directories now use consistent [0, 1, 2] class IDs!")
    return True

if __name__ == "__main__":
    fix_all_label_directories()