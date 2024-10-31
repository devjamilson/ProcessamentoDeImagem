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

class HighBoostFilter:
    def __init__(self, path: str, kernel_size: int = 3, k: float = 1.5):
        self.image = carregar_imagem_pgm(path)  # Carrega a imagem em tons de cinza
        self.kernel_size = kernel_size
        self.k = k
        self.filtered_image = None
    
    def apply_filter(self):
        img_array = np.array(self.image)
        
        # Passo 1: Aplicar filtro de média para suavização
        padded_img = np.pad(img_array, self.kernel_size // 2, mode='edge')
        smoothed_array = np.zeros_like(img_array)
        
        for i in range(img_array.shape[0]):
            for j in range(img_array.shape[1]):
                region = padded_img[i:i + self.kernel_size, j:j + self.kernel_size]
                smoothed_array[i, j] = np.mean(region)
        
        # Passo 2: Calcular o realce
        mask = img_array - smoothed_array
        high_boost_array = img_array + self.k * mask
        
        # Limitar valores entre 0 e 255 para visualização correta
        high_boost_array = np.clip(high_boost_array, 0, 255)
        
        # Converter o array para uma imagem
        self.filtered_image = Image.fromarray(high_boost_array.astype(np.uint8))
    
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

# Exemplo de uso
filtro = HighBoostFilter(r"C:\Users\jamil\OneDrive\Área de Trabalho\ProcessamentoImagem\Imagem\Utils\lena.pgm", kernel_size=3, k=1.5)
filtro.apply_filter()
filtro.show_images()
