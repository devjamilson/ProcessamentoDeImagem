import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import customtkinter as ctk


class OperacoesLogicas:
    def __init__(self, caminho_imagem1, caminho_imagem2):
        """
        Inicializa a classe com duas imagens para realizar operações lógicas.
        """
        self.imagem1 = self.carregar_imagem_pgm(caminho_imagem1)
        self.imagem2 = self.carregar_imagem_pgm(caminho_imagem2)
        self.resultado = None  # Armazena o resultado da operação

    def carregar_imagem_pgm(self, caminho_imagem):
        """
        Carrega uma imagem PGM (P2 ou P5) e retorna como um array numpy.
        """
        if not os.path.exists(caminho_imagem):
            raise FileNotFoundError(f"O arquivo não foi encontrado: {caminho_imagem}")

        with open(caminho_imagem, 'rb') as f:
            header = f.readline().strip()
            
            if header == b'P5':
                width, height = map(int, f.readline().split())
                maxval = int(f.readline().strip())
                imagem_data = np.fromfile(f, dtype=np.uint8 if maxval < 256 else np.uint16)
                imagem = imagem_data.reshape((height, width))
            
            elif header == b'P2':
                width, height = map(int, f.readline().split())
                maxval = int(f.readline().strip())
                imagem_data = []
                for line in f:
                    imagem_data.extend(map(int, line.split()))
                imagem = np.array(imagem_data, dtype=np.uint8).reshape((height, width))
            
            else:
                raise ValueError("Formato PGM não suportado (esperado P2 ou P5).")

        return imagem

    def aplicar_operacao_logica(self, operacao):
        """
        Aplica uma operação lógica pixel a pixel entre as duas imagens.
        
        :param operacao: Função que define a operação lógica a ser aplicada.
        :return: Resultado da operação como uma nova matriz.
        """
        if self.imagem1.shape != self.imagem2.shape:
            raise ValueError("As imagens devem ter as mesmas dimensões para realizar a operação.")

        self.resultado = operacao(self.imagem1, self.imagem2)
        return self.resultado

    def or_logico(self):
        """
        Realiza a operação lógica OR pixel a pixel entre as duas imagens.
        """
        return self.aplicar_operacao_logica(lambda img1, img2: np.bitwise_or(img1, img2))

    def and_logico(self):
        """
        Realiza a operação lógica AND pixel a pixel entre as duas imagens.
        """
        return self.aplicar_operacao_logica(lambda img1, img2: np.bitwise_and(img1, img2))

    def xor_logico(self):
        """
        Realiza a operação lógica XOR pixel a pixel entre as duas imagens.
        """
        return self.aplicar_operacao_logica(lambda img1, img2: np.bitwise_xor(img1, img2))

    def show_images(self, operacao_nome):
        """
        Mostra as duas imagens originais e o resultado da operação lado a lado.
        """
        if self.resultado is None:
            print("Primeiro aplique uma operação antes de visualizar.")
            return
        
        plt.figure(figsize=(15, 5))

        # Imagem 1
        plt.subplot(1, 3, 1)
        plt.title("Imagem 1")
        plt.imshow(self.imagem1, cmap="gray")
        plt.axis("off")

        # Imagem 2
        plt.subplot(1, 3, 2)
        plt.title("Imagem 2")
        plt.imshow(self.imagem2, cmap="gray")
        plt.axis("off")

        # Resultado da operação
        plt.subplot(1, 3, 3)
        plt.title(f"Resultado ({operacao_nome})")
        plt.imshow(self.resultado, cmap="gray")
        plt.axis("off")

        plt.show()

    def get_ctk_image(self, width=None, height=None):
        """
        Converte o resultado da operação para CTkImage para uso no CustomTkinter.
        """
        if self.resultado is None:
            raise ValueError("Primeiro aplique uma operação antes de converter.")
        
        imagem_resultado_pil = Image.fromarray(self.resultado)
        self.tk_image = ctk.CTkImage(imagem_resultado_pil, size=(width, height))
        return self.tk_image
