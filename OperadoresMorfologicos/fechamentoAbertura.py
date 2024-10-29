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
                width, height = map(int, f.readline().split())
                maxval = int(f.readline().strip())
                
                # Carrega a imagem em escala de cinza
                imagem_data = np.fromfile(f, dtype=np.uint8 if maxval < 256 else np.uint16)
                imagem = imagem_data.reshape((height, width))
            
            elif header == b'P2':
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
        e_height, e_width = elemento_estruturante.shape
        padding_y, padding_x = e_height // 2, e_width // 2

        imagem_padded = np.pad(self.imagem, ((padding_y, padding_y), (padding_x, padding_x)), mode='constant', constant_values=0)
        imagem_dilatada = np.zeros_like(self.imagem)

        for i in range(padding_y, imagem_padded.shape[0] - padding_y):
            for j in range(padding_x, imagem_padded.shape[1] - padding_x):
                vizinhanca = imagem_padded[i - padding_y:i + padding_y + 1, j - padding_x:j + padding_x + 1]
                imagem_dilatada[i - padding_y, j - padding_x] = np.max(vizinhanca * elemento_estruturante)
        
        return imagem_dilatada

    def erodir(self, elemento_estruturante=np.ones((3, 3), dtype=np.uint8)):
        e_height, e_width = elemento_estruturante.shape
        padding_y, padding_x = e_height // 2, e_width // 2

        imagem_padded = np.pad(self.imagem, ((padding_y, padding_y), (padding_x, padding_x)), mode='constant', constant_values=255)
        imagem_erodida = np.zeros_like(self.imagem)

        for i in range(padding_y, imagem_padded.shape[0] - padding_y):
            for j in range(padding_x, imagem_padded.shape[1] - padding_x):
                vizinhanca = imagem_padded[i - padding_y:i + padding_y + 1, j - padding_x:j + padding_x + 1]
                imagem_erodida[i - padding_y, j - padding_x] = np.min(vizinhanca * elemento_estruturante)
        
        return imagem_erodida

    def abertura(self, elemento_estruturante=np.ones((3, 3), dtype=np.uint8)):
        """Realiza a operação de abertura (erosão seguida de dilatação)."""
        imagem_erodida = self.erodir(elemento_estruturante)
        self.imagem = imagem_erodida  # Atualiza a imagem temporariamente para aplicar a dilatação
        imagem_aberta = self.dilatar(elemento_estruturante)
        self.imagem = imagem_erodida  # Restaura a imagem original
        return imagem_aberta

    def fechamento(self, elemento_estruturante=np.ones((3, 3), dtype=np.uint8)):
        """Realiza a operação de fechamento (dilatação seguida de erosão)."""
        imagem_dilatada = self.dilatar(elemento_estruturante)
        self.imagem = imagem_dilatada  # Atualiza a imagem temporariamente para aplicar a erosão
        imagem_fechada = self.erodir(elemento_estruturante)
        self.imagem = imagem_dilatada  # Restaura a imagem original
        return imagem_fechada

# Caminho para a imagem
caminho = r"C:\Users\jamil\OneDrive\Área de Trabalho\ProcessamentoImagem\Imagem\Utils\lena.pgm"

# Cria uma instância da classe
processador = ProcessamentoImagem(caminho)

# Aplica a operação de abertura
imagem_aberta = processador.abertura()
imagem_aberta_pil = Image.fromarray(imagem_aberta)
imagem_aberta_pil.show()

# Aplica a operação de fechamento
imagem_fechada = processador.fechamento()
imagem_fechada_pil = Image.fromarray(imagem_fechada)
imagem_fechada_pil.show()

# Opcionalmente, salve as imagens
# imagem_aberta_pil.save(r"C:\caminho_para_salvar\imagem_aberta.pgm")
# imagem_fechada_pil.save(r"C:\caminho_para_salvar\imagem_fechada.pgm")
