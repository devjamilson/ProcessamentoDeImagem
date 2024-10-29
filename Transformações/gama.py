import os
import numpy as np
from PIL import Image

class ProcessamentoImagem:
    def __init__(self, caminho):
        self.imagem = self.carregar_imagem_pgm(caminho)
        
    def carregar_imagem_pgm(self, caminho_imagem):
        """Carrega uma imagem PGM (P2 ou P5) e retorna como um array numpy."""
        if not os.path.exists(caminho_imagem):
            raise FileNotFoundError(f"O arquivo não foi encontrado: {caminho_imagem}")

        with open(caminho_imagem, 'rb') as f:
            header = f.readline().strip()
            
            # Verifica o formato (P2 para ASCII, P5 para binário)
            if header == b'P5':
                # Formato binário
                width, height = map(int, f.readline().split())
                maxval = int(f.readline().strip())
                
                # Carrega a imagem em escala de cinza
                imagem_data = np.fromfile(f, dtype=np.uint8 if maxval < 256 else np.uint16)
                imagem = imagem_data.reshape((height, width))
            
            elif header == b'P2':
                # Formato ASCII
                width, height = map(int, f.readline().split())
                maxval = int(f.readline().strip())
                
                # Carrega a imagem linha por linha em escala de cinza
                imagem_data = []
                for line in f:
                    imagem_data.extend(map(int, line.split()))
                imagem = np.array(imagem_data, dtype=np.uint8).reshape((height, width))
            
            else:
                raise ValueError("Formato PGM não suportado (esperado P2 ou P5).")

        return imagem
    
    def transformar_gamma(self, c, gamma):
        """Aplica a transformação gamma à imagem."""
        # Normaliza os valores da imagem para o intervalo [0, 1]
        imagem_normalizada = self.imagem / 255.0
        
        # Aplica a transformação gamma: S = c * r^gamma
        imagem_transformada = c * np.power(imagem_normalizada, gamma)
        
        # Reescala de volta para o intervalo [0, 255]
        imagem_transformada = np.clip(imagem_transformada * 255, 0, 255).astype(np.uint8)
        
        return imagem_transformada

# Caminho para a imagem
caminho = r"C:\Users\jamil\OneDrive\Área de Trabalho\ProcessamentoImagem\Imagem\Utils\lena.pgm"

# Cria uma instância da classe
processador = ProcessamentoImagem(caminho)

# Define os parâmetros para a transformação gamma
c = 1.0    # Fator de escala
gamma = 0.5  # Valor de gamma, deve estar entre 0 e 1

# Aplica a transformação gamma
imagem_gamma = processador.transformar_gamma(c, gamma)

# Converte para uma imagem PIL para exibição ou salvamento
imagem_gamma_pil = Image.fromarray(imagem_gamma)
imagem_gamma_pil.show()

# Ou, se quiser salvar:
# imagem_gamma_pil.save(r"C:\caminho_para_salvar\imagem_gamma.pgm")
