import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import json
import matplotlib.font_manager as fm
import os
import pandas as pd

# Use a default font that is likely to exist on the system
thai_font = fm.FontProperties(fname="C:/Windows/Fonts/tahoma.ttf")

with open("Data/meeting_executive1_66.pdf.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)

paragraphs = json_data["analyzeResult"]["paragraphs"]

DPI = 1
page_to_plot = 26

page_paragraphs = [p for p in paragraphs if any(br["pageNumber"] == page_to_plot for br in p["boundingRegions"])]

all_x = []
all_y = []
if page_paragraphs:
    for paragraph in page_paragraphs:
        for br in paragraph["boundingRegions"]:
            if br["pageNumber"] == page_to_plot:
                polygon = br["polygon"]
                if len(polygon) >= 6 and len(polygon) % 2 == 0:
                    try:
                        x_coords = [polygon[i] * DPI for i in range(0, len(polygon), 2)]
                        y_coords = [polygon[i+1] * DPI for i in range(1, len(polygon), 2)]
                        all_x.extend(x_coords)
                        all_y.extend(y_coords)
                    except IndexError as e:
                        print(f"Error processing polygon {polygon}: {e}")
                        continue
    
    if all_x and all_y:
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        x_padding = (max_x - min_x) * 0.1
        y_padding = (max_y - min_y) * 0.1
        xlim_min, xlim_max = min_x - x_padding, max_x + x_padding
        ylim_min, ylim_max = min_y - y_padding, max_y + y_padding
    else:
        xlim_min, xlim_max = 0, 8.5
        ylim_min, ylim_max = 0, 11
else:
    xlim_min, xlim_max = 0, 8.5
    ylim_min, ylim_max = 0, 11

fig, ax = plt.subplots(figsize=(8, 11))

for i, paragraph in enumerate(page_paragraphs):
    for br in paragraph["boundingRegions"]:
        if br["pageNumber"] == page_to_plot:
            polygon = br["polygon"]
            if len(polygon) < 6 or len(polygon) % 2 != 0:
                continue
            
            points = [(polygon[i] * DPI, polygon[i+1] * DPI) for i in range(0, len(polygon), 2)]
            colors = ['black']
            color = colors[i % len(colors)]
            
            poly = Polygon(points, closed=True, edgecolor=color, facecolor='none', linewidth=2)
            ax.add_patch(poly)

            content = paragraph.get("content", "")
            if len(content) > 100:
                content = content[:100] + "..."
            
            text_x, text_y = points[0]
            label = f"{content}"
            ax.text(text_x, text_y, label, fontproperties=thai_font, fontsize=8,
                    verticalalignment='top')

ax.set_xlim(xlim_min, xlim_max)
ax.set_ylim(ylim_max, ylim_min)
ax.set_aspect('equal')
ax.set_title(f"Paragraph Bounding Boxes - Page {page_to_plot}", fontproperties=thai_font, fontsize=14)
ax.grid(True, alpha=0.3)
ax.set_xlabel("X Coordinate", fontproperties=thai_font)
ax.set_ylabel("Y Coordinate", fontproperties=thai_font)

ax.text(0.02, 0.98, f"Total Paragraphs: {len(page_paragraphs)}",
        transform=ax.transAxes, fontproperties=thai_font,
        bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgray', alpha=0.8),
        verticalalignment='top', fontsize=10)

plt.tight_layout()
plt.savefig("paragraph_bounding.png")