import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

usuarios = [
    {
        "id": 1,
        "nome": "usuario",
        "senha": "123456",
        "perfil": "usuario",
    },
    {
        "id": 2,
        "nome": "prefeitura",
        "senha": "123456",
        "perfil": "prefeitura",
    },
]

denuncias = []

usuario_logado = None
caminho_foto = ""
denuncias_visiveis = []
minhas_denuncias_lista = []


def limpar_tela():
    for item in area_principal.winfo_children():
        item.destroy()


def criar_cabecalho():
    topo = tk.Frame(area_principal, bg="#0077b6", padx=20, pady=12)
    topo.pack(fill="x")

    tk.Label(
        topo,
        text="Agua Viva - Saneamento e Preservacao",
        font=("Arial", 14, "bold"),
        bg="#0077b6",
        fg="white",
    ).pack(side="left")

    if usuario_logado["perfil"] == "prefeitura":
        texto_perfil = f"{usuario_logado['nome']} (Gestor)"
    else:
        texto_perfil = f"Logado como: {usuario_logado['nome']}"

    tk.Label(
        topo,
        text=texto_perfil,
        font=("Arial", 10, "bold"),
        bg="#023e8a",
        fg="white",
        padx=10,
        pady=4,
    ).pack(side="right")

    menu = tk.Frame(area_principal, bg="#e0f2fe", padx=20, pady=8)
    menu.pack(fill="x")

    tk.Button(menu, text="Ver denuncias", command=mostrar_feed, width=15).pack(side="left", padx=4)

    if usuario_logado["perfil"] == "usuario":
        tk.Button(menu, text="Nova denuncia", command=mostrar_nova_denuncia, width=15).pack(side="left", padx=4)

    tk.Button(menu, text="Meu perfil", command=mostrar_perfil, width=15).pack(side="left", padx=4)
    tk.Button(menu, text="Sair", command=sair, width=10).pack(side="right", padx=4)


def mostrar_login():
    limpar_tela()

    caixa = tk.Frame(area_principal, bg="white", padx=30, pady=25, bd=1, relief="solid")
    caixa.place(relx=0.5, rely=0.5, anchor="center", width=380)

    tk.Label(caixa, text="Agua Viva", font=("Arial", 16, "bold"), bg="white", fg="#0077b6").pack()
    tk.Label(caixa, text="Escolha um perfil ou digite seu login", font=("Arial", 10), bg="white", fg="#555555").pack(pady=(0, 12))

    atalhos = tk.Frame(caixa, bg="white")
    atalhos.pack(fill="x", pady=(0, 12))

    tk.Label(caixa, text="Usuario:", bg="white", anchor="w").pack(fill="x")
    campo_usuario = tk.Entry(caixa, font=("Arial", 10))
    campo_usuario.insert(0, "usuario")
    campo_usuario.pack(fill="x", pady=(2, 10))

    tk.Label(caixa, text="Senha:", bg="white", anchor="w").pack(fill="x")
    campo_senha = tk.Entry(caixa, font=("Arial", 10), show="*")
    campo_senha.insert(0, "123456")
    campo_senha.pack(fill="x", pady=(2, 15))

    def preencher_usuario():
        campo_usuario.delete(0, tk.END)
        campo_usuario.insert(0, "usuario")
        campo_senha.delete(0, tk.END)
        campo_senha.insert(0, "123456")

    def preencher_prefeitura():
        campo_usuario.delete(0, tk.END)
        campo_usuario.insert(0, "prefeitura")
        campo_senha.delete(0, tk.END)
        campo_senha.insert(0, "123456")

    tk.Button(atalhos, text="Usuario", command=preencher_usuario).pack(side="left", expand=True, fill="x", padx=(0, 4))
    tk.Button(atalhos, text="Prefeitura", command=preencher_prefeitura).pack(side="left", expand=True, fill="x", padx=(4, 0))

    def entrar():
        global usuario_logado
        nome_digitado = campo_usuario.get().strip().lower()
        senha_digitada = campo_senha.get().strip()

        for user in usuarios:
            if user["nome"].lower() == nome_digitado and user["senha"] == senha_digitada:
                usuario_logado = user
                mostrar_feed()
                return

        messagebox.showerror("Erro", "Usuario ou senha incorretos.")

    tk.Button(
        caixa,
        text="Entrar",
        command=entrar,
        bg="#0077b6",
        fg="white",
        font=("Arial", 10, "bold"),
        pady=6,
    ).pack(fill="x")


