import os
import cv2
import random
import numpy as np
from tqdm import tqdm

# -------------------------------
# CONFIG
# -------------------------------
BASE_DIR = "final_dataset/train"

TARGET_COUNT = 2000

TARGET_CLASSES = [
    "Alternaria_leaf_blight",
    "anthracnose",
    "chlorosis",
    "initial_stage"
]

# -------------------------------
# AUGMENTATION FUNCTIONS
# -------------------------------
def augment_image(img):
    aug_type = random.choice([
        "flip", "rotate", "brightness", "zoom", "noise"
    ])

    # Flip
    if aug_type == "flip":
        return cv2.flip(img, 1)

    # Rotation
    elif aug_type == "rotate":
        angle = random.randint(-25, 25)
        h, w = img.shape[:2]
        M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1)
        return cv2.warpAffine(img, M, (w, h))

    # Brightness (FIXED)
    elif aug_type == "brightness":
        value = random.randint(-50, 50)

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.int16)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] + value, 0, 255)
        hsv = hsv.astype(np.uint8)

        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # Zoom
    elif aug_type == "zoom":
        h, w = img.shape[:2]
        scale = random.uniform(1.0, 1.3)
        resized = cv2.resize(img, None, fx=scale, fy=scale)

        # Crop back to original size
        return resized[0:h, 0:w]

    # Noise
    elif aug_type == "noise":
        noise = np.random.randint(0, 30, img.shape, dtype='uint8')
        return cv2.add(img, noise)

    return img


# -------------------------------
# AUGMENT CLASS
# -------------------------------
def augment_class(class_name):
    class_path = os.path.join(BASE_DIR, class_name)
    images = os.listdir(class_path)

    current_count = len(images)

    print(f"\n{class_name}: {current_count} images")

    if current_count >= TARGET_COUNT:
        print("Already balanced")
        return

    needed = TARGET_COUNT - current_count
    print(f"Augmenting {needed} images...")

    for i in tqdm(range(needed)):
        img_name = random.choice(images)
        img_path = os.path.join(class_path, img_name)

        img = cv2.imread(img_path)

        if img is None:
            continue

        aug_img = augment_image(img)

        new_name = f"aug_{i}_{img_name}"
        save_path = os.path.join(class_path, new_name)

        cv2.imwrite(save_path, aug_img)

    print(f"{class_name} balanced to {TARGET_COUNT}")


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":
    for cls in TARGET_CLASSES:
        augment_class(cls)

    print("\n✅ Augmentation complete!")