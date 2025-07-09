# tts_converter.py
from gtts import gTTS
import os
from pydub import AudioSegment
import re

# 이모티콘 및 특수문자 제거 함수 (유니코드 이모지 및 기호)
def remove_emojis(text):
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002700-\U000027BF"  # Dingbats
        u"\U000024C2-\U0001F251"  # Enclosed characters
        u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        u"\U00002600-\U000026FF"  # Misc symbols
        u"\U00002B50"              # Star
        u"\U00002B06"              # Up arrow
        u"\U00002194-\U00002199"  # arrows
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text)

def convert_text_to_speech(text: str, output_filepath: str):
    """
    텍스트를 음성으로 변환하여 지정된 경로에 MP3 파일로 저장합니다.
    이모티콘 및 특수문자는 제거하고, 속도는 1.5배 빠르게 변환합니다.
    """
    try:
        # 이모티콘 및 특수문자 제거
        clean_text = remove_emojis(text)
        tts = gTTS(text=clean_text, lang='ko') # 한국어 설정
        temp_path = output_filepath + '.tmp.mp3'
        tts.save(temp_path)
        # pydub로 mp3 불러와 속도 1.5배로 변환
        sound = AudioSegment.from_file(temp_path)
        faster_sound = sound._spawn(sound.raw_data, overrides={
            "frame_rate": int(sound.frame_rate * 1.5)
        }).set_frame_rate(sound.frame_rate)
        faster_sound.export(output_filepath, format="mp3")
        os.remove(temp_path)
        print(f"음성 파일 저장됨: {output_filepath}")
    except Exception as e:
        print(f"TTS 변환 중 오류 발생: {e}")
        # 오류 발생 시 빈 파일 생성 또는 예외 처리 (프론트엔드에서 음성 재생 실패)
        with open(output_filepath, 'w') as f:
            f.write("") # 빈 파일이라도 만들어야 FileResponse 오류 방지