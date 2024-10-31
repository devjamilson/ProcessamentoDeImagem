import os
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import customtkinter as ctk

# Classe para visualizar imagens PGM em Customtkinter
class VisualizadorImagemCustomTk:
    def __init__(self, master, caminho_imagem):
        self.master = master
        self.caminho_imagem = caminho_imagem
        self.imagem = self.carregar_imagem()
        self.label_imagem = None  # Inicializa o label como None

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
            if self.label_imagem is None:
                # Cria o label apenas na primeira vez
                self.label_imagem = ctk.CTkLabel(tab, image=self.imagem, text="")
                self.label_imagem.pack(side='left', padx=200)
            else:
                # Atualiza a imagem no label já existente
                self.label_imagem.configure(image=self.imagem)
        else:
            print("Não foi possível carregar a imagem.")

    def exibir_imagem(self, novo_caminho_imagem):
        """Atualiza a imagem exibida com um novo caminho de imagem."""
        self.caminho_imagem = novo_caminho_imagem
        self.imagem = self.carregar_imagem()
        self.exibir(self.master)  # Atualiza a imagem exibida

    def mostrar_histograma(self):
        """Exibe o histograma da imagem carregada."""
        if self.imagem is None:
            print("Nenhuma imagem carregada para exibir o histograma.")
            return
        
        histograma, bins = np.histogram(self.imagem.flatten(), bins=256, range=[0, 256])
        
        plt.figure(figsize=(10, 5))
        plt.title("Histograma da Imagem PGM")
        plt.xlabel("Intensidade dos Pixels")
        plt.ylabel("Número de Pixels")
        plt.xlim([0, 256])
        plt.bar(bins[:-1], histograma, width=1, color='gray')
        plt.show()

    def exibir_imagem_transformada(self, imagem_transformada):
        """Exibe a imagem transformada no visualizador."""
        imagem_transformada = imagem_transformada.resize((256, 256))  # Ajuste o tamanho da imagem, se necessário
        imagem_tk = ImageTk.PhotoImage(imagem_transformada)  # Converte a imagem PIL para um objeto ImageTk
        self.label_imagem.configure(image=imagem_tk)  # Atualiza o label com a nova imagem transformada
        self.label_imagem.image = imagem_tk  # Armazena uma referência à imagem
