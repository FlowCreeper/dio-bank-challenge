from datetime import datetime, date
from abc import ABC, abstractmethod

class Transaction(ABC):
  @abstractmethod
  def record(self, account: "Account"):
    pass
    
class Deposit(Transaction):
  def __init__(self, value: float):
    self._value = value

  def record(self, account: "Account"):
    new_balance = account.balance() + self._value
    return new_balance, self

class Withdraw(Transaction):
  def __init__(self, value):
    self._value = value

  def record(self, account: "Account"):
    if account.balance() >= self._value:
      new_balance = account.balance() - self._value
      return new_balance, self
    print(f"@ Saldo na conta insuficiente: R$ {account.balance():.2f} :: R$ {self._value:.2f}")
    return None, self

class Statement:
  def __init__(self):
    self.str_transactions : list[str] = []
    self.transactions : list[Transaction] = []

  def add_to_statement(self, transaction: Transaction):
    date_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    if isinstance(transaction, Deposit):
      symbol = "+"
      value = transaction._value
    elif isinstance(transaction, Withdraw):
      symbol = "-"
      value = transaction._value
    else:
      return 
    self.transactions.append(transaction)
    self.str_transactions.append(f"{symbol}   R$ {value:14.2f}   -   {date_time}")
    return True

class User:
  def __init__(self, address: str):
    self._address = address
    self._accounts = []

  def new_transaction(self, account: "Account", transaction: Transaction) -> tuple | None:
    if account in self._accounts:
      return transaction.record(account)
    print(f"@ A conta não pertence ao usuário")

  def add_account(self, account: "Account") -> "Account":
    self._accounts.append(account)
    return account

class NaturalPerson(User):
  def __init__(self, address: str, cpf: str, name: str, birth_date: date):
    super().__init__(address)
    self._cpf = cpf
    self._birth_date = birth_date
    self.name = name

class Account:
  def __init__(self, *, number: int, user: User):
    self._balance = 0.0
    self._number = number
    self._AGENCY = "0001"
    self._user = user
    self._statement = Statement()

  def balance(self) -> float:
    return self._balance
  
  @classmethod
  def new_account(cls, number: int, user: User) -> "Account":
    return user.add_account(cls(number=number, user=user))

  def deposit(self, value: float) -> bool:
    new_balance, deposit = Deposit(value).record(self)
    
    if new_balance is not None:
      self._balance = new_balance
      self._statement.add_to_statement(deposit)
      return True

    return False

  def withdraw(self, value: float) -> bool:
    new_balance, withdraw = Withdraw(value).record(self)
    if new_balance is not None:
      self._balance = new_balance
      self._statement.add_to_statement(withdraw)
      return True
    
    return False
  
  def get_statement(self):
    string = ""
    string += f"Extrato da conta {self._number} - Agência {self._AGENCY}\n"
    for line in self._statement.str_transactions:
      string += line + "\n"
    string += f"{"".center(48, "-")}\nSaldo atual: R$ {self._balance:.2f}\n"

    return string

class CheckingAccount(Account):
  def __init__(self, number: int, user: User, limit=500.0, withdraws_limit=3):
    super().__init__(number=number, user=user)
    self.limit = limit
    self.withdraws_limit = withdraws_limit
    self.count = 0

  def withdraw(self, value):
    if self.count >= self.withdraws_limit:
      print("@ Limite de transações atingido, tente novamente amanhã!")
    elif value > self.limit:
      print(f"@ Valor excede o valor máximo de R$ {self.limit:.2f} :: R$ {value:.2f}")
    else:
      if super().withdraw(value):
        self.count += 1
        return True
      
    return False

def test():
  user = NaturalPerson("Rua A, 123", "12345678900", "João Silva", date(1990, 1, 1))
  acc = CheckingAccount(1, user)
  user.add_account(acc)

  acc.deposit(1000)
  acc.withdraw(200)
  acc.withdraw(300)
  acc.withdraw(50)
  acc.withdraw(10)  # Deve falhar (limite de 3 saques)
  acc.get_statement()

# test()

def text_divisor(content="", size=48, character='='):
  return content.center(size, character)

def double_enter_print(text=""):
  print(text, end="\n\n")

def input_float_validation(msg="Informe um valor: "):
  try:
    value = float(input(msg))
    return value
  except ValueError:
    double_enter_print("@ Valor inválido. Tente novamente.")
    return None

def find_user_by_cpf(users: list, cpf: str):
  for user in users:
    if isinstance(user, NaturalPerson) and user._cpf == cpf:
      return user
  return None

