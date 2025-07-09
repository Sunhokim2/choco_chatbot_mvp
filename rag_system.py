# rag_system.py
import os

# 초콜릿 데이터 파일 경로 설정
CHOCOLATE_DATA_PATH = os.path.join("data", "chocolate_data.txt")

# 데이터 로드 (애플리케이션 시작 시 한 번만 로드)
chocolate_data = ""
try:
    with open(CHOCOLATE_DATA_PATH, "r", encoding="utf-8") as f:
        chocolate_data = f.read()
except FileNotFoundError:
    print(f"Error: {CHOCOLATE_DATA_PATH} 파일을 찾을 수 없습니다. 'data' 디렉토리에 파일을 넣어주세요.")
    chocolate_data = "초콜릿 관련 데이터를 로드할 수 없습니다." # 대체 메시지

def search_chocolate_data(query: str) -> str:
    """
    사용자 쿼리에서 키워드를 추출하여 초콜릿 데이터에서 관련 내용을 검색합니다.
    단순화를 위해, 쿼리의 각 단어를 키워드로 간주하고 데이터 내에서 해당 단어가 포함된
    문장들을 찾아 반환합니다.

    더 복잡한 RAG를 위해서는 텍스트 임베딩, 벡터 데이터베이스 등이 필요하지만,
    여기서는 단순 키워드 매칭을 사용합니다.
    """
    # 쿼리에서 키워드 추출 (간단하게 공백 기준으로 분리)
    keywords = query.lower().split()

    # 검색 결과를 저장할 리스트
    found_sentences = []

    # 데이터를 문장 단위로 분리 (간단하게 온점 기준으로 분리)
    sentences = chocolate_data.split('.')

    for sentence in sentences:
        sentence_lower = sentence.lower()
        # 모든 키워드가 문장에 포함되어 있는지 확인
        if all(keyword in sentence_lower for keyword in keywords if len(keyword) > 1): # 한 글자 키워드는 무시
            found_sentences.append(sentence.strip() + ".") # 다시 온점 추가

    # 검색된 문장들을 하나의 문자열로 합쳐서 반환 (최대 N개 문장)
    # 너무 많은 컨텍스트는 OpenAI 비용 및 토큰 제한에 영향을 미치므로 적절히 조절
    return "\n".join(found_sentences[:5]) if found_sentences else "" # 최대 5개 문장 반환