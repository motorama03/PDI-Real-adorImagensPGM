import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def aplicar_transferencia_linear(imagem, a, b):
    """
    Aplica uma função de transferência linear s = a*r + b na imagem.
    """
    array_imagem = np.array(imagem)
    transformada = np.clip(a * array_imagem + b, 0, 255).astype(np.uint8)  # Garantir valores válidos
    return Image.fromarray(transformada)

# Abrir uma imagem PGM (tons de cinza)
imagem_pgm = Image.open("/home/matias/Documentos/BCC2024-2/PDI/converteBinario/Entrada.pgm").convert("L")

# Aplicar transformação linear (exemplo: aumentar contraste)
a, b = 1.2, 10  # Parâmetros da função
imagem_transformada = aplicar_transferencia_linear(imagem_pgm, a, b)

# Exibir imagem original, transformada e histogramas
plt.figure(figsize=(12, 6))
plt.subplot(2, 2, 1)
plt.title("Imagem Original")
plt.imshow(imagem_pgm, cmap="gray")

plt.subplot(2, 2, 2)
plt.title("Imagem Transformada")
plt.imshow(imagem_transformada, cmap="gray")

plt.subplot(2, 2, 3)
plt.title("Histograma Original")
plt.hist(np.array(imagem_pgm).ravel(), bins=256, range=(0, 255), color="gray")

plt.subplot(2, 2, 4)
plt.title("Histograma Transformado")
plt.hist(np.array(imagem_transformada).ravel(), bins=256, range=(0, 255), color="gray")

plt.tight_layout()
plt.show()
