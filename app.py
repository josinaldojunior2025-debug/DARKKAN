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

# --- CONFIGURAÇÃO DE VOZ (TENTATIVA DINÂMICA) ---
ELEVENLABS_API_KEY = "sk_4844b5dfdd3c0a5510a1d1a110c34267dc197b4232c2ce76"

def gerar_audio(texto, index):
    nome_arquivo = f"audio_{index}.mp3"
    try:
        # Usa o cliente oficial ElevenLabs (API atual)
        from elevenlabs import ElevenLabs
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

        audio_stream = client.text_to_speech.convert(
            voice_id="pNInz6OBmcS5meDq9Dmd",  # Voz 'Adam'
            text=texto,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )
        with open(nome_arquivo, "wb") as f:
            for chunk in audio_stream:
                f.write(chunk)
    except Exception as e:
        # Fallback para gTTS se ElevenLabs não estiver disponível ou ocorrer erro
        st.warning(f"Usando voz reserva na cena {index}")
        st.text(f"[debug] ElevenLabs error: {e}")
        st.text(traceback.format_exc())
        gTTS(text=texto, lang="pt", tld="com.br").save(nome_arquivo)
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
                img_clip = ImageClip(img_path).with_duration(audio_clip.duration).with_effects([
                    lambda clip: clip.resized(lambda t: 1 + 0.04 * t)
                ])
                
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