def sair():
    global usuario_logado
    usuario_logado = None
    mostrar_login()


def mostrar_feed():
    limpar_tela()
    criar_cabecalho()

    corpo = tk.Frame(area_principal, bg="#f4f6f9", padx=20, pady=15)
    corpo.pack(fill="both", expand=True)

    barra_filtro = tk.Frame(corpo, bg="#f4f6f9")
    barra_filtro.pack(fill="x", pady=(0, 10))

    titulo = "Painel da Prefeitura" if usuario_logado["perfil"] == "prefeitura" else "Denuncias registradas"
    tk.Label(barra_filtro, text=titulo, font=("Arial", 13, "bold"), bg="#f4f6f9").pack(side="left")

    filtro = ttk.Combobox(
        barra_filtro,
        values=["Todas", "Vazamento de agua", "Esgoto a ceu aberto", "Agua parada", "Falta de agua"],
        state="readonly",
        width=24,
    )
    filtro.current(0)
    filtro.pack(side="right")

    lista = tk.Listbox(corpo, height=9, font=("Arial", 10))
    lista.pack(fill="x", pady=(0, 10))

    painel_detalhes = tk.Frame(corpo, bg="white", padx=15, pady=15, bd=1, relief="solid")
    painel_detalhes.pack(fill="both", expand=True)

    texto_detalhe = tk.Label(
        painel_detalhes,
        text="",
        font=("Arial", 10),
        bg="white",
        justify="left",
        anchor="nw",
        wraplength=760,
    )
    texto_detalhe.pack(fill="both", expand=True)

    barra_usuario = tk.Frame(painel_detalhes, bg="white")
    barra_prefeitura = tk.Frame(painel_detalhes, bg="white")

    def carregar_lista(evento=None):
        global denuncias_visiveis
        lista.delete(0, tk.END)
        barra_usuario.pack_forget()
        barra_prefeitura.pack_forget()

        categoria = filtro.get()
        if categoria == "Todas":
            denuncias_visiveis = list(denuncias)
        else:
            denuncias_visiveis = [d for d in denuncias if d["tipo"] == categoria]

        if not denuncias_visiveis:
            lista.insert(tk.END, "Nenhuma denuncia registrada ainda.")
            if usuario_logado["perfil"] == "usuario":
                texto_detalhe.config(text="A lista esta vazia. Clique em 'Nova denuncia' no menu acima para criar a primeira.")
            else:
                texto_detalhe.config(text="Nenhuma denuncia recebida ate o momento.")
            return

        texto_detalhe.config(text="Clique em uma denuncia na lista acima para ver os detalhes.")
        for item in denuncias_visiveis:
            linha = f"[{item['status']}] {item['tipo']} - {item['local']} (por {item['autor']})"
            lista.insert(tk.END, linha)

    def selecionar_item(evento):
        if not denuncias_visiveis:
            return

        selecao = lista.curselection()
        if not selecao:
            return

        item = denuncias_visiveis[selecao[0]]
        nome_foto = os.path.basename(item["foto"]) if item["foto"] else "Nenhuma foto anexada"

        resumo = (
            f"Status atual: {item['status']}\n"
            f"Problema: {item['tipo']}\n"
            f"Local: {item['local']}\n"
            f"Registrado por: {item['autor']}\n"
            f"Foto: {nome_foto}\n\n"
            f"Descricao:\n{item['descricao']}"
        )
        texto_detalhe.config(text=resumo)

        barra_usuario.pack_forget()
        barra_prefeitura.pack_forget()

        if usuario_logado["perfil"] == "prefeitura":
            barra_prefeitura.pack(anchor="w", pady=(10, 0))
        elif item["autor_id"] == usuario_logado["id"]:
            barra_usuario.pack(anchor="w", pady=(10, 0))

    def mudar_status(novo_status):
        selecao = lista.curselection()
        if not selecao or not denuncias_visiveis:
            return
        item = denuncias_visiveis[selecao[0]]
        item["status"] = novo_status
        messagebox.showinfo("Atualizado", f"Status alterado para: {novo_status}")
        carregar_lista()

    def editar_selecionada():
        selecao = lista.curselection()
        if not selecao or not denuncias_visiveis:
            return
        item = denuncias_visiveis[selecao[0]]

        janela_edicao = tk.Toplevel(janela)
        janela_edicao.title("Editar denuncia")
        janela_edicao.geometry("400x200")

        tk.Label(janela_edicao, text="Nova descricao:", font=("Arial", 10, "bold")).pack(anchor="w", padx=15, pady=(15, 5))
        caixa_texto = tk.Text(janela_edicao, height=5, font=("Arial", 10))
        caixa_texto.insert("1.0", item["descricao"])
        caixa_texto.pack(fill="x", padx=15)

        def salvar():
            novo_texto = caixa_texto.get("1.0", "end").strip()
            if novo_texto:
                item["descricao"] = novo_texto
                janela_edicao.destroy()
                carregar_lista()

        tk.Button(janela_edicao, text="Salvar", command=salvar, bg="#0077b6", fg="white").pack(pady=10)

    def excluir_selecionada():
        selecao = lista.curselection()
        if not selecao or not denuncias_visiveis:
            return
        item = denuncias_visiveis[selecao[0]]

        if messagebox.askyesno("Confirmar", "Deseja apagar essa denuncia?"):
            denuncias.remove(item)
            carregar_lista()

    tk.Button(barra_usuario, text="Editar descricao", command=editar_selecionada).pack(side="left", padx=(0, 8))
    tk.Button(barra_usuario, text="Excluir denuncia", command=excluir_selecionada).pack(side="left")

    tk.Button(
        barra_prefeitura,
        text="Marcar como Em analise",
        command=lambda: mudar_status("Em analise"),
        bg="#f59e0b",
        fg="white",
    ).pack(side="left", padx=(0, 8))
    tk.Button(
        barra_prefeitura,
        text="Marcar como Resolvido",
        command=lambda: mudar_status("Resolvido"),
        bg="#16a34a",
        fg="white",
    ).pack(side="left")

    filtro.bind("<<ComboboxSelected>>", carregar_lista)
    lista.bind("<<ListboxSelect>>", selecionar_item)
    carregar_lista()


