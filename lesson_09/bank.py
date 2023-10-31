import random
import json
import os


def get_random_digits(count: int) -> str:
    result = ''
    for _ in range(count):
        result += str(random.randint(0, 9))
    return result


class BankAccount:
    def __init__(self, card_holder, money=0.0, card_number=None, account_number=None):
        self.card_holder: str = card_holder.upper()
        self.money: float = money
        self.card_number: str = get_random_digits(16) if card_number is None else card_number
        self.account_number: str = get_random_digits(20) \
            if account_number is None else account_number


def convert_bank_account_to_dict(bank_account: BankAccount) -> dict:
    return {
        'card_holder': bank_account.card_holder,
        'money': bank_account.money,
        'card_number': bank_account.card_number,
        'account_number': bank_account.account_number
    }


def save_accounts(bank_accounts: list[BankAccount], file_name: str):
    data = [convert_bank_account_to_dict(account) for account in bank_accounts]
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=2)


def load_accounts(file_name) -> list[BankAccount]:
    if not os.path.exists(file_name):
        return []
    with open(file_name, 'r') as file:
        return [BankAccount(**data) for data in json.load(file)]


class Bank:
    def __init__(self, bank_accounts: list[BankAccount] = None):
        self.__bank_accounts: list[BankAccount] = bank_accounts or []

    def open_account(self, card_holder) -> BankAccount:
        account = BankAccount(card_holder)
        self.__bank_accounts.append(account)
        return account

    def __get_account(self, account_number: str) -> BankAccount:
        for account in self.__bank_accounts:
            if account.account_number == account_number:
                return account
        # There should be raise ValueError()
        return None

    def get_all_bank_accounts(self) -> list[BankAccount]:
        return self.__bank_accounts

    def add_money(self, account_number: str, money: float):
        target_account = self.__get_account(account_number)
        target_account.money += money

    def transfer_money(self, from_account_number,
                       to_account_number, money):
        from_account = self.__get_account(from_account_number)
        to_account = self.__get_account(to_account_number)
        from_account.money -= money
        to_account.money += money

    def external_transfer(self, from_account_number,
                          to_external_number, money):
        from_account = self.__get_account(from_account_number)
        from_account.money -= money

        print(f'Банк перевёл {money}$ с вашего счёта '
              f'{from_account_number} на внешний счёт '
              f'{to_external_number}')


class Controller:
    def __init__(self, data_file_name):
        self.data_file_name = data_file_name
        bank_accounts: list[BankAccount] = load_accounts(data_file_name)
        self.bank = Bank(bank_accounts)

    def run(self):
        print('Здравствуйте, наш банк открылся!')
        while True:
            print('Выберите действие:')
            print('0. Завершить программу')
            print('1. Открыть новый счёт')
            print('2. Просмотреть открытые счета')
            print('3. Положить деньги на счёт')
            print('4. Перевести деньги между счетами')
            print('5. Совершить платёж')

            action = int(input())
            if action == 0:
                save_accounts(self.bank.get_all_bank_accounts(), self.data_file_name)
                print('До свидания!')
                break
            elif action == 1:
                card_holder = input('Введите имя и фамилию держателя карты: ')
                account = self.bank.open_account(card_holder)
                print(f'Счёт {account.account_number} создан!')
            elif action == 2:
                print('Все счета:')
                for account in self.bank.get_all_bank_accounts():
                    print(f'Cчёт: {account.account_number}')
                    print(f'   Остаток на счету: {account.money}$')
                    print(f'   Номер карты: {account.card_number}')
                    print(f'   Держатель карты: {account.card_holder}')
            elif action == 3:
                account_number = input('Введите номер счёта: ')
                money = float(input('Введите количество денег: '))
                self.bank.add_money(account_number, money)
            elif action == 4:
                from_account_number = input('Введите номер счёта отправителя: ')
                to_account_number = input('Введите номер счёта получателя: ')
                money = float(input('Введите количество денег: '))
                self.bank.transfer_money(from_account_number, to_account_number,
                                         money)
            elif action == 5:
                from_account_number = input('Введите номер счёта отправителя: ')
                to_external_number = input('Введите номер внешнего счёта: ')
                money = float(input('Введите количество денег: '))
                self.bank.external_transfer(from_account_number, to_external_number,
                                            money)
            else:
                print('Вы ввели неподдерживаемую команду')


if __name__ == '__main__':
    controller = Controller('data.json')
    controller.run()
