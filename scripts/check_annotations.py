import os
import glob
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from pathlib import Path

output_path = os.path.join("output", "final_dataset")
FINAL_CLASSES = ['Plastic', 'Glass', 'Metal', 'Paper', 'Organic', 'Non-Recyclable']
COLORS = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta']

random.seed(42)

print("🖼️ بنعرض الصور...\n")
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

for idx, cls_name in enumerate(FINAL_CLASSES):
    found = False

    if cls_name == 'Plastic':
        pattern = os.path.join(output_path, "train", "images", "Garbage_Detection_*.jpg")
        candidates = glob.glob(pattern)
        if not candidates:
            pattern = os.path.join(output_path, "train", "images", "Pakistan_Garbage_*.jpg")
            candidates = glob.glob(pattern)
    else:
        pattern = os.path.join(output_path, "train", "images", f"aug_{cls_name}_*.jpg")
        candidates = glob.glob(pattern)

    print(f"  {cls_name}: لاقي {len(candidates)} صورة")

    random.shuffle(candidates)

    for img_path in candidates[:20]:
        stem = Path(img_path).stem
        label_path = os.path.join(output_path, "train", "labels", f"{stem}.txt")

        if not os.path.exists(label_path):
            continue

        try:
            img = Image.open(img_path).convert("RGB")
            img = img.resize((416, 416))
        except:
            continue

        w, h = img.size
        ax = axes[idx]
        ax.imshow(img)

        with open(label_path, 'r') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            cid = int(float(parts[0]))
            x_c, y_c, bw, bh = map(float, parts[1:5])
            x1 = (x_c - bw/2) * w
            y1 = (y_c - bh/2) * h
            rect = patches.Rectangle(
                (x1, y1), bw*w, bh*h,
                linewidth=2,
                edgecolor=COLORS[cid],
                facecolor='none'
            )
            ax.add_patch(rect)
            ax.text(x1, y1-5, FINAL_CLASSES[cid],
                   color=COLORS[cid], fontsize=8, fontweight='bold')

        ax.set_title(cls_name, fontsize=12)
        ax.axis('off')
        img.close()
        found = True
        print(f"  ✅ {cls_name}: {stem}")
        break

    if not found:
        axes[idx].set_title(f"{cls_name} - مش لاقي")
        axes[idx].axis('off')
        print(f"  ⚠️ مش لاقي {cls_name}")

plt.suptitle('Sample Annotations per Class', fontsize=15)
plt.tight_layout()
plt.savefig(os.path.join("notebooks", "annotation_samples.png"), dpi=100)
print("\n✅ اتحفظت في notebooks/annotation_samples.png")