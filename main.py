from os import system, name
from datetime import datetime, date

def text_divisor(content="", size=24, character='='):
  return content.center(size, character)

def input_float_validation(input_message=""):
  try:
    entry = float(input(input_message))
  except ValueError:
    print(f"Valor inválido - \"{entry}\"", end="\n\n")
  
  return entry

def double_enter_print(string=""):
  print(string, end="\n\n")

MENU_BOX = f"""{text_divisor(" MENU ")}

  [1] Depósito
  [2] Saque
  [3] Extrato
  [0] Sair
"""
WITHDRAW_MAX_VALUE = 500.0
WITHDRAW_LIMIT_PER_DAY = 10

withdrew_count = 0
balance = 0
last_loop_date = date.today()
menu_entry = None
statement = []

while True:
  if last_loop_date != date.today():
    withdrew_count, last_loop_date = 0, date.today()

  if not menu_entry:
    print(MENU_BOX)
    menu_entry = input("Insira a opção: ")
    print()

  if menu_entry == "1":
    # Depósito logic
    double_enter_print(text_divisor(" Depósito "))

    deposit_entry = input_float_validation("Informe o valor a ser depositado: ")

    if deposit_entry == 0:
      menu_entry = None
      continue

    balance += deposit_entry
    statement.append(f"+ {deposit_entry} | {datetime.now()}")
    double_enter_print(f"Depósito no valor de R$ {deposit_entry:.2f} realizado com sucesso!")
    menu_entry = None

  elif menu_entry == "2":
    # Saque logic
    double_enter_print(text_divisor(" Saque "))

    if withdrew_count > WITHDRAW_LIMIT_PER_DAY:
      double_enter_print("Quantidade de máxima de saques atingida. \nSe acha que essa mensagem é um erro contate o gerente")
      menu_entry = None
      continue
    
    withdraw_entry = input_float_validation("Informe o valor a ser sacado: ")

    if withdraw_entry == 0:
      menu_entry = None
      continue

    if withdraw_entry > WITHDRAW_MAX_VALUE:
      double_enter_print(f"Valor excede o valor de saque máximo de R$ {WITHDRAW_MAX_VALUE:.2f} | R$ {withdraw_entry:.2f}")
      continue

    if withdraw_entry > balance:
      double_enter_print(f"Valor excede o valor na conta de R$ {balance:.2f} | R$ {withdraw_entry:.2f}")
      continue

    balance -= withdraw_entry
    withdrew_count += 1
    statement.append(f"- {withdraw_entry} | {datetime.now()}")
    double_enter_print(f"Saque no valor de R$ {withdraw_entry:.2f} realizado com sucesso!")
    menu_entry = None
    
  elif menu_entry == "3":
    # Extrato logic
    double_enter_print(text_divisor(" Extrato "))
    if statement:
      for i in statement:
        print(i)
      print()
    else:
      double_enter_print("Histórico vazio")
    menu_entry = None

  elif menu_entry == "0":
    # Saída logic
    double_enter_print(text_divisor(" Saída "))
    double_enter_print("Obrigado por usar nossos serviços, até breve!")
    break

  else:
    print(f"Entrada Inválida - \"{menu_entry}\"")
    menu_entry = None

  system('pause' if name == 'nt' else 'read -n 1 -s -r -p ""')
  
print(text_divisor())