import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import customtkinter as ctk

class HitOrMiss:
    def __init__(self, caminho):
        """Inicializa a classe HitOrMiss com a imagem a ser processada."""
        self.imagem = self.carregar_imagem_pgm(caminho)  # Carrega a imagem em tons de cinza
        self.imagem_hit_or_miss = None  # Imagem com a operação Hit-or-Miss aplicada

    def carregar_imagem_pgm(self, caminho_imagem):
        """Carrega uma imagem PGM (P2 ou P5) e retorna como um array numpy."""
        if not os.path.exists(caminho_imagem):
            raise FileNotFoundError(f"O arquivo não foi encontrado: {caminho_imagem}")

        with open(caminho_imagem, 'rb') as f:
            header = f.readline().strip()
            
            # Verifica o formato (P2 para ASCII, P5 para binário)
            if header == b'P5':
                width, height = map(int, f.readline().split())
                maxval = int(f.readline().strip())
                imagem_data = np.fromfile(f, dtype=np.uint8 if maxval < 256 else np.uint16)
                imagem = imagem_data.reshape((height, width))
            
            elif header == b'P2':
                width, height = map(int, f.readline().split())
                maxval = int(f.readline().strip())
                imagem_data = []
                for line in f:
                    imagem_data.extend(map(int, line.split()))
                imagem = np.array(imagem_data, dtype=np.uint8).reshape((height, width))
            
            else:
                raise ValueError("Formato PGM não suportado (esperado P2 ou P5).")

        return imagem

    def erodir(self, elemento_estruturante=np.ones((3, 3), dtype=np.uint8)):
        """
        Aplica a erosão morfológica usando o elemento estruturante especificado.
        
        :param elemento_estruturante: Um array numpy representando o elemento estruturante (kernel) de erosão.
        :return: Imagem erodida.
        """
        e_height, e_width = elemento_estruturante.shape
        padding_y, padding_x = e_height // 2, e_width // 2
        imagem_padded = np.pad(self.imagem, ((padding_y, padding_y), (padding_x, padding_x)), mode='constant', constant_values=255)
        imagem_erodida = np.zeros_like(self.imagem)
        
        for i in range(padding_y, imagem_padded.shape[0] - padding_y):
            for j in range(padding_x, imagem_padded.shape[1] - padding_x):
                vizinhanca = imagem_padded[i - padding_y:i + padding_y + 1, j - padding_x:j + padding_x + 1]
                imagem_erodida[i - padding_y, j - padding_x] = np.min(vizinhanca * elemento_estruturante)
        
        return imagem_erodida

    def hit_or_miss(self, elemento_estruturante):
        """
        Aplica a operação Hit-or-Miss usando o elemento estruturante especificado.
        
        :param elemento_estruturante: Um array numpy representando o elemento estruturante.
        :return: Resultado da operação Hit-or-Miss.
        """
        # Define o complemento do elemento estruturante
        complemento = np.ones_like(elemento_estruturante) - elemento_estruturante

        # Erosão do elemento estruturante
        imagem_erodida = self.erodir(elemento_estruturante)
        # Erosão do complemento do elemento estruturante
        imagem_complemento_erodido = self.erodir(complemento)

        # A operação Hit-or-Miss é a interseção das duas erosiões
        hit_or_miss_result = np.where((imagem_erodida == np.min(elemento_estruturante)) & (imagem_complemento_erodido == 255), 255, 0)

        self.imagem_hit_or_miss = hit_or_miss_result  # Salva a imagem resultante internamente para uso posterior
        return self.imagem_hit_or_miss

    def show_images(self):
        """Mostra a imagem original e a imagem com Hit-or-Miss aplicada lado a lado."""
        if self.imagem_hit_or_miss is None:
            print("Primeiro aplique a operação Hit-or-Miss usando o método `hit_or_miss`.") 
            return
        
        # Configurações para mostrar as imagens lado a lado
        plt.figure(figsize=(10, 5))
        
        # Imagem original
        plt.subplot(1, 2, 1)
        plt.title("Imagem Original")
        plt.imshow(self.imagem, cmap="gray")
        plt.axis("off")
        
        # Imagem com Hit-or-Miss aplicada
        plt.subplot(1, 2, 2)
        plt.title("Imagem com Hit-or-Miss")
        plt.imshow(self.imagem_hit_or_miss, cmap="gray")
        plt.axis("off")
        
        plt.show()

    def get_ctk_image(self, width=None, height=None):
        """Converte a imagem resultante de Hit-or-Miss para CTkImage para uso no CustomTkinter."""
        if self.imagem_hit_or_miss is None:
            raise ValueError("Primeiro aplique a operação Hit-or-Miss usando o método `hit_or_miss`.")
        
        # Converte a imagem resultante para PIL e então para CTkImage
        imagem_hit_or_miss_pil = Image.fromarray(self.imagem_hit_or_miss)
        self.tk_image = ctk.CTkImage(imagem_hit_or_miss_pil, size=(width, height))
        return self.tk_image
