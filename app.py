import streamlit as st
import os
import requests
import time
import glob
from gtts import gTTS
from moviepy import ImageClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips

st.set_page_config(page_title="DARKKAN 2.0 - Estável", page_icon="🛡️")
st.title("🛡️ DARKKAN: Motor de Produção Blindado")

os.environ["IMAGEIO_VAR_NAME"] = "ffmpeg"

def limpar_temporarios():
    # Remove arquivos de tentativas que falharam para evitar conflitos
    for f in glob.glob("*.mp3") + glob.glob("*.jpg") + glob.glob("*.mp4"):
        if f not in ["imagem_final.jpg"]: # Protege sua imagem base se houver
            try: os.remove(f)
            except: pass

def gerar_imagem_ia(prompt_imagem, index):
    url = f"https://image.pollinations.ai/prompt/{prompt_imagem}?width=1080&height=1920&seed={index}&nologo=true"
    response = requests.get(url)
    nome_arquivo = f"cena_{index}.jpg"
    with open(nome_arquivo, "wb") as f:
        f.write(response.content)
    time.sleep(1) # Pausa de segurança para o disco registrar o arquivo
    return nome_arquivo

tema = st.text_input("Tema Visual:", "Dark aesthetic warrior")
roteiro_completo = st.text_area("Roteiro (separe por pontos):")

if st.button("🚀 GERAR VÍDEO SEM ERROS"):
    limpar_temporarios() # Começa do zero
    with st.spinner("Processando cenas com estabilidade..."):
        try:
            frases = [f.strip() for f in roteiro_completo.split('.') if len(f.strip()) > 5]
            clips_de_video = []
            
            for i, frase in enumerate(frases):
                # 1. Áudio
                audio_path = f"audio_{i}.mp3"
                gTTS(text=frase, lang='pt', tld='com.br').save(audio_path)
                audio_clip = AudioFileClip(audio_path)
                
                # 2. Imagem
                img_path = gerar_imagem_ia(f"{tema}, cinematic", i)
                
                # 3. Clip
                img_clip = ImageClip(img_path).with_duration(audio_clip.duration)
                txt_clip = TextClip(
                    text=frase.upper(), font_size=50, color='yellow',
                    method='caption', size=(int(img_clip.w*0.8), None),
                    stroke_color='black', stroke_width=2
                ).with_duration(audio_clip.duration).with_position(('center', 0.8), relative=True)
                
                cena = CompositeVideoClip([img_clip, txt_clip]).with_audio(audio_clip)
                clips_de_video.append(cena)
            
            # 4. Renderização com Codec de Segurança
            video_final = concatenate_videoclips(clips_de_video, method="compose")
            # Usando temp_audiofile para evitar o erro de avcodec_send_packet
            video_final.write_videofile("darkkan_estavel.mp4", fps=24, codec="libx264", audio_codec="aac", temp_audiofile='temp-audio.m4a', remove_temp=True)
            
            st.video("darkkan_estavel.mp4")
            
        except Exception as e:
            st.error(f"Erro detectado: {e}")