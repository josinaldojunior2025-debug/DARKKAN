import imageio
import streamlit as st
import os
import requests
import glob
from gtts import gTTS
from elevenlabs.client import ElevenLabs # Adicionado para voz profissional
from moviepy import ImageClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips

st.set_page_config(page_title="DARKKAN CINEMA", page_icon="🎬")
st.title("🎬 DARKKAN: Versão Cinema Pro")

# --- CONFIGURAÇÃO DE VOZES (ELEVENLABS) ---
# Se não tiver a chave ainda, o código usará gTTS automaticamente
ELEVENLABS_API_KEY = "sk_4844b5dfdd3c0a5510a1d1a110c34267dc197b4232c2ce76" 
client = ElevenLabs(api_key=ELEVENLABS_API_KEY) if ELEVENLABS_API_KEY != "SUA_CHAVE_AQUI" else None

os.environ["IMAGEIO_VAR_NAME"] = "ffmpeg"

def gerar_imagem_ia(prompt_imagem, index):
    # Prompt aprimorado para estética Dark Cinematic
    prompt_final = f"{prompt_imagem}, dark aesthetic, cinematic lighting, 8k, hyperrealistic, dramatic shadows"
    url = f"https://image.pollinations.ai/prompt/{prompt_final}?width=1080&height=1920&seed={index+100}&nologo=true"
    response = requests.get(url, timeout=30)
    nome_arquivo = f"cena_{index}.jpg"
    with open(nome_arquivo, "wb") as f:
        f.write(response.content)
    return nome_arquivo

def gerar_audio(texto, index):
    nome_arquivo = f"audio_{index}.mp3"
    if client:
        # Voz Profissional (ElevenLabs)
        audio = client.generate(text=texto, voice="Adam", model="eleven_multilingual_v2")
        with open(nome_arquivo, "wb") as f:
            for chunk in audio: f.write(chunk)
    else:
        # Voz Padrão (gTTS)
        gTTS(text=texto, lang='pt', tld='com.br').save(nome_arquivo)
    return nome_arquivo

tema = st.text_input("Qual o tema visual?", "Guerreiro medieval na penumbra")
roteiro = st.text_area("Roteiro (separe por pontos):", "A dor é temporária. O orgulho é para sempre.")

if st.button("🎬 GERAR FILME DARK"):
    with st.spinner("Produzindo obra cinematográfica..."):
        try:
            frases = [f.strip() for f in roteiro.split('.') if len(f.strip()) > 5]
            clips = []
            
            for i, frase in enumerate(frases):
                audio_path = gerar_audio(frase, i)
                audio_clip = AudioFileClip(audio_path)
                
                img_path = gerar_imagem_ia(tema, i)
                # Adicionado um leve efeito de zoom (Ken Burns)
                img_clip = ImageClip(img_path).with_duration(audio_clip.duration).with_effects([
                    lambda clip: clip.resized(lambda t: 1 + 0.02 * t)
                ])
                
                # Legendas Estilo Viral (Maiores e Centralizadas)
                txt_clip = TextClip(
                    text=frase.upper(), font_size=70, color='yellow',
                    method='caption', size=(int(img_clip.w*0.9), None),
                    stroke_color='black', stroke_width=3, font="Arial-Bold"
                ).with_duration(audio_clip.duration).with_position('center')
                
                cena = CompositeVideoClip([img_clip, txt_clip]).with_audio(audio_clip)
                clips.append(cena)
            
            video_final = concatenate_videoclips(clips, method="compose")
            video_final.write_videofile("darkkan_pro.mp4", fps=24, codec="libx264", audio_codec="aac")
            
            st.video("darkkan_pro.mp4")
            
        except Exception as e:
            st.error(f"Erro: {e}")