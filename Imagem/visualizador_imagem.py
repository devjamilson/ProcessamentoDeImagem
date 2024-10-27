import os
import numpy as np
from PIL import Image
import customtkinter as ctk

# Classe para visualizar imagens PGM em Customtkinter
class VisualizadorImagemCustomTk:
    def __init__(self, master, caminho_imagem):
        self.master = master
        self.caminho_imagem = caminho_imagem
        self.imagem = self.carregar_imagem()

    def carregar_imagem(self):
        """Carrega uma imagem PGM (P2 ou P5) e converte para um objeto CTkImage."""
        if not os.path.exists(self.caminho_imagem):
            raise FileNotFoundError(f"O arquivo não foi encontrado: {self.caminho_imagem}")

        try:
            with open(self.caminho_imagem, 'rb') as f:
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

                # Converte o array numpy para uma imagem PIL
                imagem_pil = Image.fromarray(imagem, mode='L')
                return ctk.CTkImage(light_image=imagem_pil, dark_image=imagem_pil, size=(256,256))  # Converte para CTkImage
        except Exception as e:
            print(f"Erro ao carregar a imagem: {e}")
            return None

    def exibir(self, tab):
        """Exibe a imagem carregada no widget CTkLabel no tabview especificado."""
        if self.imagem is not None:
            label_imagem = ctk.CTkLabel(tab, image=self.imagem, text="")
            label_imagem.pack(pady=10)
        else:
            print("Não foi possível carregar a imagem.")
