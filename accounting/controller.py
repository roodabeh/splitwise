from accounting.models import *


# ************************* Splitwise *************************

def find_min_index(debt_arr: {}):
    min_index = list(debt_arr.keys())[0]
    for username in debt_arr.keys():
        if debt_arr[username] < debt_arr[min_index]:
            min_index = username
    return min_index


def find_max_index(debt_arr: {}):
    max_index = list(debt_arr.keys())[0]
    for username in debt_arr.keys():
        if debt_arr[username] > debt_arr[max_index]:
            max_index = username
    return max_index


# convert list of spends to a debt arr
# pay_amount['p'] is the net amount to be paid to person 'p'
def get_pay_amount_array(expenses):
    pay_amount = {}
    for expense in expenses:
        # expense.delete()
        # continue
        debts = Debt.objects.filter(expense=expense)
        for debt in debts:
            debtor = debt.debtor
            pay_amount[debtor.username] = pay_amount.get(debtor.username, 0) - debt.share

    print(pay_amount)
    return pay_amount


def cal_min_cash_flow(expenses):
    transactions = list()

    pay_amount = get_pay_amount_array(expenses)
    if len(pay_amount) == 0:
        return transactions

    max_credit = find_max_index(pay_amount)
    max_dept = find_min_index(pay_amount)
    print(pay_amount[max_credit], pay_amount[max_dept])
    while int(pay_amount[max_credit]) != 0 or int(pay_amount[max_dept]) != 0:
        exchange_value = min(pay_amount[max_credit], -pay_amount[max_dept])
        pay_amount[max_credit] -= exchange_value
        pay_amount[max_dept] += exchange_value

        transactions.append((max_credit, max_dept, exchange_value))

        max_credit = find_max_index(pay_amount)
        max_dept = find_min_index(pay_amount)

    return transactions
