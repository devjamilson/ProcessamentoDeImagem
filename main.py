import customtkinter as ctk
from PIL import Image
from PIL import ImageTk
import numpy as np
from Imagem.visualizador_imagem import VisualizadorImagemCustomTk
from Transformações.negativo import ProcessamentoImagemNegativo
from Filtros.filtro_suavizacao_mediana import MedianFilter 
from Filtros.filtro_suavizacao_media import MediaFilter
from Filtros.filtro_passa_alta_basico import HighPassFilter
from Filtros.filtro_operador_sobel import SobelFilter
from Filtros.filtro_operador_prewitt import PrewittFilter
from Filtros.filtro_operador_de_prewitt_magnitude import PrewittMagnitudeFilter
from Filtros.filtro_de_alto_reforco import HighBoostFilter
from Filtros.filtro_operador_de_robert import RobertsFilter

from Histograma.equalizar_histograma import EqualizadorHistograma, carregar_imagem_pgm
import os

#====================================================================================================================
# Cria a janela
#====================================================================================================================
janela = ctk.CTk()
# Configurando a estrutura da janela
janela.title('Projeto de Processamento de Imagens')
janela.geometry('1370x700+0+0')  # Coloca a janela no canto superior esquerdo
janela.maxsize(width=1370, height=700)
janela.minsize(width=1370, height=700)
#====================================================================================================================
# Abas
#====================================================================================================================
tabview = ctk.CTkTabview(janela, width=1370, height=700, fg_color="#f2f2f2")
tabview.pack(pady=20, padx=20, fill="both", expand=True)
# Adicionando as abas
tabview.add("Filtros")
tabview.add("Transformações")
tabview.add("Histograma")
tabview.add("Morfologia")
#====================================================================================================================
# Adicionando Funcionandalidades Nas Abas
#====================================================================================================================
diretorio_imagens = r"C:\Users\jamil\OneDrive\Área de Trabalho\ProcessamentoImagem\Imagem\Utils"
caminho_imagem = f"{diretorio_imagens}\lena.pgm" 

#********************************************************************************************************************
#FILTROS
#********************************************************************************************************************

#HEADER
container_frame = ctk.CTkFrame(tabview.tab("Filtros"))
container_frame.pack(padx=10, pady=10, fill="x")

#Instância da Classe 
visualizador = VisualizadorImagemCustomTk(container_frame, caminho_imagem)

#imagem padrão
visualizador.exibir(tabview.tab("Filtros"))
#visualizador.exibir_imagem_transformada(tabview.tab("Filtros"), imagem_transformada= )

# Variáveis globais para manter seleção de filtro e caminho de imagem
filtro_selecionado = None
caminho_imagem_selecionado = None

# Função chamada no Select das imagens
def combobox_callback_image(choice):
    global caminho_imagem_selecionado
    print("Combobox dropdown clicked imagem:", choice)
    caminho_imagem_selecionado = os.path.join(diretorio_imagens, choice)
    visualizador.exibir_imagem(caminho_imagem_selecionado)

# Função chamada ao selecionar o filtro
def combobox_callback(choice):
    global filtro_selecionado
    print("Combobox dropdown clicked filtro:", choice)
    filtro_selecionado = choice

