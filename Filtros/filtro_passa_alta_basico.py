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

class HighPassFilter:
    def __init__(self, path: str):
        self.image = carregar_imagem_pgm(path)  # Carrega a imagem em tons de cinza
        self.filtered_image = None
        self.tk_image = None  # Adiciona o atributo para manter a imagem em memória

    def apply_filter(self):
        img_array = np.array(self.image, dtype=np.float32)

        # Definindo o kernel do filtro passa-alta (Laplaciano)
        kernel = np.array([[0, -1, 0],
                           [-1, 4, -1],
                           [0, -1, 0]], dtype=np.float32)

        # Aplicando convolução
        self.filtered_image = self.convolve(img_array, kernel)

        # Normalizar os resultados para visualização
        self.filtered_image = np.clip(self.filtered_image, 0, 255).astype(np.uint8)
        self.filtered_image = Image.fromarray(self.filtered_image)

    def convolve(self, img, kernel):
        # Obtém as dimensões da imagem e do kernel
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

        # Exibir a imagem original e a imagem filtrada
        plt.figure(figsize=(10, 5))

        # Imagem original
        plt.subplot(1, 2, 1)
        plt.title("Imagem Original")
        plt.imshow(self.image, cmap="gray")
        plt.axis("off")

        # Imagem filtrada
        plt.subplot(1, 2, 2)
        plt.title("Imagem com Filtro Passa-Alta")
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


