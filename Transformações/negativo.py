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

class Negativo:
    def __init__(self, path: str):
        """Inicializa a classe com a imagem a ser transformada em negativo."""
        self.image, self.maxval = carregar_imagem_pgm(path)
        self.negative_image = None

    def apply_negative(self):
        """Aplica a transformação de negativo à imagem."""
        negativo_array = self.maxval - self.image
        self.negative_image = Image.fromarray(negativo_array.astype(np.uint8))

    def show_images(self):
        """Mostra a imagem original e a imagem negativa."""
        if self.negative_image is None:
            print("Primeiro aplique o negativo usando o método `apply_negative`.")
            return

        # Configurações para mostrar as imagens lado a lado
        plt.figure(figsize=(10, 5))
        
        # Imagem original
        plt.subplot(1, 2, 1)
        plt.title("Imagem Original")
        plt.imshow(self.image, cmap="gray")
        plt.axis("off")
        
        # Imagem negativa
        plt.subplot(1, 2, 2)
        plt.title("Imagem Negativa")
        plt.imshow(self.negative_image, cmap="gray")
        plt.axis("off")
        
        plt.show()

    def get_ctk_image(self, width=None, height=None):
        """Converte a imagem negativa para CTkImage para uso no CustomTkinter."""
        if self.negative_image is None:
            raise ValueError("Primeiro aplique o negativo usando o método `apply_negative`.")
        
        # Converte a imagem para CTkImage e mantém em memória
        self.tk_image = ctk.CTkImage(self.negative_image, size=(width, height))
        return self.tk_image
