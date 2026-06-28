from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
import anthropic
import os

app = Flask(__name__)

CLAUDE_API_KEY = os.environ.get('CLAUDE_API_KEY')

@app.route('/incoming-call', methods=['POST'])
def incoming_call():
    """Обработка входящего звонка от Twilio"""
    from_number = request.form.get('From')

    try:
        # Вызываем Claude API
        client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": "Ты Алекс - голосовой ассистент TBILICO (сеть кофейных точек самообслуживания в Грузии). Звонит клиент из номера " + str(from_number) + ". Поздравь его, представься кратко и спроси чем помочь. Ответь в 1-2 предложениях на русском языке. Будь дружелюбным и профессиональным."
            }]
        )

        response_text = message.content[0].text
    except Exception as e:
        print(f"Error: {str(e)}")
        response_text = "Извините, произошла техническая ошибка. Попробуйте позже или свяжитесь с поддержкой."

    # Генерируем TwiML ответ
    resp = VoiceResponse()
    resp.say(response_text, language='ru-RU', voice='alice')
    resp.hangup()

    return str(resp)

@app.route('/health', methods=['GET'])
def health():
    """Проверка здоровья сервера"""
    return {'status': 'ok'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
