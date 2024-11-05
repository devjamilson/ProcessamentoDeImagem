import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import customtkinter as ctk

class TopHat:
    def __init__(self, caminho):
        """Inicializa a classe TopHat com a imagem a ser processada."""
        self.imagem = self.carregar_imagem_pgm(caminho)
        self.imagem_top_hat = None

    def carregar_imagem_pgm(self, caminho_imagem):
        """Carrega uma imagem PGM (P2 ou P5) e retorna como um array numpy."""
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
                imagem_data = []
                for line in f:
                    imagem_data.extend(map(int, line.split()))
                imagem = np.array(imagem_data, dtype=np.uint8).reshape((height, width))
            else:
                raise ValueError("Formato PGM não suportado (esperado P2 ou P5).")

        return imagem

    def aplicar_top_hat(self, elemento_estruturante=np.ones((3, 3), dtype=np.uint8)):
        """Aplica a operação Top-Hat usando o elemento estruturante especificado."""
        imagem_erodida = self.erodir(elemento_estruturante)
        imagem_dilatada = self.dilatar(self.imagem, elemento_estruturante)  # Passa self.imagem como parâmetro
        if imagem_erodida.shape == imagem_dilatada.shape:
            self.imagem_top_hat = imagem_erodida - imagem_dilatada
        else:
            raise ValueError("Erro: As dimensões de imagem_erodida e imagem_dilatada não coincidem.")
        return self.imagem_top_hat


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
        
        self.imagem_erodida = imagem_erodida  # Salva a imagem erodida internamente para uso posterior
        return self.imagem_erodida

    def dilatar(self, imagem, elemento_estruturante=np.ones((3, 3), dtype=np.uint8)):
        e_height, e_width = elemento_estruturante.shape
        padding_y, padding_x = e_height // 2, e_width // 2
        imagem_padded = np.pad(imagem, ((padding_y, padding_y), (padding_x, padding_x)), mode='constant', constant_values=0)
        imagem_dilatada = np.zeros_like(imagem)

        for i in range(padding_y, imagem_padded.shape[0] - padding_y):
            for j in range(padding_x, imagem_padded.shape[1] - padding_x):
                vizinhanca = imagem_padded[i - padding_y:i + padding_y + 1, j - padding_x:j + padding_x + 1]
                imagem_dilatada[i - padding_y, j - padding_x] = np.max(vizinhanca * elemento_estruturante)
        
        return imagem_dilatada


    def show_images(self):
        """Mostra a imagem original e a imagem Top-Hat lado a lado."""
        if self.imagem_top_hat is None:
            print("Primeiro aplique a operação Top-Hat usando o método `aplicar_top_hat`.")
            return

        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.title("Imagem Original")
        plt.imshow(self.imagem, cmap="gray")
        plt.axis("off")

        plt.subplot(1, 2, 2)
        plt.title("Imagem Top-Hat")
        plt.imshow(self.imagem_top_hat, cmap="gray")
        plt.axis("off")
        plt.show()

    def get_ctk_image(self, width=None, height=None):
        """Converte a imagem Top-Hat para CTkImage para uso no CustomTkinter."""
        if self.imagem_top_hat is None:
            raise ValueError("Primeiro aplique a operação Top-Hat usando o método `aplicar_top_hat`.")
        
        imagem_top_hat_pil = Image.fromarray(self.imagem_top_hat)
        return ctk.CTkImage(imagem_top_hat_pil, size=(width, height))
