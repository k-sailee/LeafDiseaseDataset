import os

BASE_DIR = "final_dataset"   # change if needed

def count_images(dataset_path):
    total_images = 0

    for split in ["train", "val", "test"]:
        split_path = os.path.join(dataset_path, split)

        if not os.path.exists(split_path):
            continue

        print(f"\n📂 {split.upper()} SET")

        split_total = 0

        for class_name in os.listdir(split_path):
            class_path = os.path.join(split_path, class_name)

            if not os.path.isdir(class_path):
                continue

            # count only image files
            count = len([
                f for f in os.listdir(class_path)
                if f.lower().endswith((".png", ".jpg", ".jpeg"))
            ])

            print(f"{class_name}: {count}")
            split_total += count

        print(f"➡ Total {split} images: {split_total}")
        total_images += split_total

    print("\n======================")
    print(f"🔥 FINAL TOTAL IMAGES: {total_images}")
    print("======================")


# Run
count_images(BASE_DIR)