# openai_integration.py
from openai import OpenAI
import os

# OpenAI API 키 환경 변수에서 로드
# 예: export OPENAI_API_KEY="YOUR_API_KEY"
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_ai_answer(question: str, context: str) -> str:
    """
    OpenAI API를 사용하여 질문에 대한 답변을 생성합니다.
    RAG 컨텍스트가 제공되면 이를 활용하여 답변합니다.
    """
    messages = [
        {"role": "system", "content": "당신은 초콜릿에 대한 전문 지식을 갖춘 친절한 AI 가이드입니다. 제공된 정보를 바탕으로 사용자의 질문에 정확하고 간결하게 답변해주세요."},
    ]

    if context:
        # RAG 컨텍스트를 시스템 프롬프트에 포함
        messages.append({"role": "system", "content": f"다음은 초콜릿 관련 정보입니다: {context}\n\n이 정보를 참고하여 답변해주세요."})

    messages.append({"role": "user", "content": question})

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # 또는 gpt-4, gpt-4o 등 사용 가능한 모델
            messages=messages,
            max_tokens=200, # 답변 길이 제한
            temperature=0.7 # 창의성 조절
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API 호출 중 오류 발생: {e}")
        return "죄송합니다, AI 답변을 생성하는 데 문제가 발생했습니다."