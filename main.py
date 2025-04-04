from time import sleep

def text_divisor(content="", /, *, size=24, character='='):
  return content.center(size, character)

MENU_BOX = f"""{text_divisor(" MENU ")}

  [1] Depósito
  [2] Saque
  [3] Extrato
  [0] Sair
"""
WITHDRAW_MAX_VALUE = 500.0
WITHDRAW_LIMIT_PER_DAY = 3

withdrew_count = 0
balance = 0
menu_entry = None
statement = []

while True:
  if not menu_entry:
    print(MENU_BOX)
    menu_entry = input("Insira a opção: ")
    print()

  if menu_entry == "1":
    # Depósito logic
    print(text_divisor(" Depósito "), end="\n\n")

    try:
      deposit_entry = float(input("Informe o valor a ser depositado: "))
    except ValueError:
      print(f"Valor inválido - \"{deposit_entry}\"", end="\n\n")

    balance += deposit_entry
    statement.append(f"+ {deposit_entry}")
    print(f"Depósito no valor de R$ {deposit_entry:.2f} realizado com sucesso!", end="\n\n")
    menu_entry = None

  elif menu_entry == "2":
    # Saque logic
    print(text_divisor(" Saque "), end="\n\n")

    if withdrew_count > WITHDRAW_LIMIT_PER_DAY:
      print("Quantidade de máxima de saques atingida. \nSe acha que essa mensagem é um erro contate o gerente", end="\n\n")
      menu_entry = None
      continue
    
    try:
      withdraw_entry = float(input("Informe o valor a ser sacado (0 para sair): "))
    except ValueError:
      print(f"Valor inválido - \"{withdraw_entry}\"", end="\n\n")

    if withdraw_entry == 0:
      menu_entry = None
      continue

    if withdraw_entry > WITHDRAW_MAX_VALUE:
      print(f"Valor excede o valor de saque máximo de R$ {WITHDRAW_MAX_VALUE:.2f} - R$ {withdraw_entry:.2f}", end="\n\n")
      continue

    if withdraw_entry > balance:
      print(f"Valor excede o valor na conta R$ {balance:.2f} - R$ {withdraw_entry:.2f}", end="\n\n")
      continue

    balance -= withdraw_entry
    withdrew_count += 1
    statement.append(f"- {withdraw_entry}")
    print(f"Saque no valor de R$ {withdraw_entry:.2f} realizado com sucesso!", end="\n\n")
    menu_entry = None
    
  elif menu_entry == "3":
    # Extrato logic
    print(text_divisor(" Extrato "), end="\n\n")
    if statement:
      for i in statement:
        print(i)
      print()
    else:
      print("Histórico vazio", end="\n\n")
    menu_entry = None

  elif menu_entry == "0":
    # Saída logic
    print(text_divisor(" Saída "), end="\n\n")
    print("Obrigado por usar nossos serviços, até breve!", end="\n\n")
    break

  else:
    print(f"Entrada Inválida - \"{menu_entry}\"")
    menu_entry = None

  sleep(2)
  
print(text_divisor(), end="\n\n")