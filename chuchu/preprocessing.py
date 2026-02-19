import cv2
import os
import glob

def preprocess_image(image_path, target_size=(224, 224)):
    """Standardizes images for the CNN."""
    img = cv2.imread(image_path)
    if img is None:
        return None
    # Resize to match CNN input layer
    img = cv2.resize(img, target_size)
    return img

def prepare_dataset():
    """Kinukuha ang raw data at inililipat sa processed folder para sa training."""
    raw_dirs = {
        'data/raw/healthy_birds': 'data/processed/train/healthy',
        'data/raw/suspect_birds': 'data/processed/train/suspect'
    }
    
    for raw_dir, processed_dir in raw_dirs.items():
        if not os.path.exists(raw_dir):
            print(f"Wala pang folder na {raw_dir}. Siguraduhing na-run ang main.py")
            continue
            
        os.makedirs(processed_dir, exist_ok=True)
        images = glob.glob(os.path.join(raw_dir, '*.*')) # Kunin lahat ng pictures
        
        if len(images) == 0:
            print(f"Walang laman ang {raw_dir}. Maglagay muna ng pictures dito.")
            continue
            
        print(f"Pinoprocess ang {len(images)} files mula sa {raw_dir}...")
        for img_path in images:
            img = preprocess_image(img_path)
            if img is not None:
                filename = os.path.basename(img_path)
                save_path = os.path.join(processed_dir, filename)
                cv2.imwrite(save_path, img) # I-save sa processed folder
                
    print("\nTapos na ang preprocessing! Handa na ang data para sa training.")

if __name__ == "__main__":
    prepare_dataset()