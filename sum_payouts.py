import csv
from decimal import Decimal
import glob
import sys


EXCHANGE_RATE = Decimal('1.3415')


def main():
    file_path = '{}/*.csv'.format(sys.argv[1])

    sum = Decimal('0')
    for filename in glob.glob(file_path):
        print(filename)
        with open(filename) as file:
            reader = csv.DictReader(file)
            for row in reader:
                sum += Decimal(row['Payout Amount'])

    cad = sum * EXCHANGE_RATE
    results = '{} USD, {} CAD'.format(sum, cad)
    print(results)


if __name__ == "__main__":
    main()
