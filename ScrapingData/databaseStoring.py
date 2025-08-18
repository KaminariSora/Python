import requests
from bs4 import BeautifulSoup
import re
from pymongo import MongoClient

# --------------------------
# MongoDB setup
# --------------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["PttDigital"]

meetings_col = db["meetings"]
attendees_col = db["attendees"]
agendas_col = db["agendas"]
details_col = db["details"]

# --------------------------
# Scraping
# --------------------------
url = "https://www.eppo.go.th/index.php/th/component/k2/item/21751-cepa-settha71"
resp = requests.get(url)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "html.parser")

content_tag = soup.find("div", class_="itemFullText")

title, meeting_no, meeting_seq, meeting_date = "", "", "", ""

if content_tag:
    centered_paras = content_tag.find_all("p", style=lambda v: v and "text-align: center" in v)
    texts = [p.get_text(strip=True) for p in centered_paras if p.get_text(strip=True)]

    if len(texts) >= 1:
        title = texts[0]
    if len(texts) >= 2:
        meeting_no = texts[1]
        m = re.search(r"\(ครั้งที่\s*(\d+)\)", meeting_no)
        if m:
            meeting_seq = int(m.group(1))
    if len(texts) >= 3:
        meeting_date = texts[2]

# --------------------------
# Sections
# --------------------------
agendas = []
resolutions = []
summaries = []
attendees = []

if content_tag:
    paragraphs = content_tag.find_all("p")
    current_section = None

    for p in paragraphs:
        text = p.get_text(strip=True)
        if not text:
            continue

        # Agenda
        a_tag = p.find("a")
        if a_tag and a_tag.get("id"):
            agendas.append(a_tag.get_text(strip=True))
            current_section = None
            continue

        # Summary / Resolution
        if re.search(r"สรุป\s*สาระ\s*สำคัญ", text):
            current_section = "summary"
            continue
        if re.search(r"มติ", text):
            current_section = "resolution"
            continue

        # Attendees (สมมติรูปแบบ: "ชื่อ - ตำแหน่ง - บทบาท")
        att_match = re.match(r"(.+?)\s*-\s*(.+?)\s*-\s*(.+)", text)
        if att_match:
            attendees.append({
                "meeting_seq": meeting_seq,
                "name": att_match.group(1),
                "position": att_match.group(2),
                "role": att_match.group(3)
            })
            continue

        # append ข้อมูลตาม section
        if current_section == "summary":
            summaries.append(text)
        elif current_section == "resolution":
            resolutions.append(text)

# --------------------------
# Insert into MongoDB
# --------------------------

# Meeting
meetings_col.insert_one({
    "title": title,
    "meeting_no": meeting_no,
    "meeting_seq": meeting_seq,
    "date": meeting_date
})

# Agendas and details
for i, agenda in enumerate(agendas, start=1):
    agendas_col.insert_one({
        "meeting_seq": meeting_seq,
        "agenda_no": i,
        "agenda_title": agenda
    })
    details_col.insert_one({
        "meeting_seq": meeting_seq,
        "agenda_no": i,
        "summary": summaries[i-1] if i-1 < len(summaries) else "",
        "resolution": resolutions[i-1] if i-1 < len(resolutions) else ""
    })

# Attendees
for att in attendees:
    attendees_col.insert_one(att)

print("✅ Inserted meeting, agendas, details, and attendees into MongoDB")
