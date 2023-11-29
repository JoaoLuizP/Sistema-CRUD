import PySimpleGUI as sg
from sqlalchemy import create_engine
from time import sleep  
import pandas as pd
import psycopg2

listas_tp_produtos = ['Eletrônico', 'Alimentício', 'Vestuário', 'Saúde e Beleza', 'Outros', 'Decoração', 'Bebidas']
for i in range(len(listas_tp_produtos) - 1):
    for j in range(len(listas_tp_produtos) - i - 1):
        if listas_tp_produtos[j] > listas_tp_produtos[j + 1]:
            listas_tp_produtos[j], listas_tp_produtos[j + 1] = listas_tp_produtos[j + 1], listas_tp_produtos[j]
lista_quantidade = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

local_db = psycopg2.connect(
    user="postgres",
    password="Santos010802.",
    host="localhost",
    port="5432",
    database="postgres")





class Produto:
    def __init__(self, id_produto, nome_produto, tipo_produto, quantidade, valor_produto):
        self.id_produto = id_produto
        self.nome_produto = nome_produto
        self.tipo_produto = tipo_produto
        self.quantidade = quantidade
        self.valor_produto = valor_produto
        self.valor_final = int(self.quantidade) * float(self.valor_produto)

    def calcular_valor_total(self):
        return int(self.quantidade) * self.valor_produto
    




class Database:

    def __init__(self):
        self.engine_local = None

    def conexao_db(self)-> None:
        for rec in range(3):
            try:
                self.engine_local = create_engine('postgresql://postgres:Santos010802.@localhost:5432')
            except Exception as e:
                print(f"\nError:>>> Tentativa {rec} de reconexão")
                sleep(3)
                continue
            return self.engine_local






class SistemaCRUD:
    def __init__(self):
        self.produtos = []
        self.connection = Database().conexao_db()

    def incluir_produto(self, produto):
        self.produtos.append(produto)
        query = self.connection.execute(f"""INSERT INTO public.projeto_crud (id_produto, nome_produto, tipo_produto, quantidade, preco_produto, valor_total) 
                                         VALUES ({produto.id_produto}, '{produto.nome_produto}', '{produto.tipo_produto}', 
                                         {produto.quantidade}, {produto.valor_produto}, {produto.valor_final})""")
        #connection.commit()

    def consultar_produto(self, id_produto):
        query = self.connection.execute(f"SELECT * FROM public.projeto_crud WHERE id_produto = '{id_produto}' ")
        produto = query.first()
        if produto:
            return produto
        return None
        #for produto in self.produtos:
        #     if produto.id_produto == id_produto:
        #       return produto
        #return None

    def alterar_produto(self, id_produto, novo_produto):
        query = self.connection.execute(f"""UPDATE public.projeto_crud SET nome_produto = '{novo_produto.nome_produto}', 
                                   tipo_produto = '{novo_produto.tipo_produto}', quantidade = {novo_produto.quantidade}, 
                                   preco_produto = {novo_produto.valor_produto}, valor_total = {novo_produto.quantidade*novo_produto.valor_produto}
                                   WHERE id_produto = '{id_produto}' """)
        #for i, produto in enumerate(self.produtos):
        #    if produto.id_produto == id_produto:
        #        self.produtos[i] = novo_produto
        #        break

    def excluir_produto(self, id_produto):
        query = self.connection.execute(f"DELETE FROM public.projeto_crud WHERE id_produto = '{id_produto}' ")
        #self.produtos = [produto for produto in self.produtos if produto.id_produto != id_produto]

    def obter_lista_produtos(self):
        query = self.connection.execute(f"SELECT * FROM public.projeto_crud")
        lista_produtos = []
        for produto in query:
            lista_produtos.append(Produto(produto[0], produto[1], produto[2], produto[3], produto[4]))
        return lista_produtos
    




