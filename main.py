import os
import requests
from gtts import gTTS

def gerar_darkkan_v2():
    # Texto para o vídeo
    texto_video = "A persistência é o caminho do êxito. O sistema Darkkan está sendo construído com sucesso."
    
    print("🎙️ Gerando voz (Modo Estável)...")
    try:
        # gTTS é quase impossível de ser bloqueado pelo GitHub
        tts = gTTS(text=texto_video, lang='pt', tld='com.br')
        tts.save("audio_final.mp3")
        print("✅ Áudio gerado com sucesso!")
    except Exception as e:
        print(f"❌ Erro no áudio: {e}")

    print("🎨 Gerando imagem HD...")
    try:
        # Usando um link direto de imagem de alta qualidade
        url_img = "https://picsum.photos/1920/1080"
        res = requests.get(url_img, timeout=30)
        with open("imagem_final.jpg", "wb") as f:
            f.write(res.content)
        print("✅ Imagem gerada com sucesso!")
    except Exception as e:
        print(f"❌ Erro na imagem: {e}")

if __name__ == "__main__":
    gerar_darkkan_v2()