def mostrar_nova_denuncia():
    global caminho_foto
    caminho_foto = ""
    limpar_tela()
    criar_cabecalho()

    corpo = tk.Frame(area_principal, bg="#f4f6f9", padx=20, pady=15)
    corpo.pack(fill="both", expand=True)

    form = tk.Frame(corpo, bg="white", padx=25, pady=20, bd=1, relief="solid")
    form.pack(fill="both", expand=True)

    tk.Label(form, text="Registrar nova denuncia", font=("Arial", 13, "bold"), bg="white").pack(anchor="w", pady=(0, 12))

    tk.Label(form, text="Local do problema:", bg="white", font=("Arial", 10, "bold")).pack(anchor="w")
    campo_local = tk.Entry(form, font=("Arial", 10))
    campo_local.pack(fill="x", pady=(2, 10))

    tk.Label(form, text="Tipo de ocorrencia:", bg="white", font=("Arial", 10, "bold")).pack(anchor="w")
    campo_tipo = ttk.Combobox(
        form,
        values=["Vazamento de agua", "Esgoto a ceu aberto", "Agua parada", "Falta de agua"],
        state="readonly",
        font=("Arial", 10),
    )
    campo_tipo.current(0)
    campo_tipo.pack(fill="x", pady=(2, 10))

    linha_foto = tk.Frame(form, bg="white")
    linha_foto.pack(fill="x", pady=(0, 10))
    label_foto = tk.Label(linha_foto, text="Nenhuma imagem selecionada", bg="white", fg="#555555")

    def escolher_imagem():
        global caminho_foto
        arquivo = filedialog.askopenfilename(
            title="Escolha uma foto",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png")],
        )
        if arquivo:
            caminho_foto = arquivo
            label_foto.config(text=os.path.basename(arquivo), fg="#0077b6")

    tk.Button(linha_foto, text="Anexar foto", command=escolher_imagem).pack(side="left")
    label_foto.pack(side="left", padx=10)

    tk.Label(form, text="Descricao do problema:", bg="white", font=("Arial", 10, "bold")).pack(anchor="w")
    campo_descricao = tk.Text(form, height=5, font=("Arial", 10), bd=1, relief="solid")
    campo_descricao.pack(fill="x", pady=(2, 15))

    def enviar():
        local = campo_local.get().strip()
        descricao = campo_descricao.get("1.0", "end").strip()

        if not local or not descricao:
            messagebox.showwarning("Atencao", "Preencha o local e a descricao antes de enviar.")
            return

        novo_id = max([d["id"] for d in denuncias], default=0) + 1
        nova = {
            "id": novo_id,
            "autor_id": usuario_logado["id"],
            "autor": usuario_logado["nome"],
            "local": local,
            "tipo": campo_tipo.get(),
            "descricao": descricao,
            "foto": caminho_foto,
            "status": "Pendente",
        }
        denuncias.insert(0, nova)

        messagebox.showinfo("Sucesso", "Denuncia registrada com sucesso!")
        mostrar_feed()

    tk.Button(
        form,
        text="Enviar denuncia",
        command=enviar,
        bg="#0077b6",
        fg="white",
        font=("Arial", 10, "bold"),
        pady=6,
    ).pack(side="left", padx=(0, 10))

    tk.Button(form, text="Cancelar", command=mostrar_feed, pady=6).pack(side="left")


