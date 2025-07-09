from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os
import uuid # 음성 파일 고유 ID 생성용

load_dotenv()
app = FastAPI()

# 정적 파일 (CSS, JS, 오디오 파일) 서빙
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 템플릿 설정
templates = Jinja2Templates(directory="templates")

# 필요한 모듈 임포트 (아래에서 구현 예정)
from rag_system import search_chocolate_data
from openai_integration import get_ai_answer
from tts_converter import convert_text_to_speech

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat", response_class=JSONResponse)
async def chat(request: Request):
    try:
        data = await request.json()
        user_message = data.get("message")
        if not user_message:
            raise HTTPException(status_code=400, detail="메시지 내용을 입력해주세요.")

        # 1. RAG 검색
        # 예: user_message를 기반으로 관련 초콜릿 데이터를 검색
        relevant_context = search_chocolate_data(user_message)

        # 2. OpenAI API를 통한 답변 생성
        # 검색된 컨텍스트와 질문을 조합하여 AI에게 질문
        ai_answer_text = get_ai_answer(user_message, relevant_context)

        if not ai_answer_text:
            ai_answer_text = "죄송합니다. 요청하신 질문에 대한 답변을 찾을 수 없습니다."

        # 3. 답변 텍스트를 음성으로 변환 및 파일 저장
        audio_filename = f"answer_{uuid.uuid4()}.mp3"
        audio_filepath = os.path.join("static", "audio", audio_filename)
        os.makedirs(os.path.dirname(audio_filepath), exist_ok=True) # 디렉토리 없으면 생성

        convert_text_to_speech(ai_answer_text, audio_filepath)

        # 4. 음성 파일 URL 생성 및 반환
        audio_url = f"/static/audio/{audio_filename}"

        return JSONResponse({
            "answer_text": ai_answer_text,
            "audio_url": audio_url
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # 개발 시에는 --reload 옵션으로 코드 변경 자동 반영
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)