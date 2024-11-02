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

class Sigmoide:
    def __init__(self, path: str):
        """Inicializa a classe com a imagem a ser transformada."""
        self.image, self.maxval = carregar_imagem_pgm(path)
        self.transformed_image = None

    def apply_sigmoide(self, w: float, sigma: float):
        """Aplica a função de transferência de intensidade geral à imagem."""
        # Normaliza os valores da imagem para o intervalo [0, 255]
        imagem_normalizada = self.image.astype(np.float64)
        
        # Aplica a função de transferência de intensidade: S(r) = 255 / (1 + e^(-(r - w) / sigma))
        imagem_transformada = 255 / (1 + np.exp(-(imagem_normalizada - w) / sigma))
        
        # Converte o resultado para o intervalo [0, 255] e para uint8
        self.transformed_image = np.clip(imagem_transformada, 0, 255).astype(np.uint8)

    def show_imagens(self):
        """Mostra a imagem original e a imagem transformada de intensidade geral."""
        if self.transformed_image is None:
            print("Primeiro aplique a transformação usando o método `aplicar_transformacao_intensidade`.")
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
        plt.title("Imagem com Intensidade Geral")
        plt.imshow(self.transformed_image, cmap="gray")
        plt.axis("off")
        
        plt.show()

    def get_ctk_image(self, width=None, height=None):
        """Converte a imagem transformada para CTkImage para uso no CustomTkinter."""
        if self.transformed_image is None:
            raise ValueError("Primeiro aplique a transformação usando o método `aplicar_transformacao_intensidade`.")
        
        # Converte a imagem para CTkImage e mantém em memória
        self.tk_image = ctk.CTkImage(Image.fromarray(self.transformed_image), size=(width, height))
        return self.tk_image
