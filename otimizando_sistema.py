# ======================
# FUNÇÕES DO SISTEMA
# ======================

def depositar(saldo, valor, extrato, /):
    """Depósito (positional-only)"""
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        print("Operação falhou! Valor inválido.")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """Saque (keyword-only)"""
    if valor <= 0:
        print("Operação falhou! Valor inválido.")
    elif valor > saldo:
        print("Operação falhou! Saldo insuficiente.")
    elif valor > limite:
        print("Operação falhou! Valor excede o limite.")
    elif numero_saques >= limite_saques:
        print("Operação falhou! Limite de saques atingido.")
    else:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
    return saldo, extrato, numero_saques

def mostrar_extrato(saldo, /, *, extrato):
    """Extrato (positional + keyword-only)"""
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios):
    """Cadastrar novo usuário"""
    nome = input("Nome: ").strip()
    data_nascimento = input("Data de nascimento (dd/mm/aaaa): ").strip()
    cpf = ''.join(filter(str.isdigit, input("CPF (somente números): ").strip()))
    endereco = input("Endereço (logradouro, nro, bairro, cidade/sigla, estado): ").strip()
    
    if any(u["cpf"] == cpf for u in usuarios):
        print("Usuário já cadastrado com esse CPF!")
        return None
    
    usuario = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco,
        "contas": []
    }
    usuarios.append(usuario)
    print(f"Usuário {nome} cadastrado com sucesso!")
    return usuario

def criar_conta(contas, usuarios, numero_conta):
    """Cadastrar nova conta vinculada a um usuário"""
    cpf = ''.join(filter(str.isdigit, input("Informe o CPF do usuário: ").strip()))
    
    # Buscar usuário pelo CPF
    usuario = next((u for u in usuarios if u["cpf"] == cpf), None)
    if not usuario:
        print("Usuário não encontrado. Cadastre-o primeiro.")
        return None
    
    conta = {
        "agencia": "0001",
        "numero": numero_conta,
        "usuario": usuario,
        "saldo": 0,
        "extrato": "",
        "saques_realizados": 0
    }
    contas.append(conta)
    usuario["contas"].append(conta)
    print(f"Conta {numero_conta} criada para {usuario['nome']}.")
    return conta

def listar_contas(contas):
    """Listar contas existentes"""
    if not contas:
        print("Nenhuma conta cadastrada.")
        return
    for c in contas:
        print(f"Agência: {c['agencia']}, Conta: {c['numero']}, Usuário: {c['usuario']['nome']}")

# ======================
# PROGRAMA PRINCIPAL
# ======================

menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[cu] Cadastrar Usuário
[cc] Cadastrar Conta
[lc] Listar Contas
[q] Sair
=> """

usuarios = []
contas = []
numero_conta_seq = 1
conta_atual = None
LIMITE_SAQUES = 3
LIMITE_SAQUE_DIARIO = 500

while True:
    opcao = input(menu).strip().lower()
    
    if opcao == "d":
        if not conta_atual:
            print("Nenhuma conta selecionada. Cadastre ou selecione uma conta.")
            continue
        valor = float(input("Informe o valor do depósito: "))
        conta_atual["saldo"], conta_atual["extrato"] = depositar(conta_atual["saldo"], valor, conta_atual["extrato"])
    
    elif opcao == "s":
        if not conta_atual:
            print("Nenhuma conta selecionada. Cadastre ou selecione uma conta.")
            continue
        valor = float(input("Informe o valor do saque: "))
        conta_atual["saldo"], conta_atual["extrato"], conta_atual["saques_realizados"] = sacar(
            saldo=conta_atual["saldo"],
            valor=valor,
            extrato=conta_atual["extrato"],
            limite=LIMITE_SAQUE_DIARIO,
            numero_saques=conta_atual["saques_realizados"],
            limite_saques=LIMITE_SAQUES
        )
    
    elif opcao == "e":
        if not conta_atual:
            print("Nenhuma conta selecionada. Cadastre ou selecione uma conta.")
            continue
        mostrar_extrato(conta_atual["saldo"], extrato=conta_atual["extrato"])
    
    elif opcao == "cu":
        criar_usuario(usuarios)
    
    elif opcao == "cc":
        conta_atual = criar_conta(contas, usuarios, numero_conta_seq)
        if conta_atual:
            numero_conta_seq += 1
    
    elif opcao == "lc":
        listar_contas(contas)
    
    elif opcao == "q":
        break
    
    else:
        print("Opção inválida, selecione novamente.")
