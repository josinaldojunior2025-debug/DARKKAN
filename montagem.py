from moviepy import ImageClip, AudioFileClip

def criar_video_darkkan():
    print("🎬 Iniciando a montagem profissional...")
    
    try:
        # 1. Carregar os arquivos que já estão na sua pasta
        audio = AudioFileClip("audio_final.mp3")
        
        # 2. Criar o clipe de imagem (usando a nova sintaxe da v2.x)
        # Na versão nova, a duração é passada diretamente ou via with_duration
        video = ImageClip("imagem_final.jpg").with_duration(audio.duration)
        
        # 3. Adicionar o áudio
        video = video.with_audio(audio)
        
        # 4. Renderizar o arquivo final
        print("💾 Renderizando MP4... aguarde a conclusão.")
        video.write_videofile("video_darkkan_final.mp4", fps=24, codec="libx264")
        
        print("✅ SUCESSO! Baixe o 'video_darkkan_final.mp4' na esquerda.")
        
    except Exception as e:
        print(f"❌ Erro na montagem: {e}")

if __name__ == "__main__":
    criar_video_darkkan()