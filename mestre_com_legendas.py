import os
from gtts import gTTS
from moviepy import ImageClip, AudioFileClip, TextClip, CompositeVideoClip

def criar_video_com_legendas():
    print("🚀 DARKKAN: Iniciando produção com legendas corrigidas...")

    try:
        # 1. Carregar Roteiro
        with open("roteiro_final.txt", "r", encoding="utf-8") as f:
            texto = f.read()

        # 2. Gerar Áudio
        print("🎙️ Gerando voz...")
        tts = gTTS(text=texto, lang='pt', tld='com.br')
        tts.save("audio_temp.mp3")
        audio = AudioFileClip("audio_temp.mp3")

        # 3. Criar Fundo (Imagem)
        fundo = ImageClip("imagem_final.jpg").with_duration(audio.duration)
        
        # 4. Criar Legenda (Forçando números inteiros para evitar o erro)
        largura_legenda = int(fundo.w * 0.8) # Transformando em inteiro
        
        print("📝 Criando camadas de texto...")
        txt_clip = TextClip(
            text=texto, 
            font_size=50, 
            color='white', 
            method='caption',
            size=(largura_legenda, None)
        ).with_duration(audio.duration).with_position('center')

        # 5. Unir Tudo
        video_final = CompositeVideoClip([fundo, txt_clip]).with_audio(audio)
        
        print("💾 Renderizando vídeo final... isso pode levar alguns segundos.")
        video_final.write_videofile("DARKKAN_VIRAL.mp4", fps=24, codec="libx264")
        
        print("✅ SUCESSO! O vídeo 'DARKKAN_VIRAL.mp4' está pronto.")

    except Exception as e:
        print(f"❌ Erro na produção: {e}")

if __name__ == "__main__":
    criar_video_com_legendas()