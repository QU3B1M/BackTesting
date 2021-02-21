import backtrader as bt
import backtrader.indicators as btind


class TrixIndicator(bt.Indicator):

    lines = ("trix",)
    params = (("period", 15),)

    def __init__(self):
        ema1 = btind.EMA(self.data, period=self.p.period)
        ema2 = btind.EMA(ema1, period=self.p.period)
        ema3 = btind.EMA(ema2, period=self.p.period)

        self.lines.trix = 100.0 * (ema3 - ema3(-1)) / ema3(-1)
