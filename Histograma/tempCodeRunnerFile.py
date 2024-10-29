def carregar_imagem_pgm(caminho_imagem):
    """Carrega uma imagem PGM (P2 ou P5) e retorna como um array numpy."""
    if not os.path.exists(caminho_imagem):
        raise FileNotFoundError(f"O arquivo não foi encontrado: {caminho_imagem}")

    with open(caminho_imagem, 'rb') as f:
        header = f.readline().strip()
        
        # Verifica o formato (P2 para ASCII, P5 para binário)
        if header == b'P5':
            # Formato binário
            width, height = map(int, f.readline().split())
            maxval = int(f.readline().strip())
            
            # Carrega a imagem em escala de cinza
            imagem_data = np.fromfile(f, dtype=np.uint8 if maxval < 256 else np.uint16)
            imagem = imagem_data.reshape((height, width))
        
        elif header == b'P2':
            # Formato ASCII
            width, height = map(int, f.readline().split())
            maxval = int(f.readline().strip())
            
            # Carrega a imagem linha por linha em escala de cinza
            imagem_data = []
            for line in f:
                imagem_data.extend(map(int, line.split()))
            imagem = np.array(imagem_data, dtype=np.uint8).reshape((height, width))
        
        else:
            raise ValueError("Formato PGM não suportado (esperado P2 ou P5).")

    return imagem