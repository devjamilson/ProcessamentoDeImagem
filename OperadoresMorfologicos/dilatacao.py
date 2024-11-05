import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import customtkinter as ctk

def carregar_imagem_pgm(caminho_imagem):
    """Carrega uma imagem PGM de um arquivo especificado."""
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

class Dilatacao:
    def __init__(self, path: str, kernel_size: int = 3):
        """Inicializa a classe DilationFilter com a imagem a ser dilatada e o tamanho do kernel."""
        self.image = carregar_imagem_pgm(path)  # Carrega a imagem em tons de cinza
        self.kernel_size = kernel_size
        self.filtered_image = None
        self.elemento_estruturante = np.ones((self.kernel_size, self.kernel_size), dtype=np.uint8)  # Kernel de dilatação padrão

    def apply_filter(self):
        """Aplica a dilatação morfológica na imagem."""
        img_array = np.array(self.image)
        padded_img = np.pad(img_array, self.kernel_size // 2, mode='constant', constant_values=0)
        output_array = np.zeros_like(img_array)
        
        # Aplica a dilatação
        for i in range(img_array.shape[0]):
            for j in range(img_array.shape[1]):
                # Extrai a vizinhança e aplica o elemento estruturante
                region = padded_img[i:i + self.kernel_size, j:j + self.kernel_size]
                output_array[i, j] = np.max(region * self.elemento_estruturante)
        
        self.filtered_image = Image.fromarray(output_array.astype(np.uint8))

    def show_images(self):
        """Mostra a imagem original e a imagem dilatada."""
        if self.filtered_image is None:
            print("Primeiro aplique o filtro usando o método `apply_filter`.")
            return
        
        # Configurações para mostrar as imagens lado a lado
        plt.figure(figsize=(10, 5))
        
        # Imagem original
        plt.subplot(1, 2, 1)
        plt.title("Imagem Original")
        plt.imshow(self.image, cmap="gray")
        plt.axis("off")
        
        # Imagem com dilatação aplicada
        plt.subplot(1, 2, 2)
        plt.title("Imagem com Dilatação")
        plt.imshow(self.filtered_image, cmap="gray")
        plt.axis("off")
        
        plt.show()

    def get_ctk_image(self, width=None, height=None):
        """Converte a imagem dilatada para CTkImage para uso no CustomTkinter."""
        if self.filtered_image is None:
            raise ValueError("Primeiro aplique o filtro usando o método `apply_filter`.")
        
        # Converte a imagem para CTkImage e mantém em memória
        self.tk_image = ctk.CTkImage(self.filtered_image, size=(width, height))
        return self.tk_image
