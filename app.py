import gradio as gr
import os
import shutil
import subprocess
import json
import re
from extractor import extrair_texto_pdf, criar_prompt, sanitize_llm_response

def processar_pdf(pdf):
    # Garante que o diretório de uploads exista
    os.makedirs("uploads", exist_ok=True)

    # Copia o arquivo do caminho temporário do Gradio
    caminho_destino = os.path.join("uploads", os.path.basename(pdf))
    shutil.copy(pdf, caminho_destino)

    # Extrai texto do PDF
    texto = extrair_texto_pdf(caminho_destino)

    # Gera o prompt a partir do template
    prompt = criar_prompt(texto)

    # Chama o modelo LLM local via Ollama
    resultado = subprocess.run(
        ["ollama", "run", "deepseek-r1:8b"],
        input=prompt.encode("utf-8"),
        stdout=subprocess.PIPE
    )

    resposta = resultado.stdout.decode()
    print("\n\n--- RESPOSTA DA LLM ---\n")
    print(resposta)
    print("\n-----------------------\n")

    # Tenta interpretar o resultado como JSON
    try:
        # Primeiro tenta usar a função de sanitização
        json_puro = sanitize_llm_response(resposta)
        
        if json_puro:
            data = json.loads(json_puro)
            return data
            
        # Se a sanitização não funcionar, tenta o método anterior de extração
        inicio = resposta.find("[")
        fim = resposta.rfind("]") + 1
        
        # Verifica se encontramos colchetes JSON válidos
        if inicio != -1 and fim > inicio:
            json_puro = resposta[inicio:fim]
            
            # Limpa potenciais problemas de formatação na string JSON
            json_puro = re.sub(r',\s+', ', ', json_puro)
            
            try:
                data = json.loads(json_puro)
                return data
            except json.JSONDecodeError:
                # Se a extração direta falhar, tenta uma limpeza mais agressiva
                json_puro = re.sub(r'(?<=\{)[^{}]*(?=\})', 
                                  lambda m: m.group(0).replace('\n', ' ').replace('  ', ' '), 
                                  json_puro)
                data = json.loads(json_puro)
                return data
        else:
            # Se nenhum array JSON for encontrado, retorna mensagem de erro
            return {"error": "Não foi possível encontrar um formato JSON na resposta da LLM. Verifique o prompt e tente novamente."}
    except Exception as e:
        # Retorna informações detalhadas do erro
        return {
            "error": f"Erro ao interpretar JSON: {str(e)}",
            "resposta_parcial": resposta[:500] + "..." if len(resposta) > 500 else resposta,
            "sugestao": "Tente ajustar o prompt para forçar a resposta em formato JSON válido."
        }

# Interface do Gradio
iface = gr.Interface(
    fn=processar_pdf,
    inputs=gr.File(label="Envie o laudo em PDF", file_types=[".pdf"]),
    outputs=gr.JSON(label="Resultados extraídos"),
    title="📄 Leitor de Exames com LLM Local",
    description="Envie um PDF de exame laboratorial e veja os resultados extraídos por uma LLM local (DeepSeek via Ollama)."
)

# Lançamento do app local
if __name__ == "__main__":
    iface.launch()