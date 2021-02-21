from strategies import strategies
import backtrader as bt
import argparse
import sys
import os


main_path = os.path.dirname(os.path.abspath(sys.argv[0]))
datapath = os.path.join(main_path, "dataset/syp.csv")

data = bt.feeds.YahooFinanceCSVData(
    dataname=datapath,
    reverse=False,
)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("strategy", help="Which strategy to run", type=str)
    args = parser.parse_args()

    if not args.strategy in strategies:
        print(f"Invalid strategy, must be one of {strategies.keys()}")
        sys.exit()

    cerebro = bt.Cerebro()

    cerebro.broker.set_cash(1000000)
    cerebro.adddata(data)
    cerebro.addstrategy(strategies[args.strategy])

    cerebro.run()
    cerebro.plot()
