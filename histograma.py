


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