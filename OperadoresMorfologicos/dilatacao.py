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
    
    def dilatar(self, elemento_estruturante=np.ones((3, 3), dtype=np.uint8)):
        """
        Aplica a dilatação morfológica usando o elemento estruturante especificado.
        
        :param elemento_estruturante: Um array numpy representando o elemento estruturante (kernel) de dilatação.
        :return: Imagem dilatada.
        """
        # Pega as dimensões do elemento estruturante
        e_height, e_width = elemento_estruturante.shape
        padding_y, padding_x = e_height // 2, e_width // 2

        # Adiciona padding na imagem para aplicar a dilatação nas bordas
        imagem_padded = np.pad(self.imagem, ((padding_y, padding_y), (padding_x, padding_x)), mode='constant', constant_values=0)
        
        # Cria uma matriz para a imagem dilatada
        imagem_dilatada = np.zeros_like(self.imagem)
        
        # Aplica a dilatação
        for i in range(padding_y, imagem_padded.shape[0] - padding_y):
            for j in range(padding_x, imagem_padded.shape[1] - padding_x):
                # Extrai a vizinhança da imagem
                vizinhanca = imagem_padded[i - padding_y:i + padding_y + 1, j - padding_x:j + padding_x + 1]
                
                # Aplica a operação de dilatação: pega o máximo da vizinhança
                imagem_dilatada[i - padding_y, j - padding_x] = np.max(vizinhanca * elemento_estruturante)
        
        return imagem_dilatada

# Caminho para a imagem
caminho = r"C:\Users\jamil\OneDrive\Área de Trabalho\ProcessamentoImagem\Imagem\Utils\lena.pgm"

# Cria uma instância da classe
processador = ProcessamentoImagem(caminho)

# Aplica a dilatação com um elemento estruturante 3x3
imagem_dilatada = processador.dilatar()

# Converte para uma imagem PIL para exibição ou salvamento
imagem_dilatada_pil = Image.fromarray(imagem_dilatada)
imagem_dilatada_pil.show()

# Ou, se quiser salvar:
# imagem_dilatada_pil.save(r"C:\caminho_para_salvar\imagem_dilatada.pgm")
