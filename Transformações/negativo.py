import os
import numpy as np

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

    def negativo(self):
        """Gera o negativo da imagem carregada."""
        # Calcula o negativo da imagem
        negativo_array = 255 - self.imagem
        return negativo_array

# Caminho para a imagem
caminho = r"C:\Users\jamil\OneDrive\Área de Trabalho\ProcessamentoImagem\Imagem\Utils\lena.pgm"

# Cria uma instância da classe e carrega a imagem
processador = ProcessamentoImagem(caminho)

# Obtém o negativo da imagem
imagem_negativa = processador.negativo()

# Opcional: exibe a imagem negativa usando matplotlib (se estiver disponível)
import matplotlib.pyplot as plt

plt.imshow(imagem_negativa, cmap='gray')
plt.title("Imagem Negativa")
plt.axis('off')
plt.show()
