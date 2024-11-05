import numpy as np
from PIL import Image
import customtkinter as ctk

class Fechamento:
    def __init__(self, caminho):
        self.imagem = self.carregar_imagem_pgm(caminho)
        self.imagem_fechada = None  # Inicializa a variável para armazenar a imagem processada

    def carregar_imagem_pgm(self, caminho_imagem):
        """Carrega uma imagem PGM e retorna como um array numpy."""
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

    def dilatar(self, elemento_estruturante=np.ones((3, 3), dtype=np.uint8)):
        e_height, e_width = elemento_estruturante.shape
        padding_y, padding_x = e_height // 2, e_width // 2
        imagem_padded = np.pad(self.imagem, ((padding_y, padding_y), (padding_x, padding_x)), mode='constant', constant_values=0)
        imagem_dilatada = np.zeros_like(self.imagem)

        for i in range(padding_y, imagem_padded.shape[0] - padding_y):
            for j in range(padding_x, imagem_padded.shape[1] - padding_x):
                vizinhanca = imagem_padded[i - padding_y:i + padding_y + 1, j - padding_x:j + padding_x + 1]
                imagem_dilatada[i - padding_y, j - padding_x] = np.max(vizinhanca * elemento_estruturante)
        
        return imagem_dilatada

    def erodir(self, imagem, elemento_estruturante=np.ones((3, 3), dtype=np.uint8)):
        e_height, e_width = elemento_estruturante.shape
        padding_y, padding_x = e_height // 2, e_width // 2
        imagem_padded = np.pad(imagem, ((padding_y, padding_y), (padding_x, padding_x)), mode='constant', constant_values=255)
        imagem_erodida = np.zeros_like(imagem)

        for i in range(padding_y, imagem_padded.shape[0] - padding_y):
            for j in range(padding_x, imagem_padded.shape[1] - padding_x):
                vizinhanca = imagem_padded[i - padding_y:i + padding_y + 1, j - padding_x:j + padding_x + 1]
                imagem_erodida[i - padding_y, j - padding_x] = np.min(vizinhanca * elemento_estruturante)
        
        return imagem_erodida

    def fechamento(self, elemento_estruturante=np.ones((3, 3), dtype=np.uint8)):
        """Realiza a operação de fechamento (dilatação seguida de erosão) e armazena o resultado."""
        imagem_dilatada = self.dilatar(elemento_estruturante)
        self.imagem_fechada = self.erodir(imagem_dilatada, elemento_estruturante)

    def get_ctk_image(self, width=None, height=None):
        """Converte a imagem fechada para CTkImage para uso no CustomTkinter."""
        if self.imagem_fechada is None:
            raise ValueError("Primeiro aplique o fechamento usando o método `fechamento`.")
        
        imagem_fechada_pil = Image.fromarray(self.imagem_fechada)
        self.tk_image = ctk.CTkImage(imagem_fechada_pil, size=(width, height))
        return self.tk_image
