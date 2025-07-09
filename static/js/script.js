// static/js/script.js
document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const chatBox = document.getElementById('chat-box');

    const sendMessage = async () => {
        const message = userInput.value.trim();
        if (message === "") {
            return;
        }

        // 사용자 메시지 표시
        appendMessage(message, 'user');
        userInput.value = ''; // 입력창 비우기

        // 로딩 애니메이션 메시지 표시
        const loadingMessageDiv = appendMessage("답변 생성 중...", 'ai-message loading-message');
        let dotCount = 1;
        let loadingInterval = setInterval(() => {
            dotCount = dotCount % 3 + 1;
            loadingMessageDiv.querySelector('p').textContent = '.'.repeat(dotCount).split('').join(' ');
        }, 500);
        chatBox.scrollTop = chatBox.scrollHeight; // 스크롤 하단으로

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // 로딩 메시지 제거 및 애니메이션 중지
            clearInterval(loadingInterval);
            loadingMessageDiv.remove();

            // AI 답변 텍스트 표시
            const aiMessageDiv = appendMessage(data.answer_text, 'ai');
            chatBox.scrollTop = chatBox.scrollHeight;

            // 음성 재생
            if (data.audio_url) {
                const audio = new Audio(data.audio_url);
                audio.play().catch(e => console.error("오디오 재생 오류:", e));
            }

        } catch (error) {
            console.error('채팅 중 오류 발생:', error);
            // 로딩 메시지 제거 및 애니메이션 중지
            clearInterval(loadingInterval);
            loadingMessageDiv.remove();
            appendMessage(`오류 발생: ${error.message}. 다시 시도해주세요.`, 'ai error-message');
        }
    };

    const appendMessage = (text, sender) => {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        // sender가 'user' 또는 'ai'면 명확하게 클래스 매핑
        if (sender === 'user') {
            messageDiv.classList.add('user-message');
        } else if (sender === 'ai') {
            messageDiv.classList.add('ai-message');
        } else {
            // 여러 클래스(예: 'ai-message loading-message') 지원
            sender.split(' ').forEach(cls => messageDiv.classList.add(cls));
        }

        const p = document.createElement('p');
        p.textContent = text;
        messageDiv.appendChild(p);

        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight; // 스크롤을 최신 메시지로 이동
        return messageDiv; // 로딩 메시지 제거를 위해 반환
    };

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});
