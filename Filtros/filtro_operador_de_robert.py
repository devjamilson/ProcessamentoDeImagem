from PIL import Image
import numpy as np
import os
import matplotlib.pyplot as plt

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

class RobertsFilter:
    def __init__(self, path: str):
        self.image = carregar_imagem_pgm(path)  # Carrega a imagem em tons de cinza
        self.filtered_image = None
    
    def apply_filter(self):
        img_array = np.array(self.image, dtype=np.float32)
        
        # Definindo os kernels de Roberts
        Gx = np.array([[1, 0], [0, -1]], dtype=np.float32)
        Gy = np.array([[0, 1], [-1, 0]], dtype=np.float32)
        
        # Aplicando convolução para detectar bordas
        grad_x = self.convolve(img_array, Gx)
        grad_y = self.convolve(img_array, Gy)
        
        # Calculando a magnitude do gradiente
        magnitude = np.sqrt(grad_x**2 + grad_y**2)
        
        # Normalizar e converter para uint8 para visualização
        magnitude = np.clip(magnitude, 0, 255).astype(np.uint8)
        self.filtered_image = Image.fromarray(magnitude)
    
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
        
        # Imagem com filtro de Roberts aplicado
        plt.subplot(1, 2, 2)
        plt.title("Imagem com Filtro de Roberts")
        plt.imshow(self.filtered_image, cmap="gray")
        plt.axis("off")
        
        plt.show()

# Exemplo de uso
filtro = RobertsFilter(r"C:\Users\jamil\OneDrive\Área de Trabalho\ProcessamentoImagem\Imagem\Utils\lena.pgm")
filtro.apply_filter()
filtro.show_images()
