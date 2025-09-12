import os
import shutil

# Script to flatten the nnU-Net dataset structure
# nnU-Net expects files directly in imagesTr/ and labelsTr/, not in subdirectories

def flatten_directory(source_dir, target_dir):
    """Move all files from subdirectories to the parent directory"""
    if not os.path.exists(source_dir):
        print(f"Directory {source_dir} does not exist")
        return 0
    
    moved_count = 0
    
    # Process each subdirectory
    for subdir in os.listdir(source_dir):
        subdir_path = os.path.join(source_dir, subdir)
        
        if os.path.isdir(subdir_path):
            print(f"Processing {subdir} subdirectory...")
            
            # Move all files from subdirectory to parent
            for filename in os.listdir(subdir_path):
                if filename.endswith(('.png', '.jpg', '.jpeg')):
                    source_file = os.path.join(subdir_path, filename)
                    target_file = os.path.join(target_dir, filename)
                    
                    # Check for naming conflicts
                    if os.path.exists(target_file):
                        print(f"  Warning: {filename} already exists in target directory")
                        continue
                    
                    # Move the file
                    shutil.move(source_file, target_file)
                    moved_count += 1
                    
                    if moved_count % 50 == 0:
                        print(f"  Moved {moved_count} files...")
            
            # Remove empty subdirectory
            try:
                os.rmdir(subdir_path)
                print(f"  Removed empty directory: {subdir}")
            except OSError:
                print(f"  Directory {subdir} not empty, keeping it")
    
    return moved_count

print("=== Flattening nnU-Net Dataset Structure ===")
print("Moving files from subdirectories to parent directories...")
print()

# Flatten imagesTr
print("Flattening imagesTr directory:")
images_moved = flatten_directory("nnunet_dataset/imagesTr", "nnunet_dataset/imagesTr")
print(f"Moved {images_moved} image files")
print()

# Flatten labelsTr
print("Flattening labelsTr directory:")
labels_moved = flatten_directory("nnunet_dataset/labelsTr", "nnunet_dataset/labelsTr")
print(f"Moved {labels_moved} label files")
print()

# Also flatten colored and visible directories if they exist
for dir_name in ["labelsTr_colored", "labelsTr_visible"]:
    dir_path = f"nnunet_dataset/{dir_name}"
    if os.path.exists(dir_path):
        print(f"Flattening {dir_name} directory:")
        moved = flatten_directory(dir_path, dir_path)
        print(f"Moved {moved} files")
        print()

print("=== Verification ===")
# Count files in each directory
for dir_name in ["imagesTr", "labelsTr", "labelsTr_colored", "labelsTr_visible"]:
    dir_path = f"nnunet_dataset/{dir_name}"
    if os.path.exists(dir_path):
        # Count files directly in the directory (not in subdirectories)
        files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and f.endswith(('.png', '.jpg', '.jpeg'))]
        subdirs = [d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]
        
        print(f"{dir_name}: {len(files)} files, {len(subdirs)} subdirectories")

print("\n✓ Dataset structure flattened for nnU-Net compatibility")
print("Files are now directly in imagesTr/ and labelsTr/ as expected by nnU-Net")