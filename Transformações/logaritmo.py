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
    
    def transformar_logaritmo(self, a):
        """Aplica a transformação logarítmica à imagem."""
        # Normaliza os valores da imagem para o intervalo [0, 1]
        imagem_normalizada = self.imagem / 255.0
        
        # Aplica a transformação logarítmica: S = a * log(1 + r)
        imagem_transformada = a * np.log1p(imagem_normalizada)
        
        # Reescala de volta para o intervalo [0, 255]
        imagem_transformada = np.clip(imagem_transformada * 255, 0, 255).astype(np.uint8)
        
        return imagem_transformada

# Caminho para a imagem
caminho = r"C:\Users\jamil\OneDrive\Área de Trabalho\ProcessamentoImagem\Imagem\Utils\lena.pgm"

# Cria uma instância da classe
processador = ProcessamentoImagem(caminho)

# Define o parâmetro para a transformação logarítmica
a = 1.0  # Constante de intensidade da transformação logarítmica

# Aplica a transformação logarítmica
imagem_logaritmica = processador.transformar_logaritmo(a)

# Converte para uma imagem PIL para exibição ou salvamento
imagem_logaritmica_pil = Image.fromarray(imagem_logaritmica)
imagem_logaritmica_pil.show()

# Ou, se quiser salvar:
# imagem_logaritmica_pil.save(r"C:\caminho_para_salvar\imagem_logaritmica.pgm")
