import customtkinter as ctk
from PIL import Image
from PIL import ImageTk
import numpy as np
from Imagem.visualizador_imagem import VisualizadorImagemCustomTk
from Filtros.filtro_suavizacao_mediana import MedianFilter 
from Filtros.filtro_suavizacao_media import MediaFilter
from Filtros.filtro_passa_alta_basico import HighPassFilter
from Filtros.filtro_operador_sobel import SobelFilter
from Filtros.filtro_operador_prewitt import PrewittFilter
from Filtros.filtro_operador_de_prewitt_magnitude import PrewittMagnitudeFilter
from Filtros.filtro_de_alto_reforco import HighBoostFilter
from Filtros.filtro_operador_de_robert import RobertsFilter

from Transformações.negativo import Negativo
from Transformações.gama import Gama
from Transformações.logaritmo import Log
from Transformações.sigmoide import Sigmoide
from Transformações.faixaDinamica import FaixaDinamica


from OperadoresMorfologicos.dilatacao import Dilatacao
from OperadoresMorfologicos.erosao import Erosao
from OperadoresMorfologicos.abertura import Abertura
from OperadoresMorfologicos.fechamento import Fechamento
from OperadoresMorfologicos.topHat import TopHat
from OperadoresMorfologicos.bottomHat import BottomHat
from OperadoresMorfologicos.hitOrMiss import HitOrMiss

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
label = None
label_x = None
label_y = None

# Função chamada no Select das imagens
def combobox_callback_image(choice):
    global caminho_imagem_selecionado
    print("Combobox dropdown clicked imagem:", choice)
    caminho_imagem_selecionado = os.path.join(diretorio_imagens, choice)
    visualizador.exibir_imagem(caminho_imagem_selecionado)


def combobox_callback(choice):
    global filtro_selecionado
    print("Combobox dropdown clicked filtro:", choice)
    filtro_selecionado = choice

# Função para aplicar o filtro selecionado e exibir a imagem resultante
def aplicar_filtro():
    global filtro_selecionado, caminho_imagem_selecionado, label, label_x, label_y # Incluindo label como global
    

    print("Valor de filtro selecionado:", filtro_selecionado)
    print("Valor de caminho da imagem:", caminho_imagem_selecionado)

     
    if label is not None:
       label.destroy() 

    if label_y is not None:
        label_y.destroy()
    if label_x is not None:
        label_x.destroy()

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
        print("Selecione um filtro para aplicar.")

combobox_image = ctk.CTkComboBox(
    container_frame,
    values=["lena.pgm", "Lenag.pgm", "Airplane.pgm", "Lenasalp.pgm"],
    command=combobox_callback_image,
    width=270,
    font=("Helvetica", 14),
)
combobox_image.pack(side="left", padx=10, pady=10)


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


#********************************************************************************************************************
#TRANSFORMAÇÕES
#********************************************************************************************************************
#HEADER
container_frame_transformacao = ctk.CTkFrame(tabview.tab("Transformações"))
container_frame_transformacao.pack(padx=10, pady=10, fill="x")

#usando a instância da classe Visualizar Imagens para mostras a imagem na aba transformaçoes
#Instância da Classe 
visualizador_transformacao = VisualizadorImagemCustomTk(container_frame, caminho_imagem)
visualizador_transformacao.exibir(tabview.tab("Transformações"))

# Variáveis globais para manter seleção de filtro e caminho de imagem
transformacao_selecionada = None
caminho_imagem_selecionado_transformacoes = None
label_transformacao = None


# Função chamada no Select das imagens
def combobox_callback_image_transformacao(choice):
    global caminho_imagem_selecionado_transformacoes
    print("Combobox dropdown clicked imagem:", choice)
    caminho_imagem_selecionado_transformacoes = os.path.join(diretorio_imagens, choice)
    visualizador_transformacao.exibir_imagem(caminho_imagem_selecionado_transformacoes)

def combobox_callback_transformacao(choice):
    global transformacao_selecionada
    print("Combobox dropdown clicked filtro:", choice)
    transformacao_selecionada = choice

