from google.cloud import translate_v2 as translate
import os

# Configuração da chave de autenticação (você precisa de uma chave da Google Cloud)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path_to_your_google_credentials.json'

translate_client = translate.Client()

# Função para traduzir texto
def translate_text(text, target_language='pt'):
    result = translate_client.translate(text, target_lang=target_language)
    return result['translatedText']

# Exemplo de uso dentro do seu Flask app
@app.route('/translate', methods=['POST'])
def translate_question():
    if 'username' not in session:
        return redirect(url_for('login'))

    text_to_translate = request.form['text']
    translated_text = translate_text(text_to_translate, target_language='pt')  # Traduz para português

    return render_template('translated_question.html', original=text_to_translate, translated=translated_text)


from google.cloud import translate_v2 as translate
import os

# Configuração da chave de autenticação (você precisa de uma chave da Google Cloud)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path_to_your_google_credentials.json'

translate_client = translate.Client()

# Função para traduzir texto
def translate_text(text, target_language='pt'):
    result = translate_client.translate(text, target_lang=target_language)
    return result['translatedText']

# Exemplo de uso dentro do seu Flask app
@app.route('/translate', methods=['POST'])
def translate_question():
    if 'username' not in session:
        return redirect(url_for('login'))

    text_to_translate = request.form['text']
    translated_text = translate_text(text_to_translate, target_language='pt')  # Traduz para português

    return render_template('translated_question.html', original=text_to_translate, translated=translated_text)

from google.cloud import speech_v1p1beta1 as speech
import io

def transcribe_audio(audio_file):
    client = speech.SpeechClient()

    with io.open(audio_file, 'rb') as audio:
        content = audio.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="pt-BR",
    )

    response = client.recognize(config=config, audio=audio)

    # Transcrição do áudio
    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))

# Chamando a função
transcribe_audio('path_to_audio_file.wav')