# Função para aplicar o filtro selecionado e exibir a imagem resultante
def aplicar_filtro():
    global filtro_selecionado, caminho_imagem_selecionado, label  # Incluindo label como global
    
    filtro_selecionado = 'Filtro Operador de Robert'

    print("Valor de filtro selecionado:", filtro_selecionado)
    print("Valor de caminho da imagem:", caminho_imagem_selecionado)

    if filtro_selecionado == "Filtro de Suavização - mediana":
        filtro = MedianFilter(caminho_imagem_selecionado, kernel_size=3)
        filtro.apply_filter()
        tk_image = filtro.get_ctk_image(width=256, height=256)
        
        label = ctk.CTkLabel(tabview.tab("Filtros"), image=tk_image, text="")
        label.pack(side='left', padx=200); 
        print("Filtro de suavização mediana aplicado e imagem exibida.")

    elif filtro_selecionado == "Filtro de Suavização - média":
        filtro = MediaFilter(caminho_imagem_selecionado, kernel_size=3)
        filtro.apply_filter()
        tk_image = filtro.get_ctk_image(width=256, height=256)
        
        label = ctk.CTkLabel(tabview.tab("Filtros"), image=tk_image, text="")
        label.pack(side='left', padx=200); 
        print("Filtro de suavização média aplicado e imagem exibida.")
    
    elif filtro_selecionado == "Filtro Passa Alta Básico":
        filtro = HighPassFilter(caminho_imagem_selecionado)
        filtro.apply_filter()
        tk_image = filtro.get_ctk_image(width=256, height=256)
        
        label = ctk.CTkLabel(tabview.tab("Filtros"), image=tk_image, text="")
        label.pack(side='left', padx=200); 
        print("Filtro de suavização média aplicado e imagem exibida.")

    elif filtro_selecionado == "Filtro Operador de Sobel":
        filtro = SobelFilter(caminho_imagem_selecionado)  # Usando a classe SobelFilter
        filtro.apply_filter()
        tk_image_x, tk_image_y = filtro.get_ctk_images(width=256, height=256)  # Obtendo ambas as imagens filtradas

        # Exibindo a imagem filtrada em X
        label_x = ctk.CTkLabel(tabview.tab("Filtros"), image=tk_image_x, text="")
        label_x.pack(side='left', padx=10)

        # Exibindo a imagem filtrada em Y
        label_y = ctk.CTkLabel(tabview.tab("Filtros"), image=tk_image_y, text="")
        label_y.pack(side='left', padx=10)

        print("Filtro de Sobel aplicado e imagens exibidas.")

    elif filtro_selecionado == "Filtro Operador de Prewitt":
        filtro = PrewittFilter(caminho_imagem_selecionado)  # Usando a classe SobelFilter
        filtro.apply_filter()
        tk_image_x, tk_image_y = filtro.get_ctk_images(width=256, height=256)  # Obtendo ambas as imagens filtradas

        # Exibindo a imagem filtrada em X
        label_x = ctk.CTkLabel(tabview.tab("Filtros"), image=tk_image_x, text="")
        label_x.pack(side='left', padx=10)

        # Exibindo a imagem filtrada em Y
        label_y = ctk.CTkLabel(tabview.tab("Filtros"), image=tk_image_y, text="")
        label_y.pack(side='left', padx=10)

        print("Filtro Operador de Prewitt aplicado e imagens exibidas.")

    elif filtro_selecionado == "Filtro Operador de Prewitt - Magnitude":
        filtro = PrewittMagnitudeFilter(caminho_imagem_selecionado)
        filtro.apply_filter()
        tk_image = filtro.get_ctk_image(width=256, height=256)
        
        label = ctk.CTkLabel(tabview.tab("Filtros"), image=tk_image, text="")
        label.pack(side='left', padx=200); 
        print("Filtro Operador de Prewitt Magnitude aplicado e imagem exibida.")

    elif filtro_selecionado == "Filtro de Alto Reforço":
        filtro = HighBoostFilter(caminho_imagem_selecionado)
        filtro.apply_filter()
        tk_image = filtro.get_ctk_image(width=256, height=256)
        
        label = ctk.CTkLabel(tabview.tab("Filtros"), image=tk_image, text="")
        label.pack(side='left', padx=200); 
        print("Filtro de Alto Reforço aplicado e imagem exibida.")

    elif filtro_selecionado == "Filtro Operador de Robert":
        filtro = RobertsFilter(caminho_imagem_selecionado)
        filtro.apply_filter()
        tk_image = filtro.get_ctk_image(width=256, height=256)
        
        label = ctk.CTkLabel(tabview.tab("Filtros"), image=tk_image, text="")
        label.pack(side='left', padx=200); 
        print("Filtro de Operador de Robert aplicado e imagem exibida.")

    else:
        print("Selecione um filtro de suavização mediana para aplicar.")

combobox_image = ctk.CTkComboBox(
    container_frame,
    values=["lena.pgm", "Lenag.pgm", "Airplane.pgm", "Lenasalp.pgm"],
    command=combobox_callback_image,
    width=270,
    font=("Helvetica", 14),
)
combobox_image.pack(side="left", padx=10, pady=10)


def combobox_callback(choice):
    print("Combobox dropdown clicked:", choice)

combobox_var = ctk.StringVar(value="Escolha o Filtro")
combobox_filter = ctk.CTkComboBox(
    container_frame,
    values=[
        "Filtro de Suavização - média", "Filtro de Suavização - mediana", 
        "Filtro Passa Alta Básico", "Filtro Operador de Robert", 
        "Filtro Operador de Prewitt", "Filtro Operador de Prewitt - Magnitude", 
        "Filtro de Alto Reforço", "Filtro Operador de Sobel"
    ],
    command=combobox_callback,
    variable=combobox_var,
    width=270,
    font=("Helvetica", 14),
)
combobox_filter.pack(side="left", padx=10, pady=10)

button_apply = ctk.CTkButton(
    container_frame,
    text="Aplicar Filtro",
    command=aplicar_filtro
)
button_apply.pack(side="left", padx=10, pady=10)


#====================================================================================================================
# Inicia o loop da interface
#====================================================================================================================
janela.mainloop()
