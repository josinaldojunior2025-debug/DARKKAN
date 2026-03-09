import streamlit as st
import os
import requests
import glob
import time
import traceback
import imageio
from gtts import gTTS

# --- CORREÇÃO DE AMBIENTE ---
os.environ["IMAGEIO_VAR_NAME"] = "ffmpeg"

st.set_page_config(page_title="DARKKAN PRO", page_icon="🎬")
st.title("🎬 DARKKAN: Versão Cinema Pro")

# --- CONFIGURAÇÃO DE VOZ ---
# Para evitar dependências externas e erros de permissão, usamos gTTS (Google).
# Se você tiver uma API ElevenLabs válida, pode reativar aqui.
ELEVENLABS_API_KEY = ""  # Não usado atualmente

def gerar_audio(texto, index):
    nome_arquivo = f"audio_{index}.mp3"
    try:
        gTTS(text=texto, lang="pt", tld="com.br").save(nome_arquivo)
    except Exception as e:
        st.error(f"Erro ao gerar áudio: {e}")
        st.text(traceback.format_exc())
        raise
    return nome_arquivo

# Import de vídeo movido para depois do setup inicial
from moviepy import ImageClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips

def gerar_imagem_ia(prompt_imagem, index):
    prompt_final = f"{prompt_imagem}, dark aesthetic, cinematic lighting, 8k, hyperrealistic"
    url = f"https://image.pollinations.ai/prompt/{prompt_final}?width=1080&height=1920&seed={index+500}&nologo=true"
    response = requests.get(url, timeout=30)
    nome_arquivo = f"cena_{index}.jpg"
    with open(nome_arquivo, "wb") as f:
        f.write(response.content)
    time.sleep(1)
    return nome_arquivo

# --- INTERFACE ---
tema = st.text_input("Qual o tema visual?", "Guerreiro medieval na penumbra")
roteiro = st.text_area("Roteiro (separe por pontos):", "A dor é temporária. O orgulho é para sempre.")

if st.button("🎬 GERAR FILME DARK"):
    for f in glob.glob("audio_*.mp3") + glob.glob("cena_*.jpg") + glob.glob("temp_*.*"):
        try: os.remove(f)
        except: pass

    with st.spinner("DARKKAN produzindo..."):
        try:
            frases = [f.strip() for f in roteiro.split('.') if len(f.strip()) > 5]
            clips = []
            for i, frase in enumerate(frases):
                audio_path = gerar_audio(frase, i)
                audio_clip = AudioFileClip(audio_path)
                img_path = gerar_imagem_ia(tema, i)
                
                # Efeito de movimento
                img_clip = ImageClip(img_path).set_duration(audio_clip.duration).resize(
                    lambda t: 1 + 0.04 * t
                )
                
                # Legendas
                txt_clip = TextClip(
                    text=frase.upper(), font_size=70, color='yellow',
                    method='caption', size=(int(img_clip.w*0.85), None),
                    stroke_color='black', stroke_width=3
                ).with_duration(audio_clip.duration).with_position('center')
                
                clips.append(CompositeVideoClip([img_clip, txt_clip]).with_audio(audio_clip))
            
            video_final = concatenate_videoclips(clips, method="compose")
            video_final.write_videofile("darkkan_final.mp4", fps=24, codec="libx264", audio_codec="aac")
            st.video("darkkan_final.mp4")
        except Exception as e:
            st.error(f"Erro: {e}")
            st.text(traceback.format_exc())
