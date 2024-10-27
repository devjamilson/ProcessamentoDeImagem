import customtkinter as ctk

janela = ctk.CTk()

# Configurando a estrutura da janela
janela.title('Projeto de Processamento de Imagens')
janela.geometry('1350x690')
janela.geometry("+0+0")  
#bloqueia o redimensionamento
janela.resizable(width=False, height=False)
janela.attributes('-topmost', True)

#componente frame para executar as funções do tab view
#frame1 = ctk.CTkFrame(master=janela, width=1100, height=690, fg_color="white").place(x=250, y=0)
#frame2 = ctk.CTkFrame(janela, width=250, height=690).place(x=0, y=0)



#Abas
tabview = ctk.CTkTabview(janela, width=1000, height=650)
tabview.pack()
tabview.add("Filtros")
tabview.add("Negativo")
tabview.add("Histograma")
tabview.add("Morfologia")
tabview.tab("Filtros").grid_columnconfigure(0, weight=1)
tabview.tab("Negativo").grid_columnconfigure(0, weight=1)
tabview.tab("Histograma").grid_columnconfigure(0, weight=1)
tabview.tab("Morfologia").grid_columnconfigure(0, weight=1)


#Adicionando Elementos na Tab



# Inicia o loop da interface
janela.mainloop()