def mostrar_perfil():
    global minhas_denuncias_lista
    limpar_tela()
    criar_cabecalho()

    corpo = tk.Frame(area_principal, bg="#f4f6f9", padx=20, pady=15)
    corpo.pack(fill="both", expand=True)

    # Bloco superior com os dados da conta
    caixa_perfil = tk.Frame(corpo, bg="white", padx=20, pady=15, bd=1, relief="solid")
    caixa_perfil.pack(fill="x", pady=(0, 12))

    tk.Label(caixa_perfil, text="Meu perfil", font=("Arial", 13, "bold"), bg="white", fg="#0077b6").pack(anchor="w")

    tipo_conta = "Gestor Municipal" if usuario_logado["perfil"] == "prefeitura" else "Cidadao"
    tk.Label(caixa_perfil, text=f"Tipo de acesso: {tipo_conta}", font=("Arial", 10), bg="white", fg="#555555").pack(anchor="w", pady=(2, 8))

    linha_nome = tk.Frame(caixa_perfil, bg="white")
    linha_nome.pack(fill="x")

    tk.Label(linha_nome, text="Nome:", font=("Arial", 10, "bold"), bg="white").pack(side="left")
    campo_nome = tk.Entry(linha_nome, font=("Arial", 10), width=30)
    campo_nome.insert(0, usuario_logado["nome"])
    campo_nome.pack(side="left", padx=8)

    def salvar_nome():
        novo_nome = campo_nome.get().strip()
        if not novo_nome:
            messagebox.showwarning("Atencao", "O nome nao pode ficar em branco.")
            return
        usuario_logado["nome"] = novo_nome
        for item in denuncias:
            if item["autor_id"] == usuario_logado["id"]:
                item["autor"] = novo_nome
        messagebox.showinfo("Pronto", "Nome atualizado com sucesso!")
        mostrar_perfil()

    tk.Button(linha_nome, text="Salvar nome", command=salvar_nome, bg="#0077b6", fg="white").pack(side="left")

    # Se for a prefeitura, mostra um resumo geral dos atendimentos
    if usuario_logado["perfil"] == "prefeitura":
        caixa_resumo = tk.Frame(corpo, bg="white", padx=20, pady=20, bd=1, relief="solid")
        caixa_resumo.pack(fill="both", expand=True)

        pendentes = len([d for d in denuncias if d["status"] == "Pendente"])
        em_analise = len([d for d in denuncias if d["status"] == "Em analise"])
        resolvidas = len([d for d in denuncias if d["status"] == "Resolvido"])

        tk.Label(caixa_resumo, text="Resumo das ocorrencias no sistema", font=("Arial", 12, "bold"), bg="white").pack(anchor="w", pady=(0, 10))
        tk.Label(caixa_resumo, text=f"Total recebidas: {len(denuncias)}", font=("Arial", 10), bg="white").pack(anchor="w", pady=2)
        tk.Label(caixa_resumo, text=f"Pendentes: {pendentes}", font=("Arial", 10), bg="white").pack(anchor="w", pady=2)
        tk.Label(caixa_resumo, text=f"Em analise: {em_analise}", font=("Arial", 10), bg="white").pack(anchor="w", pady=2)
        tk.Label(caixa_resumo, text=f"Resolvidas: {resolvidas}", font=("Arial", 10), bg="white").pack(anchor="w", pady=2)
        return

    # Se for usuario padrao, mostra a lista exclusiva das denuncias dele
    minhas_denuncias_lista = [d for d in denuncias if d["autor_id"] == usuario_logado["id"]]

    caixa_minhas = tk.Frame(corpo, bg="white", padx=20, pady=15, bd=1, relief="solid")
    caixa_minhas.pack(fill="both", expand=True)

    tk.Label(
        caixa_minhas,
        text=f"Minhas denuncias ({len(minhas_denuncias_lista)})",
        font=("Arial", 12, "bold"),
        bg="white",
    ).pack(anchor="w", pady=(0, 8))

    lista_minhas = tk.Listbox(caixa_minhas, height=6, font=("Arial", 10))
    lista_minhas.pack(fill="x", pady=(0, 8))

    detalhe_minha = tk.Label(
        caixa_minhas,
        text="",
        font=("Arial", 10),
        bg="#f8fafc",
        padx=10,
        pady=10,
        justify="left",
        anchor="nw",
        wraplength=740,
    )
    detalhe_minha.pack(fill="both", expand=True)

    barra_botoes = tk.Frame(caixa_minhas, bg="white")

    if not minhas_denuncias_lista:
        lista_minhas.insert(tk.END, "Voce ainda nao registrou nenhuma denuncia.")
        detalhe_minha.config(text="Clique em 'Nova denuncia' no menu superior para enviar seu primeiro relato.")
        return

    detalhe_minha.config(text="Selecione uma das suas denuncias acima para ver detalhes, editar ou excluir.")
    for item in minhas_denuncias_lista:
        lista_minhas.insert(tk.END, f"[{item['status']}] {item['tipo']} - {item['local']}")

    def ao_selecionar(evento):
        selecao = lista_minhas.curselection()
        if not selecao:
            return
        item = minhas_denuncias_lista[selecao[0]]
        nome_foto = os.path.basename(item["foto"]) if item["foto"] else "Nenhuma foto anexada"
        detalhe_minha.config(
            text=(
                f"Status: {item['status']} | Problema: {item['tipo']}\n"
                f"Local: {item['local']} | Foto: {nome_foto}\n"
                f"Descricao: {item['descricao']}"
            )
        )
        barra_botoes.pack(anchor="w", pady=(8, 0))

    def editar_minha():
        selecao = lista_minhas.curselection()
        if not selecao:
            return
        item = minhas_denuncias_lista[selecao[0]]

        janela_edicao = tk.Toplevel(janela)
        janela_edicao.title("Editar minha denuncia")
        janela_edicao.geometry("400x200")

        tk.Label(janela_edicao, text="Nova descricao:", font=("Arial", 10, "bold")).pack(anchor="w", padx=15, pady=(15, 5))
        caixa_texto = tk.Text(janela_edicao, height=5, font=("Arial", 10))
        caixa_texto.insert("1.0", item["descricao"])
        caixa_texto.pack(fill="x", padx=15)

        def salvar():
            novo_texto = caixa_texto.get("1.0", "end").strip()
            if novo_texto:
                item["descricao"] = novo_texto
                janela_edicao.destroy()
                mostrar_perfil()

        tk.Button(janela_edicao, text="Salvar", command=salvar, bg="#0077b6", fg="white").pack(pady=10)

    def excluir_minha():
        selecao = lista_minhas.curselection()
        if not selecao:
            return
        item = minhas_denuncias_lista[selecao[0]]

        if messagebox.askyesno("Confirmar", "Deseja apagar essa denuncia?"):
            denuncias.remove(item)
            mostrar_perfil()

    tk.Button(barra_botoes, text="Editar descricao", command=editar_minha).pack(side="left", padx=(0, 8))
    tk.Button(barra_botoes, text="Excluir denuncia", command=excluir_minha).pack(side="left")

    lista_minhas.bind("<<ListboxSelect>>", ao_selecionar)


janela = tk.Tk()
janela.title("Agua Viva")
janela.geometry("820x580")

area_principal = tk.Frame(janela, bg="#f4f6f9")
area_principal.pack(fill="both", expand=True)

mostrar_login()
janela.mainloop()