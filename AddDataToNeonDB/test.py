from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# 1. สร้างโครงสร้างข้อมูลให้ตรงกับ Payload ใน Swagger (name, email)
class UserPayload(BaseModel):
    name: str
    email: str

# 2. สร้าง Endpoint ให้ตรงกับ Path ใน Java Swagger
@app.post("/api/v1/user/create")
async def create_user(data: UserPayload):
    # ข้อมูลที่ Java ส่งมาจะมาอยู่ในตัวแปร data
    print(f"--- AI Agent Received Data ---")
    print(f"Name: {data.name}")
    print(f"Email: {data.email}")
    
    # ตรงนี้คือจุดที่คุณจะเอา data.name ไปให้ AI Agent ทำงานต่อ
    
    # 3. ตอบกลับให้ตรงตาม Format ที่ Swagger กำหนด (Response 200)
    return {
        "code": "200",
        "message": "Success",
        "data": {
            "userId": "AI-999",
            "token": "AI-AGENT-TOKEN-001"
        }
    }

if __name__ == "__main__":
    # รันบน localhost พอร์ต 8080
    uvicorn.run(app, port=8081)