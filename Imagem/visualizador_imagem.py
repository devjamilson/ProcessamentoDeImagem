import os
import numpy as np
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import customtkinter as ctk
import io

# Classe para visualizar imagens PGM em Customtkinter
class VisualizadorImagemCustomTk:

    def __init__(self, master, caminho_imagem):
        self.master = master
        self.caminho_imagem = caminho_imagem
        self.imagem = self.carregar_imagem()
        self.label_imagem = None  # Inicializa o label como None
        self.label_histograma = None  

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

    def exibir(self, tab, selecao="Filtros"):
        """Exibe a imagem carregada no widget CTkLabel no tabview especificado."""
        if self.imagem is not None:
            if self.label_imagem is None:
                
                # Cria o label apenas na primeira vez
                if selecao == "Filtros":
                    self.label_imagem = ctk.CTkLabel(tab, image=self.imagem, text="")
                    self.label_imagem.pack(side='left', padx=200)
                elif selecao == "Operacao": 
                    self.label_imagem = ctk.CTkLabel(tab, image=self.imagem, text="")
                    self.label_imagem.pack(side='left', padx=50)    
            else:
                # Atualiza a imagem no label já existente
                self.label_imagem.configure(image=self.imagem)
                    
        else:
            print("Não foi possível carregar a imagem.")

    def exibir_img_histo(self, tab):
            """Exibe a imagem carregada no widget CTkLabel no tabview especificado."""
            if self.imagem is not None:
                if self.label_imagem is None:
                    # Cria o label apenas na primeira vez
                    self.label_imagem = ctk.CTkLabel(tab, image=self.imagem, text="")
                    self.label_imagem.pack(side='top', anchor='nw', padx=200)

                else:
                    # Atualiza a imagem no label já existente
                    self.label_imagem.configure(image=self.imagem)
            else:
                print("Não foi possível carregar a imagem.")

    def exibir_imagem_histo(self, novo_caminho_imagem):
            """Atualiza a imagem exibida com um novo caminho de imagem."""
            self.caminho_imagem = novo_caminho_imagem
            self.imagem = self.carregar_imagem()
            self.exibir_img_histo(self.master) 

    def exibir_imagem(self, novo_caminho_imagem):
        """Atualiza a imagem exibida com um novo caminho de imagem."""
        self.caminho_imagem = novo_caminho_imagem
        self.imagem = self.carregar_imagem()
        self.exibir(self.master)  # Atualiza a imagem exibida

     # Atualiza a imagem exibida

    def mostrar_histograma(self, tab):
        """Exibe o histograma da imagem carregada diretamente em uma CTkLabel."""
        if self.imagem is None:
            print("Nenhuma imagem carregada para exibir o histograma.")
            return
        
        # Converte o CTkImage para um array numpy para processamento
        pil_image = self.imagem._light_image  # Acessa a imagem PIL do CTkImage
        np_image = np.array(pil_image)

        # Calcula o histograma
        histograma, bins = np.histogram(np_image.flatten(), bins=256, range=[0, 256])

        # Cria uma figura do histograma e salva como imagem no buffer
        fig, ax = plt.subplots(figsize=(5, 3))  # Ajuste o tamanho conforme necessário
        ax.bar(bins[:-1], histograma, width=1, color='gray')
        ax.set_title("Histograma da Imagem")
        ax.set_xlabel("Intensidade dos Pixels")
        ax.set_ylabel("Número de Pixels")
        ax.set_xlim([0, 256])

        # Salva a figura em um buffer de memória
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        plt.close(fig)  # Fecha a figura para liberar memória

        # Converte a imagem do buffer para PIL e depois para CTkImage
        histograma_imagem = Image.open(buf)
        ctk_histograma_imagem = ctk.CTkImage(histograma_imagem, size=(440, 250))  # Ajuste o tamanho conforme necessário

        # Exibe na CTkLabel dentro do tab especificado
        if not hasattr(self, 'label_histograma') or self.label_histograma is None:
            # Cria a label apenas na primeira vez
            self.label_histograma = ctk.CTkLabel(tab, image=ctk_histograma_imagem, text="")
            self.label_histograma.pack(side='left')
        else:
            # Atualiza a imagem no label já existente
            self.label_histograma.configure(image=ctk_histograma_imagem)

