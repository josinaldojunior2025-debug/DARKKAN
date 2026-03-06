from google import genai

# Sua chave configurada
CHAVE_API = "AIzaSyBeeZaw7WDjms1BOh88eXCD097AyhUXQz4"

def criar_roteiro_darkkan(tema):
    print(f"🧠 DARKKAN acessando novo motor de IA para: {tema}...")
    
    try:
        # Nova forma de conectar à IA do Google
        client = genai.Client(api_key=CHAVE_API)
        
        prompt = (
            f"Escreva uma narração curta e impactante para um vídeo de canal Dark sobre {tema}. "
            "Use frases curtas, tom misterioso e profundo. Vá direto ao ponto."
        )
        
        # Gerando o conteúdo com o modelo mais atual
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )
        
        texto_final = response.text
        
        with open("roteiro_final.txt", "w", encoding="utf-8") as f:
            f.write(texto_final)
            
        print("✅ SUCESSO ABSOLUTO! Roteiro gerado.")
        print("-" * 30)
        print(texto_final)
        print("-" * 30)
        
    except Exception as e:
        print(f"❌ Erro no novo motor: {e}")

if __name__ == "__main__":
    tema_escolhido = "O poder da disciplina inabalável"
    criar_roteiro_darkkan(tema_escolhido)