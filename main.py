import customtkinter as ctk
from PIL import Image
from PIL import ImageTk
import numpy as np
from Imagem.visualizador_imagem import VisualizadorImagemCustomTk
from Transformações.negativo import ProcessamentoImagemNegativo
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

#********************************************************************************************************************
#FILTROS
#********************************************************************************************************************

diretorio_imagens = r"C:\Users\jamil\OneDrive\Área de Trabalho\ProcessamentoImagem\Imagem\Utils"
caminho_imagem = f"{diretorio_imagens}\lena.pgm" 

def combobox_callback_image(choice):
    global visualizador
    print("Combobox dropdown clicked imagem:", choice)
    
    caminho_imagem_selecionado = os.path.join(diretorio_imagens, choice)
    
    visualizador.exibir_imagem(caminho_imagem_selecionado)

container_frame = ctk.CTkFrame(tabview.tab("Filtros"))
container_frame.pack(padx=10, pady=10, fill="x")


visualizador = VisualizadorImagemCustomTk(container_frame, caminho_imagem)
visualizador.exibir(tabview.tab("Filtros"))

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
    command=lambda: print("Botão Aplicar Filtro clicado")
)
button_apply.pack(side="left", padx=10, pady=10)





#********************************************************************************************************************
#TRANSFORMAÇÕES
#********************************************************************************************************************






#********************************************************************************************************************
# HISTOGRAMA
#********************************************************************************************************************
# Variáveis globais
imagem_atual = None
equalizador = None

def combobox_callback_image_histograma(choice):
    global imagem_atual, equalizador
    print("Combobox dropdown clicked imagem:", choice)
    
    caminho_imagem_selecionado = os.path.join(diretorio_imagens, choice)
    
    imagem_atual = carregar_imagem_pgm(caminho_imagem_selecionado)
    equalizador = EqualizadorHistograma(imagem_atual)
    print("Imagem carregada:", choice)

def aplicar_equalizacao(tab):
    if equalizador is not None:
        equalizador.equalizar()  # Realiza a equalização
        equalizador.plotar_resultados(tab)  # Exibe a imagem e o histograma no tab especificado
    else:
        print("Nenhuma imagem foi carregada para equalizar.")


diretorio_imagens = r"C:\Users\jamil\OneDrive\Área de Trabalho\ProcessamentoImagem\Imagem\Utils"

container_frame_histograma = ctk.CTkFrame(tabview.tab("Histograma"))
container_frame_histograma.pack(padx=10, pady=10, fill="x")

combobox_image = ctk.CTkComboBox(
    container_frame_histograma,
    values=["lena.pgm", "Lenag.pgm", "Airplane.pgm", "Lenasalp.pgm"],
    command=combobox_callback_image_histograma,
    width=270,
    font=("Helvetica", 14),
)
combobox_image.pack(side="left", padx=10, pady=10)

# Botão "Equalizar" para realizar a equalização
botao_equalizar = ctk.CTkButton(
    container_frame_histograma,
    text="Equalizar",
    command=lambda: aplicar_equalizacao(tabview.tab("Histograma")),  # Usando lambda para passar o argumento
    width=100,
    font=("Helvetica", 14)
)
botao_equalizar.pack(side="left", padx=10, pady=10)





#********************************************************************************************************************
# MORFOLOGIA
#********************************************************************************************************************

def combobox_callback_image_morfologia(choice):
    global visualizador_morfologia
    print("Combobox dropdown clicked imagem:", choice)
    
    caminho_imagem_selecionado = os.path.join(diretorio_imagens, choice)
    
    visualizador_morfologia.exibir_imagem(caminho_imagem_selecionado)

container_frame_morfologia= ctk.CTkFrame(tabview.tab("Morfologia"))
container_frame_morfologia.pack(padx=10, pady=10, fill="x")

combobox_image = ctk.CTkComboBox(
    container_frame_morfologia,
    values=["lena.pgm", "Lenag.pgm", "Airplane.pgm", "Lenasalp.pgm"],
    command=combobox_callback_image_morfologia,
    width=270,
    font=("Helvetica", 14),
)
combobox_image.pack(side="left", padx=10, pady=10)
visualizador_morfologia = VisualizadorImagemCustomTk(container_frame_morfologia, caminho_imagem)
visualizador_morfologia.exibir(tabview.tab("Morfologia"))


def combobox_callback(choice):
    print("Combobox dropdown clicked:", choice)

combobox_var_morfologia = ctk.StringVar(value="Escolha a Morfologia")
combobox_morfologia = ctk.CTkComboBox(
    container_frame_morfologia,
    values=[
        "Dilatação", "Erosão", 
        "Fechamento", "Abertura", 
        "Hit Or Miss", "Top Hat", "Bottom Hat"
    ],
    command=combobox_callback,
    variable=combobox_var_morfologia,
    width=270,
    font=("Helvetica", 14),
)
combobox_morfologia.pack(side="left", padx=10, pady=10)

button_apply_morfologia= ctk.CTkButton(
    container_frame_morfologia,
    text="Aplicar Morfologia",
    command=lambda: print("Botão Aplicar Morfologia"),
    width=200,
)
button_apply_morfologia.pack(side="left", padx=10, pady=10)


#====================================================================================================================
# Inicia o loop da interface
#====================================================================================================================
janela.mainloop()