# Função para aplicar o filtro selecionado e exibir a imagem resultante
def aplicar_transformacao():
    global transformacao_selecionada, caminho_imagem_selecionado_transformacoes, label_transformacao  # Incluindo label como global
    

    print("Valor de filtro selecionado:", transformacao_selecionada)
    print("Valor de caminho da imagem:", caminho_imagem_selecionado_transformacoes)

     
    if label_transformacao is not None:
       label_transformacao.destroy() 

    if transformacao_selecionada == "Faixa Dinâmica":
       transformacao = FaixaDinamica(caminho_imagem_selecionado_transformacoes)
       transformacao.transformar_faixa_dinamica()
       tk_image = transformacao.get_ctk_image(width=256, height=256)
        
       label_transformacao = ctk.CTkLabel(tabview.tab("Transformações"), image=tk_image, text="")
       label_transformacao.pack(side='left', padx=200); 
       print("Transformação de Faixa Dinâmica aplicado a imagem exibida.")

    elif transformacao_selecionada == "Gama":
        transformacao = Gama(caminho_imagem_selecionado_transformacoes)
        #vator de escala, fator gama
        transformacao.apply_gamma(1.0, 0.5)
        tk_image = transformacao.get_ctk_image(width=256, height=256)
            
        label_transformacao = ctk.CTkLabel(tabview.tab("Transformações"), image=tk_image, text="")
        label_transformacao.pack(side='left', padx=200); 
        print("Transformação de Gama aplicada a imagem exibida.")

    elif transformacao_selecionada == "Logaritmica":
        transformacao = Log(caminho_imagem_selecionado_transformacoes)
        #Parametro da transformação logaritmica
        transformacao.apply_log(1.0)
        tk_image = transformacao.get_ctk_image(width=256, height=256)
            
        label_transformacao = ctk.CTkLabel(tabview.tab("Transformações"), image=tk_image, text="")
        label_transformacao.pack(side='left', padx=200); 
        print("Transformação Logaritmica aplicada a imagem exibida.")
    
    elif transformacao_selecionada == "Negativo":
        transformacao =  Negativo(caminho_imagem_selecionado_transformacoes)
        transformacao.apply_negative()
        tk_image = transformacao.get_ctk_image(width=256, height=256)
            
        label_transformacao = ctk.CTkLabel(tabview.tab("Transformações"), image=tk_image, text="")
        label_transformacao.pack(side='left', padx=200); 
        print("Transformação Negativo aplicada a imagem exibida.")
    
    elif transformacao_selecionada == "Sigmoide":
        transformacao =  Sigmoide(caminho_imagem_selecionado_transformacoes)

        #centro dos valores de cinza, largura da janela para suavidade da transição
        transformacao.apply_sigmoide(128,30)
        tk_image = transformacao.get_ctk_image(width=256, height=256)
            
        label_transformacao = ctk.CTkLabel(tabview.tab("Transformações"), image=tk_image, text="")
        label_transformacao.pack(side='left', padx=200); 
        print("Transformação Sigmoide aplicada a imagem exibida.")

    else:
        print("Selecione uma transformação para aplicar.")


combobox_image_transformacao = ctk.CTkComboBox(
    container_frame_transformacao,
    values=["lena.pgm", "Lenag.pgm", "Airplane.pgm", "Lenasalp.pgm"],
    command=combobox_callback_image_transformacao,
    width=270,
    font=("Helvetica", 14),
)
combobox_image_transformacao.pack(side="left", padx=10, pady=10)

combobox_var_transformacao = ctk.StringVar(value="Escolha a Transformação")
combobox_transformacao = ctk.CTkComboBox(
    container_frame_transformacao,
    values=[
        "Faixa Dinâmica", "Gama", 
        "Logaritmica", "Negativo", 
        "Sigmoide"
    ],
    command=combobox_callback_transformacao,
    variable=combobox_var_transformacao,
    width=270,
    font=("Helvetica", 14),
)
combobox_transformacao.pack(side="left", padx=10, pady=10)

button_apply_transformacao = ctk.CTkButton(
    container_frame_transformacao,
    text="Aplicar Transformação",
    command=aplicar_transformacao
)
button_apply_transformacao.pack(side="left", padx=10, pady=10)


#********************************************************************************************************************
#HISTOGRAMA
#********************************************************************************************************************
# HEADER
container_frame_histograma = ctk.CTkFrame(tabview.tab("Histograma"))
container_frame_histograma.pack(padx=10, pady=10, fill="x")

# Frame superior dentro do container para exibir a imagem e o histograma lado a lado
frame_superior_histograma = ctk.CTkFrame(
    tabview.tab("Histograma"), width=1000, height=300, fg_color='#f3f3f3'
)
frame_superior_histograma.pack( fill="x")

# Frame para a imagem na parte esquerda do frame superior
frame_imagem = ctk.CTkFrame(
    frame_superior_histograma, width=500, height=300,  fg_color='#f3f3f3'
)
frame_imagem.pack(side="left", fill="both", expand=True)

# Frame para o histograma na parte direita do frame superior
frame_histograma = ctk.CTkFrame(
    frame_superior_histograma, width=500, height=300,  fg_color='#f3f3f3'
)
frame_histograma.pack(side="left", fill="both", expand=True)

# Frame inferior dentro do container para seleção de filtros e botões
frame_inferior_histograma = ctk.CTkFrame(
    tabview.tab("Histograma"), width=1000, height=300,  fg_color='#f3f3f3'
)
frame_inferior_histograma.pack( fill="x")


