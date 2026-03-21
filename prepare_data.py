import os
import random
import shutil
from PIL import Image

BASE_DIR = "."

# ----------------------------
# STEP 1 — Rename folders
# ----------------------------
rename_map = {
    "Anthracnose": "anthracnose",
    "Cholorosis": "chlorosis",
    "Dried Leaf": "dried_leaf",
    "Healthy": "healthy",
    "Initial stage": "initial_stage",
    "Leaf Blight": "leaf_blight",
    "Leaf Spot": "leaf_spot",
    "Pest Damage": "pest_damage",
    "Rustdiseases": "rust_diseases"
}

def rename_folders(base_path):
    for old_name, new_name in rename_map.items():
        old_path = os.path.join(base_path, old_name)
        new_path = os.path.join(base_path, new_name)

        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            print(f"Renamed: {old_name} → {new_name}")

# ----------------------------
# STEP 2 — Clean + Resize
# ----------------------------
def clean_and_resize(folder, size=(224,224)):
    for class_name in os.listdir(folder):

        # skip unwanted folders
        if class_name.startswith(".") or class_name == "final_dataset":
            continue

        class_path = os.path.join(folder, class_name)

        if not os.path.isdir(class_path):
            continue

        for img_name in os.listdir(class_path):

            # only images
            if not img_name.lower().endswith((".png", ".jpg", ".jpeg")):
                continue

            img_path = os.path.join(class_path, img_name)

            try:
                img = Image.open(img_path).convert("RGB")
                img = img.resize(size)
                img.save(img_path)
            except:
                print(f"Removed corrupt: {img_path}")
                try:
                    os.remove(img_path)
                except:
                    print(f"Could not remove: {img_path}")

# ----------------------------
# STEP 3 — Split dataset
# ----------------------------
def split_dataset(source_dir, dest_dir, train=0.7, val=0.15, test=0.15):

    for class_name in os.listdir(source_dir):

        # skip unwanted folders
        if class_name.startswith(".") or class_name == "final_dataset":
            continue

        class_path = os.path.join(source_dir, class_name)

        if not os.path.isdir(class_path):
            continue

        # only image files
        files = [
            f for f in os.listdir(class_path)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]

        random.shuffle(files)

        n = len(files)
        train_end = int(train * n)
        val_end = train_end + int(val * n)

        splits = {
            "train": files[:train_end],
            "val": files[train_end:val_end],
            "test": files[val_end:]
        }

        for split_name, split_files in splits.items():
            split_path = os.path.join(dest_dir, split_name, class_name)
            os.makedirs(split_path, exist_ok=True)

            for file in split_files:
                src = os.path.join(class_path, file)
                dst = os.path.join(split_path, file)
                shutil.copy(src, dst)

    print("Dataset split completed!")

# ----------------------------
# RUN PIPELINE
# ----------------------------
rename_folders(BASE_DIR)
clean_and_resize(BASE_DIR)
split_dataset(BASE_DIR, "final_dataset")