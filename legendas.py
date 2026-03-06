import whisper

def gerar_legendas_darkkan():
    print("🎧 DARKKAN está ouvindo o áudio para legendar...")
    model = whisper.load_model("base")
    
    # Transcreve o áudio gerado pelo Script Mestre
    result = model.transcribe("audio_mestre.mp3")
    
    # Salva no formato de legenda padrão
    with open("legendas.srt", "w", encoding="utf-8") as f:
        for i, segment in enumerate(result['segments']):
            start = segment['start']
            end = segment['end']
            text = segment['text'].strip()
            # Formatação simples de SRT
            f.write(f"{i+1}\n00:00:{int(start):02d},000 --> 00:00:{int(end):02d},000\n{text}\n\n")
            
    print("✅ Legendas geradas em 'legendas.srt'!")

if __name__ == "__main__":
    gerar_legendas_darkkan()