frame_imagem_inf = ctk.CTkFrame(
    frame_inferior_histograma, width=500, height=300,  fg_color='#f3f3f3'
)
frame_imagem_inf.pack(side="left", fill="both", expand=True)


frame_histograma_inf = ctk.CTkFrame(
    frame_inferior_histograma, width=500, height=300,  fg_color='#f3f3f3'
)
frame_histograma_inf.pack(side="left", fill="both", expand=True)

# Instância da Classe VisualizadorImagemCustomTk para visualizar a imagem
visualizador_histograma_eq = VisualizadorImagemCustomTk(frame_imagem, caminho_imagem)
visualizador_histograma_eq.exibir_img_histo(frame_imagem)

# Variáveis globais para manter seleção de filtro e caminho de imagem
caminho_imagem_selecionado_histograma = None
label_histograma = None
label_imagem_equalizada = None
label_histograma_equalizado = None

# Função chamada no Select das imagens
def combobox_callback_image_histograma(choice):
    global caminho_imagem_selecionado_histograma
    print("Combobox dropdown clicked imagem:", choice)
    caminho_imagem_selecionado_histograma = os.path.join(diretorio_imagens, choice)
    visualizador_histograma_eq.exibir_imagem_histo(caminho_imagem_selecionado_histograma)
    visualizador_histograma_eq.mostrar_histograma(frame_histograma)


def equalizar_imagem():
    global label_histograma, label_imagem_equalizada, label_histograma_equalizado, caminho_imagem_selecionado_histograma

    # Remove os widgets anteriores da imagem e do histograma equalizado, se existirem
    if label_imagem_equalizada is not None:
        label_imagem_equalizada.destroy()
    if label_histograma_equalizado is not None:
        label_histograma_equalizado.destroy()

    # Equaliza a imagem selecionada
    Equalizada = EqualizadorHistograma(caminho_imagem_selecionado_histograma)
    Equalizada.equalizar()
    tk_image_equalizada = Equalizada.get_ctk_image(width=256, height=256)

    # Exibe a imagem equalizada no frame inferior
    label_imagem_equalizada = ctk.CTkLabel(frame_imagem_inf, image=tk_image_equalizada, text="", bg_color='red')
    label_imagem_equalizada.pack(side='left', padx=200, pady=10)

    # Remover todos os widgets de histograma antes de exibir o novo
    for widget in frame_histograma_inf.winfo_children():
        widget.destroy()

    # Exibe o histograma da imagem equalizada
    Equalizada.mostrar_histograma_equalizado(frame_histograma_inf)
    print("Imagem Equalizada e Histograma exibidos")


# Combobox para selecionar a imagem
combobox_image_histograma = ctk.CTkComboBox(
    container_frame_histograma,
    values=["lena.pgm", "Lenag.pgm", "Airplane.pgm", "Lenasalp.pgm"],
    command=combobox_callback_image_histograma,
    width=270,
    font=("Helvetica", 14),
)
combobox_image_histograma.pack(side="left", padx=10, pady=10)

# Botão para aplicar equalização na imagem
button_apply_histograma = ctk.CTkButton(
    container_frame_histograma,
    text="Equalizar Imagem",
    command=equalizar_imagem
)
button_apply_histograma.pack(side="left", padx=10, pady=10)


#********************************************************************************************************************
#MORFOLOGIA
#********************************************************************************************************************

#HEADER
container_frame_morfologia = ctk.CTkFrame(tabview.tab("Morfologia"))
container_frame_morfologia.pack(padx=10, pady=10, fill="x")

#usando a instância da classe Visualizar Imagens para mostras a imagem na aba transformaçoes
#Instância da Classe 
visualizador_morfologia = VisualizadorImagemCustomTk(container_frame, caminho_imagem)
visualizador_morfologia.exibir(tabview.tab("Morfologia"))


# Variáveis globais para manter seleção de filtro e caminho de imagem
caminho_imagem_selecionado_morfologia = None
label_morfologia = None
morfologia_selecionada = None


# Função chamada no Select das imagens
def combobox_callback_image_morfologia(choice):
    global caminho_imagem_selecionado_morfologia
    print("Combobox dropdown clicked imagem:", choice)
    caminho_imagem_selecionado_morfologia = os.path.join(diretorio_imagens, choice)
    visualizador_morfologia.exibir_imagem(caminho_imagem_selecionado_morfologia)

def combobox_callback_morfologia(choice):
    global morfologia_selecionada
    print("Combobox dropdown clicked filtro:", choice)
    morfologia_selecionada = choice

