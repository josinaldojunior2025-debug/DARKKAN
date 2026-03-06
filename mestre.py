import os
from gtts import gTTS
from moviepy import ImageClip, AudioFileClip

def modo_mestre():
    print("🚀 DARKKAN: Iniciando automação total...")

    # 1. Ler o roteiro
    if not os.path.exists("roteiro_final.txt"):
        print("❌ Erro: Crie o arquivo 'roteiro_final.txt' primeiro!")
        return
        
    with open("roteiro_final.txt", "r", encoding="utf-8") as f:
        texto = f.read()

    # 2. Gerar Áudio (Usando gTTS para evitar erros de conexão no Codespace)
    print("🎙️ Gerando voz...")
    tts = gTTS(text=texto, lang='pt', tld='com.br')
    tts.save("audio_mestre.mp3")

    # 3. Montar Vídeo
    print("🎬 Montando vídeo final...")
    try:
        audio = AudioFileClip("audio_mestre.mp3")
        # Usamos a imagem que você já tem na pasta
        video = ImageClip("imagem_final.jpg").with_duration(audio.duration)
        video = video.with_audio(audio)
        
        video.write_videofile("PRODUCAO_FINAL.mp4", fps=24, codec="libx264")
        print("✅ SUCESSO! O vídeo 'PRODUCAO_FINAL.mp4' está pronto para o YouTube.")
        
    except Exception as e:
        print(f"❌ Erro na montagem: {e}")

if __name__ == "__main__":
    modo_mestre()