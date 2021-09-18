import statistics

# orders = [60.5, -10.3, -20.46, 10]
# orders = [-10.3, -20.46]
orders = [60.5, 10]

average = statistics.mean(orders)

print("The average coffee order price today is $" + str(round(average, 2)))