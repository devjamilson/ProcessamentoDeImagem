import customtkinter as ctk
from PIL import Image
import numpy as np
from Imagem.visualizador_imagem import VisualizadorImagemCustomTk

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
tabview.pack(pady=10, padx=10, fill="both", expand=True)


# Adicionando as abas
tabview.add("Filtros")
tabview.add("Transformações")
tabview.add("Histograma")
tabview.add("Morfologia")



#====================================================================================================================
# Adicionando Funcionandalidades Nas Abas
#====================================================================================================================

#FILTROS
# Caminho da imagem PGM
caminho_imagem = r"C:\Users\jamil\OneDrive\Área de Trabalho\ProcessamentoImagem\Imagem\Utils\lena.pgm"

def combobox_callback(choice):
    print("Combobox dropdown clicked:", choice)

def combobox_callback_image(choice):
    print("Combobox dropdown clicked imagem:", choice)

# Frame container para a tab de Filtros
container_frame = ctk.CTkFrame(tabview.tab("Filtros"))
container_frame.pack(padx=40, pady=40, fill="x") 

# Visualizador da Imagem
visualizador = VisualizadorImagemCustomTk(container_frame, caminho_imagem)
visualizador.exibir(tabview.tab("Filtros"))

# Combobox para seleção de Imagem
combobox_var_image = ctk.StringVar(value="Escolha a Imagem")
combobox_image = ctk.CTkComboBox(
    container_frame,
    values=["lena.pgm", "Lenag.pgm", "Airplane.pgm", "Lenasalp.pgm"],
    command=combobox_callback_image,
    variable=combobox_var_image,
    width=270,
    font=("Helvetica", 14),
)
combobox_image.pack(side="left", padx=10, pady=10)

# Combobox para seleção de Filtro
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

# Botão para aplicar o filtro ou ação
button_apply = ctk.CTkButton(
    container_frame,
    text="Aplicar Filtro",
    command=lambda: print("Botão Aplicar Filtro clicado")
)
button_apply.pack(side="left", padx=10, pady=10)






#====================================================================================================================
# Inicia o loop da interface
#====================================================================================================================
janela.mainloop()
