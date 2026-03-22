import os
import cv2
import random
import numpy as np

BASE_DIR = "final_dataset/train"   # augment only training data

TARGET_CLASS = "rust_diseases"
AUG_CLASSES = ["leaf_spot", "leaf_blight"]

# ----------------------------
# Augmentation Functions
# ----------------------------
def augment_image(img):

    aug_type = random.choice([
        "flip", "rotate", "brightness", "zoom", "noise"
    ])

    if aug_type == "flip":
        img = cv2.flip(img, 1)

    elif aug_type == "rotate":
        angle = random.randint(-25, 25)
        h, w = img.shape[:2]
        M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1)
        img = cv2.warpAffine(img, M, (w, h))

    elif aug_type == "brightness":
        value = random.randint(-40, 40)
        img = cv2.convertScaleAbs(img, alpha=1, beta=value)

    elif aug_type == "zoom":
        h, w = img.shape[:2]
        scale = random.uniform(1.0, 1.3)
        resized = cv2.resize(img, None, fx=scale, fy=scale)
        img = resized[0:h, 0:w]

    elif aug_type == "noise":
        noise = np.random.randint(0, 30, img.shape, dtype='uint8')
        img = cv2.add(img, noise)

    return img


# ----------------------------
# Count images
# ----------------------------
def count_images(folder):
    return len([
        f for f in os.listdir(folder)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ])


# ----------------------------
# Augment function
# ----------------------------
def augment_class(class_name, target_count):

    class_path = os.path.join(BASE_DIR, class_name)
    images = [
        f for f in os.listdir(class_path)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    current_count = len(images)
    needed = target_count - current_count

    print(f"\n🔹 {class_name}")
    print(f"Current: {current_count}, Target: {target_count}, Need: {needed}")

    if needed <= 0:
        print("Already sufficient")
        return

    i = 0
    while i < needed:
        img_name = random.choice(images)
        img_path = os.path.join(class_path, img_name)

        img = cv2.imread(img_path)
        if img is None:
            continue

        aug_img = augment_image(img)

        new_name = f"aug_{i}_{img_name}"
        save_path = os.path.join(class_path, new_name)

        cv2.imwrite(save_path, aug_img)
        i += 1

    print(f"✅ Added {needed} images")


# ----------------------------
# MAIN
# ----------------------------
target_path = os.path.join(BASE_DIR, TARGET_CLASS)
target_count = count_images(target_path)

print(f"🎯 Target class ({TARGET_CLASS}) count: {target_count}")

for cls in AUG_CLASSES:
    augment_class(cls, target_count)

print("\n🔥 Augmentation Complete!")