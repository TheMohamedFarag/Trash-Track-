import os
import glob
import shutil
import random
from pathlib import Path

random.seed(42)

# المسارات
street_data_path = "D:/Data Traning"
subset_path = "output/subset_resized"

# الـ classes في الداتا الجديدة
STREET_CLASSES = ['Glass', 'Metal', 'Non-Recyclable', 'Organic', 'Paper', 'Plastic', 'garbage']

# الـ classes بتاعتنا
FINAL_CLASSES = ['Plastic', 'Glass', 'Metal', 'Paper', 'Organic', 'Non-Recyclable']

# mapping من classes الداتا الجديدة لـ classes بتاعتنا
CLASS_MAP = {
    0: 1,  # Glass → Glass
    1: 2,  # Metal → Metal
    2: 5,  # Non-Recyclable → Non-Recyclable
    3: 4,  # Organic → Organic
    4: 3,  # Paper → Paper
    5: 0,  # Plastic → Plastic
    6: -1, # garbage → مش هنستخدمها
}

print("🔄 بنضيف الداتا الجديدة...\n")

copied = 0
skipped = 0

for split in ['train', 'valid', 'test']:
    # تحويل اسم الـ split
    out_split = 'val' if split == 'valid' else split
    
    images = glob.glob(os.path.join(street_data_path, split, 'images', '*.jpg')) + \
             glob.glob(os.path.join(street_data_path, split, 'images', '*.png'))
    
    for img_path in images:
        stem = Path(img_path).stem
        ext = Path(img_path).suffix
        label_path = os.path.join(street_data_path, split, 'labels', f'{stem}.txt')
        
        if not os.path.exists(label_path):
            skipped += 1
            continue
        
        # اقرأ الـ labels وحول الـ classes
        new_lines = []
        with open(label_path, 'r') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            old_class = int(parts[0])
            new_class = CLASS_MAP.get(old_class, -1)
            
            if new_class == -1:
                continue
            
            new_lines.append(f"{new_class} {' '.join(parts[1:])}\n")
        
        if not new_lines:
            skipped += 1
            continue
        
        # اسم جديد للملف
        new_name = f"street_{stem}"
        
        # انسخ الصورة
        dst_img = os.path.join(subset_path, out_split, 'images', f'{new_name}{ext}')
        shutil.copy2(img_path, dst_img)
        
        # اكتب الـ label
        dst_label = os.path.join(subset_path, out_split, 'labels', f'{new_name}.txt')
        with open(dst_label, 'w') as f:
            f.writelines(new_lines)
        
        copied += 1

print(f"✅ اتضافت {copied} صورة")
print(f"⚠️ اتسكبت {skipped} صورة")

# إحصائيات
print("\n📊 الإجمالي بعد الإضافة:")
for split in ['train', 'val', 'test']:
    imgs = glob.glob(os.path.join(subset_path, split, 'images', '*.jpg')) + \
           glob.glob(os.path.join(subset_path, split, 'images', '*.png'))
    print(f"  {split}: {len(imgs)} صورة")