# Função para criar a interface gráficadef criar_layout():
def criar_layout():    
    botoes_layout = [
        sg.Button("Incluir Produto", font=('Calibri', 11, 'bold'), pad=((0, 10), 5), key='-INCLUIR-'),
        sg.Button("Consultar Produto", font=('Calibri', 11, 'bold'), pad=((0, 10), 5), key='-CONSULTAR-'),
        sg.Button("Alterar Produto", font=('Calibri', 11, 'bold'), pad=((0, 10), 5), key='-ALTERAR-'),
        sg.Button("Excluir Produto", font=('Calibri', 11, 'bold'), pad=((0, 10), 5), key='-EXCLUIR-'),
        sg.Button("Listar Produtos", font=('Calibri', 11, 'bold'), pad=((0, 10), 5), key='-LISTAR-'),
    ]

    tabela_layout = [
        [sg.Table(values=[], headings=["ID", "Nome", "Tipo", "Quantidade", "Valor Produto", "Total"],
                  auto_size_columns=False, justification='center',
                  key='-TABLE-', enable_events=True, bind_return_key=True,
                  font=('Calibri', 11, 'bold'),  # Especificando a fonte para as colunas
                  )],
    ]
    
    botao_atualizar = [
        sg.Button("Atualizar tabela", font=('Calibri', 9, 'bold'), pad=((0, 5), 5), key='-ATT-')
    ]

    linha_separadora = [sg.Text('-' * 500, size=(70, 1), justification='center')]

    layout = [
        botoes_layout,
        linha_separadora,  
       #[sg.HSeparator, sg.Text("", size=(15, 1))], # Adicionando um espaço vertical entre os botões e a tabela
        tabela_layout,
        [botao_atualizar]
    ]

    return layout







# Função para mostrar a janela principal
def mostrar_janela(layout):
    window = sg.Window("CRUD - Produtos", layout, icon=r'projeto_crud\crud.ico')

    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED:
            break
        elif event == "Incluir Produto" or event == '-INCLUIR-':
            # Implementar a lógica de inclusão aqui
            incluir_produto()
            atualizar_tabela(window)
        elif event == "Consultar Produto" or event == '-CONSULTAR-':
            # Implementar a lógica de consulta aqui
            consultar_produto()
        elif event == "Alterar Produto" or event == '-ALTERAR-':
            # Implementar a lógica de alteração aqui
            alterar_produto()
            atualizar_tabela(window)
        elif event == "Excluir Produto" or event == '-EXCLUIR-':
            # Implementar a lógica de exclusão aqui
            excluir_produto()
            atualizar_tabela(window)
        elif event == "Listar Produtos" or event == '-LISTAR-':
            # Implementar a lógica de listagem aqui
            listar_produtos()
        else:
            atualizar_tabela(window)

    window.close()






# Função para atualizar a tabela
def atualizar_tabela(window):
    lista_produtos = sistema.obter_lista_produtos()
    table_data = [[produto.id_produto, produto.nome_produto, produto.tipo_produto,
                   produto.quantidade, produto.valor_produto, produto.valor_final] for produto in lista_produtos]
    window['-TABLE-'].update(values=table_data)









# Função para implementar a lógica de inclusão
def incluir_produto():
    layout_popup = [
        [sg.Text("ID do Produto:", font=('Calibri', 11, 'italic', 'bold')), sg.Input(key='id_produto', font=('Calibri', 10), size=(35, 1))],
        [sg.Text("Nome do Produto:", font=('Calibri', 11, 'italic', 'bold')), sg.Input(key='nome_produto', font=('Calibri', 10), size=(35, 1))],
        [sg.Text("Tipo do Produto:", font=('Calibri', 11, 'italic', 'bold')), sg.InputCombo(listas_tp_produtos, key='tipo_produto', font=('Calibri', 10), size=(35, 1))],
        [sg.Text("Quantidade:", font=('Calibri', 11, 'italic', 'bold')), sg.InputCombo(lista_quantidade, key='quantidade', font=('Calibri', 10), size=(35, 1))],
        [sg.Text("Valor do Produto:", font=('Calibri', 11, 'italic', 'bold')), sg.Input(key='valor_produto_str', font=('Calibri', 10), size=(35, 1))],
        [sg.Button('OK', font=('Calibri', 10, 'italic', 'bold'), pad=((0, 10), 5)), sg.Button('Cancelar', font=('Calibri', 10, 'italic', 'bold'), pad=((0, 10), 5))]
    ]

    window_popup = sg.Window('Incluir Produto', layout_popup, icon=r'projeto_crud\create.ico')

    while True:
        event, values = window_popup.read()

        if event == sg.WIN_CLOSED or event == 'Cancelar':
            break
        elif event == 'OK':
            id_produto = values['id_produto']
            nome_produto = values['nome_produto']
            tipo_produto = values['tipo_produto']
            quantidade = values['quantidade']
            valor_produto_str = values['valor_produto_str']

            try:
                valor_produto = float(valor_produto_str.replace(',', '.'))
            except ValueError:
                sg.popup_error("Valor do produto inválido. Certifique-se de usar um formato numérico correto.", title="Erro cadastro", 
                               font=('Calibri', 10, 'italic', 'bold'), icon=r'projeto_crud\error.ico')
                continue

            novo_produto = Produto(id_produto, nome_produto, tipo_produto, int(quantidade), int(valor_produto))
            sistema.incluir_produto(novo_produto)

            window_popup.close()
            break

    window_popup.close()







