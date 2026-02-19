import os

def setup_directory_structure():
    base_dir = "." # Setup sa current directory
    
    # Define sub-directories based on the paper's needs
    sub_dirs = [
        'data/raw/healthy_birds',
        'data/raw/suspect_birds',
        'data/processed/train/healthy',
        'data/processed/train/suspect',
        'data/processed/val/healthy',
        'data/processed/val/suspect',
        'data/zones',
        'models/checkpoints',
        'src'
    ]
    
    for folder in sub_dirs:
        path = os.path.join(base_dir, folder)
        os.makedirs(path, exist_ok=True)
        print(f"Created: {path}")

if __name__ == "__main__":
    setup_directory_structure()