def aplicar_morfologia():
    global morfologia_selecionada, caminho_imagem_selecionado_morfologia, label_morfologia  # Incluindo label como global

      
    if label_morfologia is not None:
       label_morfologia.destroy() 

    if morfologia_selecionada == "Dilatação":
        morfologia = Dilatacao(caminho_imagem_selecionado_morfologia)
        morfologia.apply_filter()
        tk_image = morfologia.get_ctk_image(width=256, height=256)

        label_morfologia = ctk.CTkLabel(tabview.tab("Morfologia"), image=tk_image, text="")
        label_morfologia.pack(side='left', padx=200)
        print("Morfologia de dilatação aplicado e imagem exibida.")
    elif morfologia_selecionada == "Erosão":
        morfologia = Erosao(caminho_imagem_selecionado_morfologia)
        morfologia.erodir()
        tk_image = morfologia.get_ctk_image(width=256, height=256)

        label_morfologia = ctk.CTkLabel(tabview.tab("Morfologia"), image=tk_image, text="")
        label_morfologia.pack(side='left', padx=200)
        print("Morfologia de erosao aplicado e imagem exibida.")

    elif morfologia_selecionada == "Fechamento":
        morfologia = Fechamento(caminho_imagem_selecionado_morfologia)
        morfologia.fechamento()
        tk_image = morfologia.get_ctk_image(width=256, height=256)

        label_morfologia = ctk.CTkLabel(tabview.tab("Morfologia"), image=tk_image, text="")
        label_morfologia.pack(side='left', padx=200)
        print("Morfologia de erosao aplicado e imagem exibida.")

    
    elif morfologia_selecionada == "Abertura":
        morfologia = Abertura(caminho_imagem_selecionado_morfologia)
        morfologia.abertura()
        tk_image = morfologia.get_ctk_image(width=256, height=256)

        label_morfologia = ctk.CTkLabel(tabview.tab("Morfologia"), image=tk_image, text="")
        label_morfologia.pack(side='left', padx=200)
        print("Morfologia de erosao aplicado e imagem exibida.")
    
    elif morfologia_selecionada == "Hit Or Miss":    
        morfologia = HitOrMiss(caminho_imagem_selecionado_morfologia)
        
        elemento_estruturante = np.ones((3, 3), dtype=np.uint8)
        
        morfologia.hit_or_miss(elemento_estruturante)
        
        tk_image = morfologia.get_ctk_image(width=256, height=256)
        
        label_morfologia = ctk.CTkLabel(tabview.tab("Morfologia"), image=tk_image, text="")
        label_morfologia.pack(side='left', padx=200)
        
        print("Morfologia de erosão aplicada e imagem exibida.")
    
    elif morfologia_selecionada == "Top Hat":
        morfologia = TopHat(caminho_imagem_selecionado_morfologia)
        morfologia.aplicar_top_hat()
        tk_image = morfologia.get_ctk_image(width=256, height=256)

        label_morfologia = ctk.CTkLabel(tabview.tab("Morfologia"), image=tk_image, text="")
        label_morfologia.pack(side='left', padx=200)
        print("Morfologia de erosao aplicado e imagem exibida.")

    elif morfologia_selecionada == "Bottom Hat":
        morfologia = BottomHat(caminho_imagem_selecionado_morfologia)
        morfologia.aplicar_bottom_hat()
        tk_image = morfologia.get_ctk_image(width=256, height=256)

        label_morfologia = ctk.CTkLabel(tabview.tab("Morfologia"), image=tk_image, text="")
        label_morfologia.pack(side='left', padx=200)
        print("Morfologia de erosao aplicado e imagem exibida.")

    else:
        print("Selecione uma morfologia para aplicar.")

combobox_image_morfologia = ctk.CTkComboBox(
    container_frame_morfologia,
    values=["lena.pgm", "Lenag.pgm", "Airplane.pgm", "Lenasalp.pgm"],
    command=combobox_callback_image_morfologia,
    width=270,
    font=("Helvetica", 14),
)
combobox_image_morfologia.pack(side="left", padx=10, pady=10)

combobox_var_morfologia = ctk.StringVar(value="Escolha a Morfologia")
combobox_morfologia = ctk.CTkComboBox(
    container_frame_morfologia,
    values=[
        "Dilatação", "Erosão", 
        "Fechamento", "Abertura", 
        "Hit Or Miss", "Top Hat", "Bottom Hat"
    ],
    command=combobox_callback_morfologia,
    variable=combobox_var_morfologia,
    width=270,
    font=("Helvetica", 14),
)
combobox_morfologia.pack(side="left", padx=10, pady=10)

button_apply_morfologia = ctk.CTkButton(
    container_frame_morfologia,
    text="Aplicar Transformação",
    command=aplicar_morfologia
)
button_apply_morfologia.pack(side="left", padx=10, pady=10)

#====================================================================================================================
# Inicia o loop da interface
#====================================================================================================================
janela.mainloop()
