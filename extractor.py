import pdfplumber

def extrair_texto_pdf(caminho_pdf):
    texto_total = []
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if texto:
                texto_total.append(texto.strip())
    return "\n\n".join(texto_total)

def criar_prompt(texto_pdf):
    with open("llm_config/prompt.txt", "r", encoding="utf-8") as f:
        prompt = f.read()
    return prompt.replace("{{TEXTO_PDF}}", texto_pdf)

def sanitize_llm_response(resposta):
    """
    Sanitize LLM response to extract only valid JSON content.
    """
    # Find array pattern
    import re
    
    # Try to find a JSON array pattern
    array_match = re.search(r'\[\s*\{.+?\}\s*\]', resposta, re.DOTALL)
    if array_match:
        return array_match.group(0)
    
    # If no array pattern found, look for individual objects
    objects_match = re.search(r'\{\s*".+?"\s*:.+?\}', resposta, re.DOTALL)
    if objects_match:
        return '[' + objects_match.group(0) + ']'
    
    return None