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
    
    def transformar_faixa_dinamica(self):
        """Aplica a transformação de faixa dinâmica à imagem para ajustar os valores ao intervalo [0, 255]."""
        min_val = self.imagem.min()
        max_val = self.imagem.max()
        
        # Ajusta a faixa dinâmica: S(r) = (r - min_val) * 255 / (max_val - min_val)
        imagem_transformada = (self.imagem - min_val) * 255.0 / (max_val - min_val)
        
        # Converte o resultado para o intervalo [0, 255] e para uint8
        imagem_transformada = np.clip(imagem_transformada, 0, 255).astype(np.uint8)
        
        return imagem_transformada

# Caminho para a imagem
caminho = r"C:\Users\jamil\OneDrive\Área de Trabalho\ProcessamentoImagem\Imagem\Utils\lena.pgm"

# Cria uma instância da classe
processador = ProcessamentoImagem(caminho)

# Aplica a transformação de faixa dinâmica
imagem_faixa_dinamica = processador.transformar_faixa_dinamica()

# Converte para uma imagem PIL para exibição ou salvamento
imagem_faixa_dinamica_pil = Image.fromarray(imagem_faixa_dinamica)
imagem_faixa_dinamica_pil.show()

# Ou, se quiser salvar:
# imagem_faixa_dinamica_pil.save(r"C:\caminho_para_salvar\imagem_faixa_dinamica.pgm")
