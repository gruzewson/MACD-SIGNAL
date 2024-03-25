from data import *
import matplotlib.pyplot as plt

def EMA(data, period):
    ema = []
    alpha = 2 / (period + 1)

    denominator = 0
    for i in range(0, period):
        denominator += (1 - alpha) ** i

    for i in range(period, len(data)):
        numerator = 0
        for j in range(0, period):
            numerator += (1 - alpha) ** j * data[i - j]

        ema.append(numerator / denominator)

    return ema

def plot_transaction(dates, prices, trans, title):
    dates_best = dates[(trans[1] - 10):(trans[2] + 10)]
    prices_best = prices[(trans[1] - 10):(trans[2] + 10)]
    plt.plot(dates_best, prices_best)
    plt.scatter(dates[trans[2]], prices[trans[2]], color='green', label='Sell')
    plt.scatter(dates[trans[1]], prices[trans[1]], color='red', label='Buy')
    number_of_dates = 5
    indices = range(0, len(dates_best), len(dates_best) // number_of_dates)
    xticks = [dates_best[i] for i in indices]
    plt.xticks(indices, xticks, rotation=25)
    plt.xlabel('dates')
    plt.ylabel('prices')
    plt.title(title)
    plt.legend()
    plt.show()

def main(graph_title, file_name):
    data, rows = get_data(file_name)
    dates = [row[0] for row in data]
    prices = [row[4] for row in data]
    dates = dates[35:1035]
    prices = prices[35:1035]

    EMA12 = EMA(prices, 12)
    EMA26 = EMA(prices, 26)
    EMA12 = EMA12[14:]
    MACD = [EMA12[i] - EMA26[i] for i in range(len(EMA12))]

    SIGNAL = EMA(MACD, 9)
    MACD = MACD[9:]

    buy = []
    sell = []
    for i in range(len(MACD)):
        if MACD[i] > SIGNAL[i] and MACD[i-1] <= SIGNAL[i-1]:
            buy.append(i)
        elif MACD[i] < SIGNAL[i] and MACD[i-1] >= SIGNAL[i-1]:
            sell.append(i)

    money_start = 1000
    money = money_start
    shares = 0

    dates = dates[-len(MACD):]
    prices = prices[-len(MACD):]

    money_without_macd = money / prices[0]
    money_without_macd = money_without_macd * prices[-1]

    balances = [] #date, price sell, price buy, gained money
    good_transactions = []
    bad_transactions = []
    best_trans = [0, 0, 0]        #balance, index_buy, index_sell
    worst_trans = [999999, 0, 0]  # balance, index_buy, index_sell

    for i in range(len(MACD)):
       if i in buy and money != 0:
           buy_price = prices[i]
           buy_index = i
           gained_money = -money
           shares = money/prices[i]
           money = 0
       elif i in sell and shares != 0:
           sell_price = prices[i]
           balance = sell_price - buy_price
           if balance > 0:
               good_transactions.append((buy_index, i))
               if balance > best_trans[0]:
                   best_trans = [balance, buy_index, i]
           else:
               bad_transactions.append((buy_index, i))
               if balance < worst_trans[0]:
                   worst_trans = [balance, buy_index, i]

           money += shares * prices[i]
           gained_money += money
           balances.append((dates[i], sell_price, buy_price, gained_money))
           shares = 0

    if shares != 0:
        money += shares * prices[-1]
        shares = 0

    #printing balances for table
    #print("Date, Sell Price, Buy Price, Gained Money")
    #for balance in balances:
    #    print(", ".join(map(str, balance)))

    print("-------------------------NO MACD-----------------------")
    print(f"money for start: {money_start}")
    print(f"money with holding stocks whole simulation: {money_without_macd} ({(((money_without_macd - money_start) / money_start * 100) + 100):.2f}%)")
    print(f"profit: {money_without_macd - money_start}")
    print("--------------------------MACD-------------------------")
    print(f"money for start: {money_start}")
    print(f"money at the end: {money} ({(((money - money_start)/money_start * 100)+100):.2f}%)")
    print(f"profit: {money - money_start}")
    print(f"best balance from the simulation: {best_trans[0]}")
    print(f"worst balance from the simulation: {worst_trans[0]}")

    print(f"transactions with good balance: {len(good_transactions)}")
    print(f"transactions with bad balance: {len(bad_transactions)}")
    plot_transaction(dates, prices, best_trans, 'best transaction')
    plot_transaction(dates, prices, worst_trans, 'worst transaction')

    plt.plot(dates, prices)
    plt.title(graph_title)
    number_of_dates = 6
    indices = range(0, len(dates), len(dates) // number_of_dates)
    xticks = [dates[i] for i in indices]
    plt.xticks(indices, xticks, rotation=35)
    plt.xlabel('dates')
    plt.ylabel('prices')
    plt.show()

    plt.plot(dates, prices)
    number_of_dates = 6
    indices = range(0, len(dates), len(dates) // number_of_dates)
    xticks = [dates[i] for i in indices]
    plt.xticks(indices, xticks, rotation=35)
    plt.scatter([dates[i] for i in sell], [prices[i] for i in sell], color='green', label='Sell')
    plt.scatter([dates[i] for i in buy], [prices[i] for i in buy], color='red', label='Buy')
    plt.title(graph_title)
    plt.xlabel('dates')
    plt.ylabel('prices')
    plt.legend()
    plt.show()

    plt.plot(dates, MACD, label='MACD')
    plt.plot(dates, SIGNAL, label='SIGNAL')
    number_of_dates = 6
    indices = range(0, len(dates), len(dates) // number_of_dates)
    xticks = [dates[i] for i in indices]
    plt.xticks(indices, xticks, rotation=35)
    plt.scatter([dates[i] for i in sell], [MACD[i] for i in sell], color='green', label='sell')
    plt.scatter([dates[i] for i in buy], [MACD[i] for i in buy], color='red', label='buy')
    plt.xlabel('dates')
    plt.ylabel('prices')
    plt.title('MacD')
    plt.legend()
    plt.show()

main('DINOPL', 'dnp_d.csv')
main('WIG20', 'wig20_d.csv')