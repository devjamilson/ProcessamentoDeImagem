from PIL import Image
import matplotlib.pyplot as plt

def visualizar_imagem_pgm(caminho_imagem):
    # Abre a imagem usando PIL
    imagem = Image.open(caminho_imagem)
    
    # Converte a imagem para escala de cinza, caso necessário
    imagem = imagem.convert('L')
    
    # Exibe a imagem usando matplotlib
    plt.imshow(imagem, cmap='gray')
    plt.axis('off')  # Remove os eixos para uma visualização mais limpa
    plt.show()

# Exemplo de uso
visualizar_imagem_pgm("lena.pgm")
