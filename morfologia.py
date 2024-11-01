
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