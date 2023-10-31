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