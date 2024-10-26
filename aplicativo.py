import os
from Imagem.visualizador_imagem import VisualizadorImagemPGM
from Filtros.filtro_exemplo import FiltroExemplo

def main():
    caminho_imagem = r"C:\Users\jamil\OneDrive\Área de Trabalho\ProcessamentoImagem\Utils\lena.pgm"  # Altere para o caminho da sua imagem

    # Verificar se o arquivo existe
    if not os.path.exists(caminho_imagem):
        print(f"O arquivo não foi encontrado: {caminho_imagem}")
        return

    try:
        # Inicializa o visualizador de imagem
        visualizador = VisualizadorImagemPGM(caminho_imagem)

        # Carrega a imagem
        visualizador.carregar_imagem()

        # Apresenta a imagem original
        visualizador.visualizar()

        # Aplicar um filtro
        filtro = FiltroExemplo()
        imagem_filtrada = filtro.aplicar(visualizador.imagem)

        # Salvar e mostrar a imagem filtrada
        visualizador.imagem = imagem_filtrada
        caminho_saida = r"C:\Users\jamil\OneDrive\Área de Trabalho\ProcessamentoImagem\Imagem\imagem_filtrada.pgm"  # Altere para o caminho de saída desejado
        visualizador.salvar_imagem(caminho_saida)

        # Mostrar a imagem filtrada
        visualizador.visualizar()

    except Exception as e:
        print(f"Erro ao processar a imagem: {e}")

if __name__ == "__main__":
    main()