def main():
  users: list[NaturalPerson] = []
  accounts: list[Account] = []

  account_number = 1
  current_user = None

  MENU = f"""{text_divisor(" MENU ")}
  [1] Criar Usuário
  [2] Trocar Usuário
  [3] Criar Conta
  [4] Selecionar Conta
  [5] Depositar
  [6] Sacar
  [7] Ver Extrato
  [8] Listar Contas
  [0] Sair
"""
  
  # Usuários e contas de exemplo
  user1 = NaturalPerson("Rua das Flores, 123", "11111111111", "Ana Souza", date(1990, 5, 14))
  user2 = NaturalPerson("Av. Brasil, 456", "22222222222", "Carlos Lima", date(1985, 8, 20))
  user3 = NaturalPerson("Rua Verde, 789", "33333333333", "Mariana Silva", date(2000, 1, 10))

  users.extend([user1, user2, user3])

  acc1 = CheckingAccount(number=account_number, user=user1)
  account_number += 1
  acc2 = CheckingAccount(number=account_number, user=user2)
  account_number += 1
  acc3 = CheckingAccount(number=account_number, user=user3)
  account_number += 1

  user1.add_account(acc1)
  user2.add_account(acc2)
  user3.add_account(acc3)

  accounts.extend([acc1, acc2, acc3])

  # Transações iniciais
  acc1.deposit(1000.0)
  acc1.withdraw(150.0)
  acc1.deposit(500.0)

  acc2.deposit(2000.0)
  acc2.withdraw(300.0)

  acc3.deposit(1500.0)

  current_user = user1  # Começa com o usuário Ana Souza
  print(f"> Usuário inicial: {current_user._cpf} - {current_user._accounts[0]._number}")

  while True:
    print(MENU)

    if current_user:
      print(f"> Usuário atual: {current_user.name}")
      if current_user._accounts:
        print(f"> Conta ativa: {current_user._accounts[0]._number}")
    else:
      print("> Nenhum usuário selecionado")

    choice = input("\nEscolha uma opção: ").strip()

    if choice == "1":
      cpf = input("CPF: ").strip()
      if find_user_by_cpf(users, cpf):
        double_enter_print("@ Usuário já existe.")
        continue
      nome = input("Nome completo: ")
      nascimento = input("Data de nascimento (DD-MM-AAAA): ")
      endereco = input("Endereço: ")
      try:
        birth_date = datetime.strptime(nascimento, "%d-%m-%Y").date()
      except ValueError:
        double_enter_print("@ Data inválida.")
        continue
      user = NaturalPerson(address=endereco, cpf=cpf, name=nome, birth_date=birth_date)
      users.append(user)
      double_enter_print("> Usuário criado com sucesso.")

    elif choice == "2":
      cpf = input("Digite o CPF: ")
      user = find_user_by_cpf(users, cpf)
      if user:
        current_user = user
        double_enter_print(f"> Usuário {cpf} selecionado com sucesso.")
      else:
        double_enter_print("@ Usuário não encontrado.")

    elif choice == "3":
      if not current_user:
        double_enter_print("@ Nenhum usuário selecionado.")
        continue
      conta = CheckingAccount(number=account_number, user=current_user)
      current_user.add_account(conta)
      accounts.append(conta)
      double_enter_print(f"> Conta {account_number} criada para o usuário {current_user.name}")
      account_number += 1

    elif choice == "4":
      if not current_user or not current_user._accounts:
        double_enter_print("@ Nenhum usuário selecionado ou sem contas.")
        continue
      print("Contas disponíveis:")
      for i, acc in enumerate(current_user._accounts):
        print(f"[{i}] Conta {acc._number} | Saldo: R$ {acc.balance():.2f}")
      try:
        index = int(input("Escolha o número da conta: "))
        conta = current_user._accounts[index]
        current_user._accounts = [conta]  # Mantém apenas a conta ativa
        double_enter_print(f"> Conta {conta._number} selecionada.")
      except (ValueError, IndexError):
        double_enter_print("@ Conta inválida.")

    elif choice == "5":
      if not current_user or not current_user._accounts:
        double_enter_print("@ Nenhum usuário ou conta ativa.")
        continue
      value = input_float_validation("Valor para depósito: ")
      if value is not None:
        if current_user._accounts[0].deposit(value):
          double_enter_print("> Depósito realizado com sucesso.")
        else:
          double_enter_print("@ Falha no depósito.")

    elif choice == "6":
      if not current_user or not current_user._accounts:
        double_enter_print("@ Nenhum usuário ou conta ativa.")
        continue
      value = input_float_validation("Valor para saque: ")
      if value is not None:
        if current_user._accounts[0].withdraw(value):
          double_enter_print("> Saque realizado com sucesso.")
        else:
          double_enter_print("@ Falha no saque.")

    elif choice == "7":
      if not current_user or not current_user._accounts:
        double_enter_print("@ Nenhum usuário ou conta ativa.")
        continue
      double_enter_print(current_user._accounts[0].get_statement())

    elif choice == "8":
      if not accounts:
        double_enter_print("Nenhuma conta cadastrada.")
        continue
      for acc in accounts:
        print(f"Agência: {acc._AGENCY} | Número: {acc._number} | Titular: {acc._user.name}")
      print()

    elif choice == "0":
      print("\nEncerrando aplicação. Até logo!")
      break

    else:
      double_enter_print("@ Opção inválida. Tente novamente.")
  
  print(text_divisor())

main()