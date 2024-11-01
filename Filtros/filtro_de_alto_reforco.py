from PIL import Image
import numpy as np
import os
import matplotlib.pyplot as plt
import customtkinter as ctk

def carregar_imagem_pgm(caminho_imagem):
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

class HighBoostFilter:
    def __init__(self, path: str, kernel_size: int = 3, k: float = 1.5):
        self.image = carregar_imagem_pgm(path)
        self.kernel_size = kernel_size
        self.k = k
        self.filtered_image = None
        self.tk_image = None  # Atributo para manter a imagem em memória para CustomTkinter

    def apply_filter(self):
        img_array = np.array(self.image, dtype=np.float32)

        # Passo 1: Aplicar filtro de média para suavização
        smoothed_array = self.convolve(img_array, np.ones((self.kernel_size, self.kernel_size)) / (self.kernel_size ** 2))

        # Passo 2: Calcular o realce
        mask = img_array - smoothed_array
        high_boost_array = img_array + self.k * mask

        # Limitar valores entre 0 e 255 para visualização correta
        high_boost_array = np.clip(high_boost_array, 0, 255)
        
        # Converter o array para uma imagem
        self.filtered_image = Image.fromarray(high_boost_array.astype(np.uint8))

    def convolve(self, img, kernel):
        """Aplica a convolução do kernel na imagem fornecida."""
        img_height, img_width = img.shape
        kernel_size = kernel.shape[0]
        pad_width = kernel_size // 2

        # Padding da imagem
        padded_img = np.pad(img, pad_width, mode='edge')
        output = np.zeros_like(img)

        # Convolução manual
        for i in range(img_height):
            for j in range(img_width):
                region = padded_img[i:i + kernel_size, j:j + kernel_size]
                output[i, j] = np.sum(region * kernel)

        return output

    def show_images(self):
        if self.filtered_image is None:
            print("Primeiro aplique o filtro usando o método `apply_filter`.")
            return

        # Exibir a imagem original e a imagem com filtro de alto reforço aplicado
        plt.figure(figsize=(10, 5))

        # Imagem original
        plt.subplot(1, 2, 1)
        plt.title("Imagem Original")
        plt.imshow(self.image, cmap="gray")
        plt.axis("off")

        # Imagem com filtro de alto reforço aplicado
        plt.subplot(1, 2, 2)
        plt.title("Imagem com Filtro de Alto Reforço")
        plt.imshow(self.filtered_image, cmap="gray")
        plt.axis("off")

        plt.show()

    def get_ctk_image(self, width=None, height=None):
        """Converte a imagem filtrada para CTkImage para uso no CustomTkinter."""
        if self.filtered_image is None:
            raise ValueError("Primeiro aplique o filtro usando o método `apply_filter`.")

        # Converte a imagem para CTkImage e mantém em memória
        self.tk_image = ctk.CTkImage(self.filtered_image, size=(width, height))
        return self.tk_image
