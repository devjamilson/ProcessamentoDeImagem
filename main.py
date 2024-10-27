import customtkinter as ctk

janela = ctk.CTk()

# Configurando a estrutura da janela
janela.title('Projeto de Processamento de Imagens')
janela.geometry('1350x690')
janela.geometry("+0+0")  
#bloqueia o redimensionamento
janela.resizable(width=False, height=False)
janela.attributes('-topmost', True)

#componente frame para executar as funções dos buttons
frame1 = ctk.CTkFrame(master=janela, width=1100, height=690).place(x=250, y=0)

frame2 = ctk.CTkFrame(janela, width=200, height=690).place(x=0, y=0)

# Inicia o loop da interface
janela.mainloop()
