import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Função para aplicar a transferência linear (s = a*r + b)
def aplicar_transferencia_linear(imagem, a, b):
    """
    Aplica uma função de transferência linear s = a*r + b em uma imagem.
    """
    array_imagem = np.array(imagem)
    transformada = np.clip(a * array_imagem + b, 0, 255).astype(np.uint8)  # Garante valores entre 0 e 255
    return Image.fromarray(transformada)

# Função para gerar histogramas de cada canal
def gerar_histogramas(imagem, titulo="Histograma"):
    """
    Gera histogramas para cada canal de cor (RGB ou escala de cinza).
    """
    array_imagem = np.array(imagem)
    
    plt.figure(figsize=(12, 6))
    
    if len(array_imagem.shape) == 2:  # Escala de cinza
        plt.title(f"{titulo} - Escala de Cinza")
        plt.hist(array_imagem.ravel(), bins=256, range=(0, 255), color="gray")
        plt.xlabel("Intensidade")
        plt.ylabel("Frequência")
    else:  # RGB
        cores = ["Red", "Green", "Blue"]
        for i, cor in enumerate(cores):
            plt.subplot(1, 3, i + 1)
            plt.title(f"{titulo} - {cor}")
            plt.hist(array_imagem[:, :, i].ravel(), bins=256, range=(0, 255), color=cor.lower())
            plt.xlabel("Intensidade")
            plt.ylabel("Frequência")
    
    plt.tight_layout()
    plt.show()

# Função principal para processar PGM e PPM
def processar_imagens(caminho_imagem, a, b, tipo="PPM"):
    """
    Processa a imagem PGM ou PPM aplicando a função de transferência linear.
    """
    imagem = Image.open(caminho_imagem)
    imagem_original = imagem.copy()  # Para comparação posterior
    
    if tipo == "PGM":  # Tons de cinza
        imagem = imagem.convert("L") 
        imagem_transformada = aplicar_transferencia_linear(imagem, a, b)
    elif tipo == "PPM":  # Imagem colorida (RGB)
        imagem = imagem.convert("RGB")
        canais = [aplicar_transferencia_linear(imagem.getchannel(c), a, b) for c in range(3)]
        imagem_transformada = Image.merge("RGB", canais)
    else:
        raise ValueError("Tipo de imagem inválido. Escolha 'PGM' ou 'PPM'.")
    
    # Exibir imagens e histogramas
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.title("Imagem Original")
    plt.imshow(imagem_original, cmap="gray" if tipo == "PGM" else None)
    
    plt.subplot(1, 2, 2)
    plt.title("Imagem Transformada")
    plt.imshow(imagem_transformada, cmap="gray" if tipo == "PGM" else None)
    plt.show()

    # Gerar histogramas
    gerar_histogramas(imagem_original, titulo="Original")
    gerar_histogramas(imagem_transformada, titulo="Transformada")
    
    return imagem_transformada

# Caminhos dos arquivos de entrada
caminho_ppm = "/home/matias/Documentos/BCC2024-2/PDI/converteBinario/Fig1.ppm" 

# Parâmetros da função de transferência
a = 1.2  # Fator de escala (contraste)
b = 10   # Ajuste de brilho

# Processar PPM (RGB)
imagem_transformada_ppm = processar_imagens(caminho_ppm, a, b, tipo="PPM")
