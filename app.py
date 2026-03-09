import streamlit as st
import os
import requests
import time
import glob
from gtts import gTTS
from moviepy import ImageClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips

st.set_page_config(page_title="DARKKAN PRO - Estável", page_icon="🛡️")
st.title("🛡️ DARKKAN: Versão Ultra Estável")

os.environ["IMAGEIO_VAR_NAME"] = "ffmpeg"

def gerar_imagem_ia(prompt_imagem, index):
    url = f"https://image.pollinations.ai/prompt/{prompt_imagem}?width=1080&height=1920&seed={index}&nologo=true"
    try:
        response = requests.get(url, timeout=20)
        nome_arquivo = f"cena_{index}.jpg"
        with open(nome_arquivo, "wb") as f:
            f.write(response.content)
        return nome_arquivo
    except:
        return "imagem_final.jpg" # Fallback caso a IA falhe

tema = st.text_input("Tema Visual:", "Dark aesthetic warrior")
roteiro_completo = st.text_area("Roteiro (separe frases por ponto final):")

if st.button("🚀 GERAR VÍDEO AGORA"):
    # Limpeza profunda inicial
    for f in glob.glob("temp_*.*") + glob.glob("audio_*.mp3") + glob.glob("cena_*.jpg"):
        try: os.remove(f)
        except: pass

    with st.spinner("DARKKAN está construindo seu vídeo..."):
        try:
            frases = [f.strip() for f in roteiro_completo.split('.') if len(f.strip()) > 5]
            clips_de_video = []
            
            for i, frase in enumerate(frases):
                # 1. Áudio Único por cena
                audio_path = f"audio_{i}.mp3"
                tts = gTTS(text=frase, lang='pt', tld='com.br')
                tts.save(audio_path)
                
                # Forçamos o MoviePy a carregar o áudio com buffer
                audio_clip = AudioFileClip(audio_path)
                
                # 2. Imagem da Cena
                img_path = gerar_imagem_ia(f"{tema}, cinematic dark background", i)
                
                # 3. Montagem da Cena
                img_clip = ImageClip(img_path).with_duration(audio_clip.duration)
                
                txt_clip = TextClip(
                    text=frase.upper(), font_size=55, color='yellow',
                    method='caption', size=(int(img_clip.w*0.8), None),
                    stroke_color='black', stroke_width=2
                ).with_duration(audio_clip.duration).with_position(('center', 0.85), relative=True)
                
                cena = CompositeVideoClip([img_clip, txt_clip]).with_audio(audio_clip)
                clips_de_video.append(cena)
            
            # 4. Renderização com parâmetros de compatibilidade total
            video_final = concatenate_videoclips(clips_de_video, method="compose")
            
            # O SEGREDO: Usamos 'libx264' e forçamos o áudio para um arquivo temporário único
            output_file = "darkkan_final.mp4"
            video_final.write_videofile(
                output_file, 
                fps=24, 
                codec="libx264", 
                audio_codec="aac", 
                temp_audiofile='temp-audio-final.m4a', 
                remove_temp=True,
                write_logfile=False
            )
            
            st.video(output_file)
            st.success("✅ Vídeo gerado com sucesso!")

        except Exception as e:
            st.error(f"Erro no processamento: {e}")