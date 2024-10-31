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




class MedianFilter:
    def __init__(self, path: str, kernel_size: int = 3):
        self.image = carregar_imagem_pgm(path)  # Carrega a imagem em tons de cinza
        self.kernel_size = kernel_size
        self.filtered_image = None
    
    def apply_filter(self):
        img_array = np.array(self.image)
        padded_img = np.pad(img_array, self.kernel_size // 2, mode='edge')
        output_array = np.zeros_like(img_array)
        
        for i in range(img_array.shape[0]):
            for j in range(img_array.shape[1]):
                region = padded_img[i:i + self.kernel_size, j:j + self.kernel_size]
                output_array[i, j] = np.median(region)
        
        self.filtered_image = Image.fromarray(output_array.astype(np.uint8))
    
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
        
        # Imagem com filtro de mediana aplicado
        plt.subplot(1, 2, 2)
        plt.title("Imagem com Filtro de Mediana")
        plt.imshow(self.filtered_image, cmap="gray")
        plt.axis("off")
        
        plt.show()

# Exemplo de uso
filtro = MedianFilter(r"C:\Users\jamil\OneDrive\Área de Trabalho\ProcessamentoImagem\Imagem\Utils\lena.pgm", kernel_size=3)
filtro.apply_filter()
filtro.show_images()
