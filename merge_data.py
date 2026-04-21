import os
import shutil

SRC_DIR = "scraped_data"
DEST_DIR = "merged_data"

os.makedirs(DEST_DIR, exist_ok=True)

os.makedirs(os.path.join(DEST_DIR, "healthy"), exist_ok=True)
os.makedirs(os.path.join(DEST_DIR, "Alternaria_leaf_blight"), exist_ok=True)

# Copy healthy
for file in os.listdir(os.path.join(SRC_DIR, "healthy")):
    src = os.path.join(SRC_DIR, "healthy", file)
    dst = os.path.join(DEST_DIR, "healthy", file)
    shutil.copy(src, dst)

# Merge all stages
stages = ["stage1", "stage2", "stage3", "stage4"]

counter = 0
for stage in stages:
    stage_path = os.path.join(SRC_DIR, stage)

    for file in os.listdir(stage_path):
        src = os.path.join(stage_path, file)
        dst = os.path.join(DEST_DIR, "Alternaria_leaf_blight", f"{counter}.jpg")
        shutil.copy(src, dst)
        counter += 1

print("Merging complete!")