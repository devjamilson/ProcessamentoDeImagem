import os
import numpy as np
from PIL import Image
import customtkinter as ctk

# Classe para visualizar imagens PGM em Customtkinter
class VisualizadorImagem2:

    def __init__(self, master2, caminho_imagem2):
        self.master2 = master2
        self.caminho_imagem2 = caminho_imagem2
        self.imagem2 = self.carregar_imagem()
        self.label_imagem2 = None  # Inicializa o label como None 

    def carregar_imagem(self):
        """Carrega uma imagem PGM (P2 ou P5) e converte para um objeto CTkImage."""
        if not os.path.exists(self.caminho_imagem2):
            raise FileNotFoundError(f"O arquivo não foi encontrado: {self.caminho_imagem2}")

        try:
            with open(self.caminho_imagem2, 'rb') as f:
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

    def exibir2(self, tab):
        """Exibe a imagem carregada no widget CTkLabel no tabview especificado."""
        if self.imagem2 is not None:
            if self.label_imagem2 is None:
                # Cria o label apenas na primeira vez
                self.label_imagem2 = ctk.CTkLabel(tab, image=self.imagem2, text="")
                self.label_imagem2.pack(side='left')
            else:
                # Atualiza a imagem no label já existente
                self.label_imagem2.configure(image=self.imagem2)
                    
        else:
            print("Não foi possível carregar a imagem.")


    def exibir_imagem2(self, novo_caminho_imagem):
        """Atualiza a imagem exibida com um novo caminho de imagem."""
        self.caminho_imagem2 = novo_caminho_imagem
        self.imagem2 = self.carregar_imagem()
        self.exibir2(self.master2)  # Atualiza a imagem exibida

