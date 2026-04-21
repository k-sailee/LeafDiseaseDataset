import os
import shutil
from sklearn.model_selection import train_test_split

MERGED_DIR = "merged_data"
FINAL_DIR = "final_dataset"

SPLIT_RATIO = (0.7, 0.15, 0.15)


def split_and_copy(class_name):
    class_path = os.path.join(MERGED_DIR, class_name)
    images = os.listdir(class_path)

    train, temp = train_test_split(images, test_size=0.3, random_state=42)
    val, test = train_test_split(temp, test_size=0.5, random_state=42)

    splits = {
        "train": train,
        "val": val,
        "test": test
    }

    for split in splits:
        target_dir = os.path.join(FINAL_DIR, split, class_name)
        os.makedirs(target_dir, exist_ok=True)

        for img in splits[split]:
            src = os.path.join(class_path, img)
            dst = os.path.join(target_dir, img)
            shutil.copy(src, dst)

    print(f"{class_name} added successfully!")


if __name__ == "__main__":
    split_and_copy("healthy")
    split_and_copy("Alternaria_leaf_blight")