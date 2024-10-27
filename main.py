import customtkinter as ctk


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
tabview.add("Negativo")
tabview.add("Histograma")
tabview.add("Morfologia")



#====================================================================================================================
# Adicionando Funcionandalidades Nas Abas
#====================================================================================================================

def combobox_callback(choice):
    print("Combobox dropdown clicked:", choice)

# Adicionando um ComboBox
combobox_var = ctk.StringVar(value="Escolha o Filtro")  # Valor padrão
combobox = ctk.CTkComboBox(
    tabview.tab("Filtros"),
    values=["Filtro de Suavização - média", "Filtro de Suavização - mediana", "Filtro Passa Alta Básico", "Filtro Operador de Robert", "Filtro Operador de Prewitt", "Filtro Operador de Prewitt - Magnitude", "Filtro de Alto Reforço", "Filtro Operador de Sobel"],
    command=combobox_callback,
    variable=combobox_var,
    width= 270,
    font=("Helvetica", 14),
    
)
combobox.grid(row=1, column=0, padx=10, pady=10, columnspan=2)  # Posiciona o ComboBox








#====================================================================================================================
# Inicia o loop da interface
#====================================================================================================================
janela.mainloop()
