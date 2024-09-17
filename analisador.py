# Importando as bibliotecas necessárias
from pytube import YouTube
import whisper
import openai

# Função para baixar o áudio do YouTube
def download_audio_from_youtube(url):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    audio_file = stream.download(filename="video_audio.mp4")
    return audio_file

# Função para transcrever o áudio usando Whisper
def transcribe_audio(audio_file):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    return result['text']

# Função para gerar resumo usando GPT
def summarize_text(text, api_key):
    openai.api_key = api_key
    
    response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=f"Resuma o seguinte texto:\n\n{text}\n",
      max_tokens=150,
      n=1,
      stop=None,
      temperature=0.5,
    )
    return response.choices[0].text.strip()

# Função principal para integrar tudo
def summarize_youtube_video(url, openai_api_key):
    print("Baixando o áudio do vídeo...")
    audio_file = download_audio_from_youtube(url)

    print("Transcrevendo o áudio...")
    transcription = transcribe_audio(audio_file)

    print("Gerando o resumo...")
    summary = summarize_text(transcription, openai_api_key)

    return summary

# Exemplo de uso
if __name__ == "__main__":
    youtube_url = "https://www.youtube.com/watch?v=EXAMPLE"  # Substitua pela URL do vídeo
    openai_api_key = "sua-chave-openai"
    
    resumo = summarize_youtube_video(youtube_url, openai_api_key)
    print("Resumo do vídeo:")
    print(resumo)
