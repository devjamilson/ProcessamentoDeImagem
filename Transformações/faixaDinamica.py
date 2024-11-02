import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import customtkinter as ctk

class FaixaDinamica:
    def __init__(self, caminho):
        """Inicializa a classe com o caminho da imagem e carrega a imagem PGM."""
        self.imagem, self.maxval = self.carregar_imagem_pgm(caminho)
        self.imagem_transformada = None
        
    def carregar_imagem_pgm(self, caminho_imagem):
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
    
    def transformar_faixa_dinamica(self):
        """Aplica a transformação de faixa dinâmica à imagem para ajustar os valores ao intervalo [0, 255]."""
        min_val = self.imagem.min()
        max_val = self.imagem.max()
        
        # Ajusta a faixa dinâmica
        imagem_transformada = (self.imagem - min_val) * 255.0 / (max_val - min_val)
        
        # Converte o resultado para uint8
        self.imagem_transformada = np.clip(imagem_transformada, 0, 255).astype(np.uint8)
        
    def show_images(self):
        """Mostra a imagem original e a imagem transformada."""
        if self.imagem_transformada is None:
            print("Primeiro aplique a transformação de faixa dinâmica.")
            return
        
        # Configurações para mostrar as imagens lado a lado
        plt.figure(figsize=(10, 5))
        
        # Imagem original
        plt.subplot(1, 2, 1)
        plt.title("Imagem Original")
        plt.imshow(self.imagem, cmap="gray")
        plt.axis("off")
        
        # Imagem transformada
        plt.subplot(1, 2, 2)
        plt.title("Imagem Transformada")
        plt.imshow(self.imagem_transformada, cmap="gray")
        plt.axis("off")
        
        plt.show()

    def get_ctk_image(self, width=None, height=None):
        """Converte a imagem transformada para CTkImage para uso no CustomTkinter."""
        if self.imagem_transformada is None:
            raise ValueError("Primeiro aplique a transformação de faixa dinâmica.")
        
        # Converte a imagem transformada para CTkImage e mantém em memória
        self.tk_image = ctk.CTkImage(Image.fromarray(self.imagem_transformada), size=(width, height))
        return self.tk_image
