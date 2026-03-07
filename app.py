import streamlit as st
import os
from gtts import gTTS
from moviepy import ImageClip, AudioFileClip, TextClip, CompositeVideoClip

st.set_page_config(page_title="DARKKAN Engine", page_icon="🎬")

st.title("🎬 DARKKAN: Gerador de Vídeos Dark")

# Configuração para o MoviePy encontrar o ImageMagick no servidor
os.environ["IMAGEIO_VAR_NAME"] = "ffmpeg"

tema = st.text_input("Qual o tema do vídeo?", "O poder do silêncio")
roteiro = st.text_area("Roteiro:", "A disciplina é a ponte entre objetivos e conquistas.")

if st.button("🚀 GERAR VÍDEO AGORA"):
    with st.spinner("Produzindo..."):
        try:
            tts = gTTS(text=roteiro, lang='pt', tld='com.br')
            tts.save("audio_app.mp3")
            audio = AudioFileClip("audio_app.mp3")
            fundo = ImageClip("imagem_final.jpg").with_duration(audio.duration)
            
            txt_clip = TextClip(
                text=roteiro, font_size=50, color='white', 
                method='caption', size=(int(fundo.w*0.8), None)
            ).with_duration(audio.duration).with_position('center')

            video_final = CompositeVideoClip([fundo, txt_clip]).with_audio(audio)
            video_final.write_videofile("darkkan_web.mp4", fps=24, codec="libx264")

            st.video("darkkan_web.mp4")
            with open("darkkan_web.mp4", "rb") as f:
                st.download_button("📥 Baixar Vídeo", f, "video_darkkan.mp4")
        except Exception as e:
            st.error(f"Erro: {e}")