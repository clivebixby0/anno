import json

def find_no_annotation_cases():
    # Load COCO data
    with open('train/_annotations.coco.json', 'r') as f:
        coco_data = json.load(f)
    
    # Get images with annotations
    images_with_annotations = set()
    for ann in coco_data['annotations']:
        images_with_annotations.add(ann['image_id'])
    
    # Find images without annotations and their case numbers
    images_without_annotations = []
    for i, img_info in enumerate(coco_data['images']):
        img_id = img_info['id']
        if img_id not in images_with_annotations:
            case_id = f"case{i+1:03d}"
            images_without_annotations.append({
                'case_id': case_id,
                'image_id': img_id,
                'filename': img_info['file_name']
            })
    
    print(f"Images without annotations (will have empty masks):")
    for item in images_without_annotations:
        print(f"  {item['case_id']}: {item['filename']} (ID: {item['image_id']})")
    
    return images_without_annotations

if __name__ == "__main__":
    find_no_annotation_cases()