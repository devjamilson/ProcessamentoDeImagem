import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import customtkinter as ctk

def carregar_imagem_pgm(caminho_imagem):
    """Carrega uma imagem PGM (P2 ou P5) e retorna como um array numpy e o valor máximo de intensidade."""
    if not os.path.exists(caminho_imagem):
        raise FileNotFoundError(f"O arquivo não foi encontrado: {caminho_imagem}")

    with open(caminho_imagem, 'rb') as f:
        header = f.readline().strip()
        
        if header == b'P5':
            width, height = map(int, f.readline().split())
            maxval = int(f.readline().strip())
            imagem_data = np.fromfile(f, dtype=np.uint8 if maxval < 256 else np.uint16)
            imagem = imagem_data.reshape((height, width))
        
        elif header == b'P2':
            width, height = map(int, f.readline().split())
            maxval = int(f.readline().strip())
            imagem_data = [int(i) for line in f for i in line.split()]
            imagem = np.array(imagem_data, dtype=np.uint8).reshape((height, width))
        
        else:
            raise ValueError("Formato PGM não suportado (esperado P2 ou P5).")
    
    return imagem, maxval

class LinearTransfer:
    def __init__(self, path: str):
        """Inicializa a classe com a imagem a ser transformada linearmente."""
        self.image, self.maxval = carregar_imagem_pgm(path)
        self.transformed_image = None

    def apply_linear_transfer(self, a: float, b: float):
        """Aplica a transformação linear à imagem."""
        # Normaliza os valores da imagem para o intervalo [0, 1]
        imagem_normalizada = self.image / 255.0
        
        # Aplica a transformação linear: S = a * R + b
        imagem_transformada = a * imagem_normalizada + b
        
        # Reescala de volta para o intervalo [0, 255]
        imagem_transformada = np.clip(imagem_transformada * 255, 0, 255).astype(np.uint8)
        
        self.transformed_image = Image.fromarray(imagem_transformada)

    def Show_imagens(self):
        """Mostra a imagem original e a imagem transformada linearmente."""
        if self.transformed_image is None:
            print("Primeiro aplique a transformação usando o método `apply_linear_transfer`.")
            return

        # Configurações para mostrar as imagens lado a lado
        plt.figure(figsize=(10, 5))
        
        # Imagem original
        plt.subplot(1, 2, 1)
        plt.title("Imagem Original")
        plt.imshow(self.image, cmap="gray")
        plt.axis("off")
        
        # Imagem transformada
        plt.subplot(1, 2, 2)
        plt.title("Imagem Linear")
        plt.imshow(self.transformed_image, cmap="gray")
        plt.axis("off")
        
        plt.show()

    def get_ctk_image(self, width=None, height=None):
        """Converte a imagem transformada para CTkImage para uso no CustomTkinter."""
        if self.transformed_image is None:
            raise ValueError("Primeiro aplique a transformação usando o método `apply_linear_transfer`.")
        
        # Converte a imagem para CTkImage e mantém em memória
        self.tk_image = ctk.CTkImage(self.transformed_image, size=(width, height))
        return self.tk_image
