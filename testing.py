import json

with open("Data/meeting_executive1_66.pdf.json", "r", encoding="utf-8") as f:
    json_data = json.load(f)

words = json_data["analyzeResult"]["pages"][0]["words"]

word_boxes = []
for word in words:
    polygon = word["polygon"]
    x_coords = polygon[::2]
    y_coords = polygon[1::2]
    center_x = sum(x_coords) / 4
    center_y = sum(y_coords) / 4
    word_boxes.append({
        "content": word["content"],
        "center_x": center_x,
        "center_y": center_y
    })

line_threshold = 0.1
# จัดคำเป็นบรรทัด
word_boxes.sort(key=lambda w: w["center_y"])

lines = []
current_line = []
current_y = None

# Loop เพื่อรวมคำที่อยู่บรรทัดเดียวกันเข้าไปใน current_line
# ถ้าคำถัดไป center_y ต่างจาก current_y มากเกิน line_threshold -> เริ่มบรรทัดใหม่
for word in word_boxes:
    if current_y is None or abs(word["center_y"] - current_y) <= line_threshold:
        current_line.append(word)
        current_y = word["center_y"]
    else:
        lines.append(sorted(current_line, key=lambda w: w["center_x"]))
        current_line = [word]
        current_y = word["center_y"]

if current_line:
    lines.append(sorted(current_line, key=lambda w: w["center_x"]))

# วนแต่ละบรรทัด
# ต่อคำแต่ละคำต่อกัน
# ถ้าระยะห่าง (space) ระหว่างคำปัจจุบันกับคำถัดไป มากกว่า 0.6 → ถือว่าเป็นช่องว่าง → ใส่ _
output_lines = []
for line in lines:
    line_text = ""
    for i, word in enumerate(line):
        line_text += word["content"]
        
        # ถ้าไม่ใช่คำสุดท้ายในบรรทัด
        if i < len(line) - 1:
            next_word = line[i + 1]
            space = next_word["center_x"] - word["center_x"]
            
            if space > 0.6:
                line_text += "_"
    output_lines.append(line_text)
    print(line_text)

with open("Data/output_1.txt", "w", encoding="utf-8") as out_file:
    for line in output_lines:
        out_file.write(line + "\n")

        
print("✅ บันทึกไฟล์เรียบร้อย: Data/meeting_executive2_66_output.txt")