# 🗑️ Trash Track - AI Module

## Overview
Trash Track is a smart waste management system that uses AI to detect and classify street waste into recyclable categories, helping municipalities manage waste more efficiently.

## AI Module
This module is responsible for waste detection and classification using YOLOv8.

### Waste Classification Model
Built and trained by **Mohamed Farag** — detects and classifies waste from street images into 6 categories to support recycling operations.

## Classes
- Plastic
- Glass
- Metal
- Paper
- Organic
- Non-Recyclable

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```python
from ultralytics import YOLO

model = YOLO('best.pt')
results = model.predict(source='image.jpg', conf=0.25)
results[0].show()
```

## Project Structure

Master_Waste_Dataset/
├── datasets/ ← Raw datasets (not included in repo)
├── notebooks/ ← Data exploration & training notebooks
├── scripts/ ← Processing scripts
└── output/model/ ← Trained model (best.pt)



## Model
- Architecture: YOLOv8
- Input: Street images (any resolution)
- Output: Detected waste with class and confidence score

## Team
| Name | Role |
|------|------|
| Mohamed Farag | AI Engineer — Waste Classification Model |
| Hussien Appas | AI Engineer |

## License
This project is part of a graduation project.