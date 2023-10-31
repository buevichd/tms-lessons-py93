import random


def get_random_digits(count: int) -> str:
    result = ''
    for _ in range(count):
        result += str(random.randint(0, 9))
    return result


class BankAccount:
    def __init__(self, card_holder):
        self.card_holder = card_holder.upper()
        self.money = 0
        self.account_number = get_random_digits(20)
        self.card_number = get_random_digits(16)


class Bank:
    def __init__(self):
        self.__bank_accounts: list[BankAccount] = []

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
    def __init__(self):
        self.bank = Bank()

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


if __name__ == '__main__':
    controller = Controller()
    controller.run()