# Função para implementar a lógica de consulta
def consultar_produto():
    layout_popup = [
        [sg.Text("Informe o ID do produto a ser consultado", font=('Calibri', 11, 'italic', 'bold'))],
        [sg.Input(key='id_produto', font=('Calibri', 10))],
        [sg.Button('Consultar', pad=((0, 10), 5)), sg.Button('Cancelar', pad=((0, 10), 5))]
    ]

    window_popup = sg.Window('Consultar Produto', layout_popup, icon=r'projeto_crud\read.ico')

    while True:
        event, values = window_popup.read()

        if event == sg.WIN_CLOSED or event == 'Cancelar':
            break
        elif event == 'Consultar':
            id_produto = values['id_produto']
            produto = sistema.consultar_produto(id_produto)

            if produto:
                # Modificação do layout principal para mostrar as informações do produto
                layout_expandido = [
                    [sg.Text(f"ID: {produto.id_produto}", font=('Calibri', 10, 'italic', 'bold'))],
                    [sg.Text(f"Nome: {produto.nome_produto}", font=('Calibri', 10, 'italic', 'bold'))],
                    [sg.Text(f"Tipo: {produto.tipo_produto}", font=('Calibri', 10, 'italic', 'bold'))],
                    [sg.Text(f"Quantidade: {produto.quantidade}", font=('Calibri', 10, 'italic', 'bold'))],
                    [sg.Text(f"Preço do produto: {produto.preco_produto}", font=('Calibri', 10, 'italic', 'bold'))],
                    [sg.Text(f"Valor total: {produto.valor_total}", font=('Calibri', 10, 'italic', 'bold'))],
                ]

                window_expandido = sg.Window(f'Produto {produto.nome_produto}', layout_expandido, size=(320, 180), icon=r'projeto_crud\read.ico')
                while True:
                    event_expandido, _ = window_expandido.read()

                    if event_expandido == sg.WIN_CLOSED or event_expandido == 'OK':
                        break
                window_expandido.close()

            else:
                sg.popup_error("Produto não encontrado.", title="Consulta de Produto", font=('Calibri', 10, 'italic', 'bold'), icon=r'projeto_crud\error.ico')

            break  # Encerra o loop após a consulta

    window_popup.close()




