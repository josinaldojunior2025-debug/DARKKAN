import streamlit as st
import os
import requests
import imageio
from gtts import gTTS
from moviepy import ImageClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips

st.set_page_config(page_title="DARKKAN 2.0 - Escala", page_icon="🔥")
st.title("🔥 DARKKAN 2.0: Múltiplas Cenas & IA")

# Configurações de Ambiente
os.environ["IMAGEIO_VAR_NAME"] = "ffmpeg"

def gerar_imagem_ia(prompt_imagem, index):
    print(f"🎨 Gerando imagem para a cena {index}...")
    url = f"https://image.pollinations.ai/prompt/{prompt_imagem}?width=1080&height=1920&seed={index}&nologo=true"
    response = requests.get(url)
    nome_arquivo = f"cena_{index}.jpg"
    with open(nome_arquivo, "wb") as f:
        f.write(response.content)
    return nome_arquivo

tema = st.text_input("Tema do Vídeo (para a IA se inspirar):", "Guerreiro estoico no escuro")
roteiro_completo = st.text_area("Roteiro (separe as frases por ponto final):", 
                               "O silêncio é sua maior arma. A disciplina molda o seu destino. O DARKKAN nunca para.")

if st.button("🚀 GERAR VÍDEO PROFISSIONAL"):
    with st.spinner("DARKKAN está criando arte e vídeo..."):
        try:
            frases = [f.strip() for f in roteiro_completo.split('.') if len(f.strip()) > 5]
            clips_de_video = []
            
            for i, frase in enumerate(frases):
                # 1. Áudio da frase
                audio_path = f"audio_{i}.mp3"
                gTTS(text=frase, lang='pt', tld='com.br').save(audio_path)
                audio_clip = AudioFileClip(audio_path)
                
                # 2. Imagem da frase via IA
                img_path = gerar_imagem_ia(f"{tema}, cinematic, dark, hyperrealistic", i)
                
                # 3. Criar Clip da Cena
                img_clip = ImageClip(img_path).with_duration(audio_clip.duration)
                txt_clip = TextClip(
                    text=frase, font_size=60, color='yellow', stroke_color='black', stroke_width=2,
                    method='caption', size=(int(img_clip.w*0.8), None)
                ).with_duration(audio_clip.duration).with_position('center')
                
                cena = CompositeVideoClip([img_clip, txt_clip]).with_audio(audio_clip)
                clips_de_video.append(cena)
            
            # 4. Unir todas as cenas
            print("🎬 Unindo cenas...")
            video_final = concatenate_videoclips(clips_de_video, method="compose")
            video_final.write_videofile("darkkan_final.mp4", fps=24, codec="libx264")
            
            st.video("darkkan_final.mp4")
            with open("darkkan_final.mp4", "rb") as f:
                st.download_button("📥 Baixar Vídeo Viral", f, "darkkan_viral.mp4")
                
        except Exception as e:
            st.error(f"Erro na produção: {e}")