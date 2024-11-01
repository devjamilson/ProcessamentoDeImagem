from PIL import Image
import numpy as np
import os
import matplotlib.pyplot as plt
import customtkinter as ctk

def carregar_imagem_pgm(caminho_imagem):
    """Carrega uma imagem no formato PGM (P2 ou P5)."""
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

    return imagem

class PrewittMagnitudeFilter:
    def __init__(self, path: str):
        """Inicializa o filtro Prewitt carregando a imagem do caminho fornecido."""
        self.image = carregar_imagem_pgm(path)  # Carrega a imagem em tons de cinza
        self.filtered_image = None

    def apply_filter(self):
        """Aplica o filtro Prewitt à imagem e calcula a magnitude do gradiente."""
        img_array = np.array(self.image, dtype=np.float32)
        
        # Definindo os kernels de Prewitt
        Gx = np.array([[-1, 0, 1],
                       [-1, 0, 1],
                       [-1, 0, 1]], dtype=np.float32)
        
        Gy = np.array([[1, 1, 1],
                       [0, 0, 0],
                       [-1, -1, -1]], dtype=np.float32)
        
        # Aplicando convolução para detectar bordas
        grad_x = self.convolve(img_array, Gx)
        grad_y = self.convolve(img_array, Gy)
        
        # Calculando a magnitude do gradiente
        magnitude = np.sqrt(grad_x**2 + grad_y**2)
        
        # Normalizar e converter para uint8 para visualização
        self.filtered_image = Image.fromarray(np.clip(magnitude, 0, 255).astype(np.uint8))
    
    def convolve(self, img, kernel):
        """Aplica a convolução manualmente à imagem usando o kernel fornecido."""
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
                output[i, j] = np.sum(region * kernel)  # Aplica a operação de convolução
        
        return output

    def get_ctk_image(self, width=None, height=None):
        """Converte a imagem filtrada para CTkImage para uso no CustomTkinter."""
        if self.filtered_image is None:
            raise ValueError("Primeiro aplique o filtro usando o método `apply_filter`.")

        # Converte a imagem para CTkImage e mantém em memória
        self.tk_image = ctk.CTkImage(self.filtered_image, size=(width, height))
        return self.tk_image

    def show_images(self):
        """Exibe a imagem original e a imagem filtrada com o filtro de Prewitt aplicado."""
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
        
        # Imagem com filtro de Prewitt aplicado
        plt.subplot(1, 2, 2)
        plt.title("Imagem com Filtro de Prewitt (Magnitude)")
        plt.imshow(self.filtered_image, cmap="gray")
        plt.axis("off")
        
        plt.show()