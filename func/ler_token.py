# -= ler o token
def ler_token(caminho_arquivo):
    with open(caminho_arquivo, 'r') as f:
        return f.read().strip()