# Função para implementar a lógica de alteração
def alterar_produto():
    layout_popup = [
        [sg.Text("Informe o ID do produto a ser alterado", font=('Calibri', 11, 'italic', 'bold'))],
        [sg.Input(key='id_produto', font=('Calibri', 10))],
        [sg.Button('Consultar', pad=((0, 10), 5)), sg.Button('Cancelar', pad=((0, 10), 5))]
    ]

    window_popup = sg.Window('Alterar Produto', layout_popup, icon=r'projeto_crud\update.ico')

    while True:
        event, values = window_popup.read()

        if event == sg.WIN_CLOSED or event == 'Cancelar':
            break
        elif event == 'Consultar':
            id_produto = values['id_produto']
            produto_existente = sistema.consultar_produto(id_produto)

            if produto_existente:
                layout_popup = [
                    [sg.Text(f"ID do produto: {produto_existente.id_produto}", font=('Calibri', 13, 'italic', 'bold'))],
                    [sg.Text('-' * 130)],

                    [sg.Text("Informe o novo nome do produto:", font=('Calibri', 11, 'italic', 'bold')),
                    sg.Input(default_text=produto_existente.nome_produto, font=('Calibri', 10), key='nome_produto')],

                    [sg.Text("Informe o novo tipo do produto:", font=('Calibri', 11, 'italic', 'bold')),
                    sg.Combo(listas_tp_produtos, default_value=produto_existente.tipo_produto, font=('Calibri', 10), key='tipo_produto')],

                    [sg.Text("Informe a nova quantidade:", font=('Calibri', 11, 'italic', 'bold')),
                    sg.Combo(lista_quantidade, default_value=produto_existente.quantidade, font=('Calibri', 10), key='quantidade')],

                    [sg.Text("Informe o novo valor do produto:", font=('Calibri', 11, 'italic', 'bold')),
                    sg.Input(default_text=produto_existente.preco_produto, font=('Calibri', 10), key='valor_produto'), sg.Push()],

                    [sg.Button('OK', font=('Calibri', 11, 'italic', 'bold'), pad=((0, 10), 5)),
                    sg.Button('Cancelar', font=('Calibri', 11, 'italic', 'bold'), pad=((0, 10), 5))]
                    ]

                window_popup = sg.Window(f'Alterar Produto - {produto_existente.nome_produto}', layout_popup, icon=r'projeto_crud\update.ico')

                while True:
                    event, values = window_popup.read()

                    if event == sg.WIN_CLOSED or event == 'Cancelar':
                        break
                    elif event == 'OK':
                        nome_produto = values['nome_produto']
                        tipo_produto = values['tipo_produto']
                        quantidade = values['quantidade']
                        valor_produto = values['valor_produto']
                        valor_produto = float(valor_produto.replace(',', '.'))

                        novo_produto = Produto(id_produto, nome_produto, tipo_produto, int(quantidade), valor_produto)
                        sistema.alterar_produto(id_produto, novo_produto)

                        window_popup.close()
                        sg.popup_ok("Produto alterado com sucesso.", title="Alterar Produto", font=('Calibri', 11, 'italic', 'bold'), icon=r'projeto_crud\ok.ico')
                        break

            else:
                sg.popup_error("Produto não encontrado.", title="Alterar Produto", font=('Calibri', 10, 'italic', 'bold'), icon=r'projeto_crud\error.ico')

            break

    window_popup.close()
            






# Função para implementar a lógica de exclusão
def excluir_produto():
    layout_popup = [
        [sg.Text("Informe o ID do produto a ser excluído", font=('Calibri', 11, 'italic', 'bold'))],
        [sg.Input(key='id_produto', font=('Calibri', 10))],
        [sg.Button('Consultar', pad=((0, 10), 5)), sg.Button('Cancelar', pad=((0, 10), 5))]
    ]

    window_popup = sg.Window('Excluir Produto', layout_popup, icon=r'projeto_crud\delete.ico')

    while True:
        event, values = window_popup.read()

        if event == sg.WIN_CLOSED or event == 'Cancelar':
            break
        elif event == 'Consultar':
            id_produto = values['id_produto']
            produto_existente = sistema.consultar_produto(id_produto)

            if produto_existente:
                sistema.excluir_produto(id_produto)
                sg.popup_ok("Produto excluído com sucesso.", title="Excluir Produto", font=('Calibri', 11, 'italic', 'bold'), icon=r'projeto_crud\ok.ico')
            else:
                sg.popup_ok("Produto não encontrado.", title="Excluir Produto", font=('Calibri', 11, 'italic', 'bold'), icon=r'projeto_crud\ok.ico')
            break

    window_popup.close()




# Função para implementar a lógica de listagem
def listar_produtos():
    lista_produtos = sistema.obter_lista_produtos()
    if lista_produtos:
        popup_text = "Listagem dos produtos cadastrados:\n---------------------------\n"
        #calculo_valor_total = str(produto.quantidade) * produto.valor_produto
        for produto in lista_produtos:
            popup_text += (f"ID do produto: {produto.id_produto}\nNome do produto: {produto.nome_produto}\n"
                           f"Tipo do produto: {produto.tipo_produto}\nQuantidade: {produto.quantidade}\n"
                           f"Preço do produto: {produto.valor_produto}\nValor total: {produto.valor_final}\n\n")

        sg.popup(popup_text, font=('Calibri', 11, 'italic', 'bold'), title="Lista de Produtos", line_width=50, icon=r'projeto_crud\read.ico')
    else:
        sg.popup_ok("Não há produtos cadastrados.", title="Listar Produtos", font=('Calibri', 11, 'italic', 'bold'), icon=r'projeto_crud\ok.ico')








# Criação de instâncias
sistema = SistemaCRUD()
sg.theme('GreenTan')
# Execução do programa
layout = criar_layout()
mostrar_janela(layout)
