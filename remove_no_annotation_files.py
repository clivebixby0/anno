import os
import glob

def remove_no_annotation_files():
    # Files to remove (cases without annotations)
    cases_to_remove = ['case012_0000.png', 'case163_0000.png', 'case225_0000.png', 'case245_0000.png', 'case309_0000.png']
    
    # Directories to clean
    directories = [
        'nnunet_dataset/imagesTr',
        'nnunet_dataset/imagesTr/Axial',
        'nnunet_dataset/imagesTr/Coronal',
        'nnunet_dataset/labelsTr',
        'nnunet_dataset/labelsTr/Axial',
        'nnunet_dataset/labelsTr/Coronal',
        'nnunet_dataset/labelsTr_colored',
        'nnunet_dataset/labelsTr_colored/Axial',
        'nnunet_dataset/labelsTr_colored/Coronal',
        'nnunet_dataset/labelsTr_visible',
        'nnunet_dataset/labelsTr_visible/Axial',
        'nnunet_dataset/labelsTr_visible/Coronal'
    ]
    
    removed_files = []
    
    for directory in directories:
        if os.path.exists(directory):
            for case_file in cases_to_remove:
                file_path = os.path.join(directory, case_file)
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                        removed_files.append(file_path)
                        print(f"Removed: {file_path}")
                    except Exception as e:
                        print(f"Error removing {file_path}: {e}")
                else:
                    print(f"File not found: {file_path}")
        else:
            print(f"Directory not found: {directory}")
    
    print(f"\nTotal files removed: {len(removed_files)}")
    return removed_files

if __name__ == "__main__":
    remove_no_annotation_files()