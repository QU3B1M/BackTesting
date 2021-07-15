import backtrader as bt


class TheThirdCandle(bt.Strategy):
    """
    A Class to implement a Triple Candlestick Pattern called 'The Third Candle'.
    """

    params = (
        # Loss and Profit percentages.
        ("loss_pct", "30"),
        ("profit_pct", "30"),
    )

    def __init__(self):
        """Initialize all the required attributes."""
        self.stochastic = bt.indicators.Stochastic()
        self.candles_after_position = 0

    def log(self, txt, dt=None):
        """Logging function for this strategy."""
        dt = dt or self.datas[0].datetime.date(0)
        print("%s, %s" % (dt.isoformat(), txt))

    def notify_order(self, order):
        """Logs the order status."""

        # If the order status is Submitted or Accepted there is nothing to do here.
        if order.status in [order.Submitted, order.Accepted]:
            return

        # If Completed then log the kind of order with the price.
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    "BUY EXECUTED, Price: {0:8.2f}, Size: {1:8.2f}, Cost: {2:8.2f}, Comm: {3:8.2f}".format(
                        order.executed.price,
                        order.executed.size,
                        order.executed.value,
                        order.executed.comm,
                    )
                )
            elif order.issell():
                self.log(
                    "SELL EXECUTED,  Price: {0:8.2f}, Size: {1:8.2f}, Cost: {2:8.2f}, Comm: {3:8.2f}".format(
                        order.executed.price,
                        order.executed.size,
                        order.executed.value,
                        order.executed.comm,
                    )
                )

        # If the order fails also logs it.
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order Canceled/Margin/Rejected")

    def next(self):
        """Applies the algorithm to find the pattern and generate the position."""
        if not self.position:

            # Look if The Third Candle pattern mathes.
            if self.the_third_candle_bullish():
                # Set the price.
                price = self.data.open[0]
                self.buy(price=price)

                # Sets the attributes needed for the sale.
                self.candles_after_position = 0
                self.take_profit = self.set_take_profit(price)
                self.stop_loss = self.set_stop_loss(price)

        else:
            # Sells if the price surpases the Take Profit.
            if self.take_profit <= self.data.high[0]:
                price = self.take_profit
                self.sell(price=price)

            # Or if the price goes under the Stop Loss.
            elif self.stop_loss >= self.data.low[0]:
                price = self.stop_loss
                self.sell(price=price)

            # And its better if The Third Candle pattern matches.
            elif self.candles_after_position > 5:
                if self.the_third_candle_bearish():
                    price = self.data.close[0]
                    self.sell(price=price)

        # Counter used to know when to sell
        self.candles_after_position += 1

    # ---- Helpers ----

    def the_third_candle_bullish(self) -> bool:
        """Evaluates if The Third Candle bullish pattern matches."""
        return (
            not self.candles_are_positive((-2,))
            # The stochastic indicator should be Bullish
            and self.stochastic[-2] < self.stochastic[-1]
            and self.stochastic[-1] < self.stochastic[0]
            # The first candle (-2) low should be the lower.
            and self.data.low[-2] > self.data.low[-1]
            and self.data.low[-1] < self.data.low[-0]
            and self.candles_are_positive((-1, 0))
        )

    def the_third_candle_bearish(self) -> bool:
        """Evaluates if the bearish pattern matches"""
        return (
            self.candles_are_positive((-2,))
            # The stochastic indicator should be Bearish
            and self.stochastic[-2] > self.stochastic[-1]
            and self.stochastic[-1] > self.stochastic[0]
            # The first candle (-2) high should be the higher.
            and self.data.high[-2] < self.data.high[-1]
            and self.data.high[-1] > self.data.high[-0]
            and not self.candles_are_positive((-1, 0))
        )

    def candles_are_positive(self, candles: tuple) -> bool:
        """Validates that the candlesticks are positives"""
        try:
            for candle in candles:
                assert (
                    self.data.close[candle - 1] < self.data.close[candle]
                    and self.data.open[candle] < self.data.close[candle]
                )
            return True
        except:
            return False

    def set_take_profit(self, price: float) -> float:
        """Sets the Take Profit using as percentaje the param profit_pct."""
        return (int(self.params.profit_pct) / 100) * price + price

    def set_stop_loss(self, price: float) -> float:
        """Sets the Stop Loss using as percentaje the param loss_pct."""
        return price - (int(self.params.loss_pct) / 100) * price
