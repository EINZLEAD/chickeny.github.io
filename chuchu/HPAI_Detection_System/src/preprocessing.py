import cv2
import os
import numpy as np

def preprocess_image(image_path, target_size=(224, 224)):
    """
    Standardizes images for the CNN as per the paper's 
    non-invasive visual monitoring requirements.
    """
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        return None
    
    # Resize to match CNN input layer
    img = cv2.resize(img, target_size)
    
    # Normalization (Scaling pixels 0-1)
    img = img.astype('float32') / 255.0
    
    return img

def augment_data(image):
    """
    Optional: Flips and rotates to simulate different 
    camera angles in the poultry house.
    """
    flipped = cv2.flip(image, 1)
    return flipped

if __name__ == "__main__":
    print("Preprocessing module ready.")