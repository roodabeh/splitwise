# ************************* Splitwise *************************

def find_min_index(debt_arr):
    min_index = 0
    for i in range(1, len(debt_arr)):
        if debt_arr[i] < debt_arr[min_index]:
            min_index = i
    return min_index


def find_max_index(debt_arr):
    max_index = 0
    for i in range(1, len(debt_arr)):
        if debt_arr[i] > debt_arr[max_index]:
            max_index = i
    return max_index


def get_payment_graph(spends):
    # convert list of spends to a payment flow graph
    pass


def convert_graph_2_debt_arr(graph, n):
    debt_arr = [0 for _ in range(n)]
    for j in range(n):
        for i in range(n):
            debt_arr[j] += (graph[i][j] - graph[j][i])
    return debt_arr


def cal_min_cash_flow(debt_arr):
    transactions = list()
    max_debt_index = find_max_index(debt_arr)
    min_debt_index = find_min_index(debt_arr)
    while debt_arr[max_debt_index] != 0 or debt_arr[min_debt_index] != 0:
        exchange_value = min(debt_arr[max_debt_index], -debt_arr[min_debt_index])
        debt_arr[max_debt_index] -= exchange_value
        debt_arr[min_debt_index] += exchange_value

        transactions.append((max_debt_index, min_debt_index, exchange_value))

        max_debt_index = find_max_index(debt_arr)
        min_debt_index = find_min_index(debt_arr)

    return transactions
