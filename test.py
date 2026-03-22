import os

folder = "final_dataset/train/leaf_spot"  # change if needed

aug_files = [f for f in os.listdir(folder) if f.startswith("aug_")]

print(f"Augmented images: {len(aug_files)}")
print("Sample files:", aug_files[:5])