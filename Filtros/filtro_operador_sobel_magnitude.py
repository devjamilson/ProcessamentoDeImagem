from PIL import Image
import numpy as np
import os
import matplotlib.pyplot as plt
import customtkinter as ctk  # Certifique-se de que o CustomTkinter está instalado

def carregar_imagem_pgm(caminho_imagem):
    """Carrega uma imagem no formato PGM e a retorna como um array numpy."""
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

class SobelMagFilter:
    def __init__(self, path: str):
        self.image = carregar_imagem_pgm(path)  # Carrega a imagem em tons de cinza
        self.filtered_image_x = None
        self.filtered_image_y = None
        self.magnitude_image = None

    def apply_filter(self):
        """Aplica o filtro de Sobel na imagem carregada."""
        img_array = np.array(self.image, dtype=np.float32)

        # Definindo os kernels de Sobel
        Gx = np.array([[1, 2, 1],
                       [0, 0, 0],
                       [-1, -2, -1]], dtype=np.float32)
        
        Gy = np.array([[-1, 0, 1],
                       [-2, 0, 2],
                       [-1, 0, 1]], dtype=np.float32)
        
        # Aplicando convolução para detectar bordas
        self.filtered_image_x = self.convolve(img_array, Gx)
        self.filtered_image_y = self.convolve(img_array, Gy)

        # Normalizar os resultados para visualização
        self.filtered_image_x = np.clip(self.filtered_image_x, 0, 255).astype(np.uint8)
        self.filtered_image_y = np.clip(self.filtered_image_y, 0, 255).astype(np.uint8)

    def apply_magnitude(self):
        """
        Calcula a magnitude do gradiente combinando os resultados de Gx e Gy.
        """
        if self.filtered_image_x is None or self.filtered_image_y is None:
            raise ValueError("Os gradientes Gx e Gy ainda não foram calculados. Use `apply_filter` primeiro.")

        # Calculando a magnitude do gradiente
        magnitude = np.sqrt(self.filtered_image_x.astype(np.float32)**2 + 
                            self.filtered_image_y.astype(np.float32)**2)
        
        # Normalizar e armazenar a imagem de magnitude
        self.magnitude_image = np.clip(magnitude, 0, 255).astype(np.uint8)

    def convolve(self, img, kernel):
        """Aplica a convolução manualmente na imagem com um kernel especificado."""
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
        """Exibe a imagem original, as imagens filtradas e a magnitude."""
        if self.filtered_image_x is None or self.filtered_image_y is None or self.magnitude_image is None:
            print("Primeiro aplique o filtro e a magnitude usando os métodos `apply_filter` e `apply_magnitude`.")
            return

        plt.figure(figsize=(20, 5))

        # Imagem original
        plt.subplot(1, 4, 1)
        plt.title("Imagem Original")
        plt.imshow(self.image, cmap="gray")
        plt.axis("off")

        # Imagem filtrada em X
        plt.subplot(1, 4, 2)
        plt.title("Filtro de Sobel - Direção X")
        plt.imshow(self.filtered_image_x, cmap="gray")
        plt.axis("off")

        # Imagem filtrada em Y
        plt.subplot(1, 4, 3)
        plt.title("Filtro de Sobel - Direção Y")
        plt.imshow(self.filtered_image_y, cmap="gray")
        plt.axis("off")

        # Imagem de magnitude
        plt.subplot(1, 4, 4)
        plt.title("Magnitude do Gradiente")
        plt.imshow(self.magnitude_image, cmap="gray")
        plt.axis("off")

        plt.show()

    def get_ctk_images(self, width=None, height=None):
        """Converte as imagens filtradas e de magnitude para CTkImage para uso no CustomTkinter."""
        if self.filtered_image_x is None or self.filtered_image_y is None or self.magnitude_image is None:
            raise ValueError("Primeiro aplique o filtro e a magnitude usando os métodos `apply_filter` e `apply_magnitude`.")

        # Converte as imagens para CTkImage
        tk_image_x = ctk.CTkImage(Image.fromarray(self.filtered_image_x), size=(width, height))
        tk_image_y = ctk.CTkImage(Image.fromarray(self.filtered_image_y), size=(width, height))
        tk_magnitude = ctk.CTkImage(Image.fromarray(self.magnitude_image), size=(width, height))

        return tk_image_x, tk_image_y, tk_magnitude
