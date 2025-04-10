from os import system, name
from datetime import datetime, date

def text_divisor(content="", size=48, character='='):
  return content.center(size, character)

def input_float_validation(input_message=""):
  try:
    entry = ""
    entry = float(input(input_message))
  except ValueError:
    double_enter_print(f"@ Valor inválido - \"{entry}\"")
    return 
  return entry

def double_enter_print(string=""):
  print(string, end="\n\n")

def deposit(entry: float, balance: float, statement: list[str], /):
  if not entry:
    double_enter_print("Voltando ao menu...")
    return balance, statement

  balance += entry
  statement.append(f"+\t\tR$ {entry:.2f} : {datetime.now()}")
  double_enter_print(f"Depósito no valor de R$ {entry:.2f} realizado com sucesso!")

  return balance, statement

def withdraw(*, entry: float, balance: float, statement: list[str], count: int, limit: float):
  if not entry:
    double_enter_print("Voltando ao menu...")
    return balance, statement
  
  if entry > balance:
    double_enter_print(f"@ Valor excede o valor na conta de R$ {balance:.2f} | R$ {entry:.2f}")
    return

  if entry > limit:
    double_enter_print(f"@ Valor excede o valor de saque máximo de R$ {limit:.2f} | R$ {entry:.2f}")
    return

  balance -= entry
  count += 1
  statement.append(f"-\t\tR$ {entry:.2f} : {datetime.now()}")
  double_enter_print(f"Saque no valor de R$ {entry:.2f} realizado com sucesso!")

  return balance, statement

def get_statement(balance: float, /, *, statement: list):
  if statement:
    for i in statement:
      print(i)
      
    double_enter_print(f"Saldo = \tR$ {balance:.2f} : {datetime.now()}")
  else:
    double_enter_print("Extrato vazio")

  return balance, statement

def find_user_by_cpf(users: list[dict], cpf: str):
  for user in users:
    if user["cpf"] == cpf:
      return user

def create_user(users: list[dict]):
  cpf = input("Insira o CPF (somente números): ")

  if find_user_by_cpf(users, cpf):
    double_enter_print(f"@ CPF já cadastrado | {cpf}")
    return
  
  name = input("Insira seu nome completo: ")
  birthday = input("Insira sua data de nascimento (dd-mm-aaaa): ")
  address = input("Insira seu endereço (logradouro, numero - bairro - cidade/sigla estado)")

  users.append({"nome": name, "data_nascimento": birthday, "cpf": cpf, "address": address, "accounts": []})

  double_enter_print(f"Usuário {name} criado com sucesso!")
  return users[-1]

def create_account(account_number: int, users: list, accounts: list[dict], agency):
  cpf = input("Insira o CPF do usuário (somente números): ")
  user = find_user_by_cpf(users, cpf)

  if user:
    accounts.append({"agencia": f"{agency:04}", "conta": f"{account_number:08}", "usuario": user})
    double_enter_print(f"Conta {account_number} criada com sucesso!")
    return accounts[-1]
  
  double_enter_print(f"@ CPF não cadastrado | {cpf}")

def list_accounts(accounts: list[dict]):
  for account in accounts:
    for key in account.keys():
      if key == "usuario":
        print(f"{key.title()}: {account[key]["nome"]}")
      else:
        print(f"{key.title()}: {account[key]}")
    print()
    if account != accounts[-1]:
      double_enter_print(text_divisor(character='-'))

def main():
  MENU_BOX = f"""{text_divisor(" MENU ")}

  [1] Depósito
  [2] Saque
  [3] Extrato
  [4] Cadastro de Usuário
  [5] Cadastro de Conta
  [6] Listar Contas
  [0] Sair
"""
  
  AGENCY = 1
  WITHDRAW_MAX_VALUE = 500.0
  WITHDRAW_LIMIT_PER_DAY = 10

  withdrew_count = 0
  balance = 0
  last_loop_date = date.today()
  menu_entry: str = None
  statement: list[str] = []
  users: list[dict] = []
  accounts: list[dict] = []
  account_count = 0

  while True:
    if last_loop_date != date.today():
      withdrew_count, last_loop_date = 0, date.today()

    if not menu_entry:
      print(MENU_BOX)
      menu_entry = input("Insira a opção: ")
      print()

    if isinstance(menu_entry, str):
      if menu_entry.isdigit():
        menu_entry = int(menu_entry)

    if menu_entry == 1:
      # Depósito logic
      double_enter_print(text_divisor(" Depósito "))

      deposit_entry = input_float_validation("Informe o valor a ser depositado: ")
      if deposit_entry is None: continue
      balance = deposit(deposit_entry, balance, statement)[0]
      menu_entry = None 

    elif menu_entry == 2:
      # Saque logic
      double_enter_print(text_divisor(" Saque "))

      if withdrew_count > WITHDRAW_LIMIT_PER_DAY:
        double_enter_print("@ Quantidade de máxima de saques atingida. \n  Se acha que essa mensagem é um erro contate o gerente")
        menu_entry = None
        continue
      
      withdraw_entry = input_float_validation("Informe o valor a ser sacado: ")
      if withdraw_entry is None: continue

      balance = withdraw(entry=withdraw_entry, balance=balance, statement=statement, count=withdrew_count, 
                         limit=WITHDRAW_MAX_VALUE)[0]

      menu_entry = None
      
    elif menu_entry == 3:
      # Extrato logic
      double_enter_print(text_divisor(" Extrato "))
      
      menu_entry = None if get_statement(balance, statement=statement) else menu_entry

    elif menu_entry == 4:
      double_enter_print(text_divisor(" Cadastro de Usuário "))

      create_user(users)

      menu_entry = None

    elif menu_entry == 5:
      double_enter_print(text_divisor(" Cadastro de Conta Corrente "))

      create_account(account_count, users, accounts, AGENCY) 

      menu_entry = None

    elif menu_entry == 6:
      double_enter_print(text_divisor(" Contas Corrente Cadastradas "))

      list_accounts(accounts)

      menu_entry = None

    elif menu_entry == 0:
      # Saída logic
      double_enter_print(text_divisor(" Saída "))

      double_enter_print("Obrigado por usar nossos serviços, até breve!")
      break

    else:
      double_enter_print(f"@ Entrada Inválida - \"{menu_entry}\"")
      menu_entry = None

    system('pause' if name == 'nt' else 'read -n 1 -s -r -p ""')
    
  print(text_divisor())

main()