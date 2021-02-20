from strategies.test_strategy import TestStrategy
from strategies.golden_cross import GoldenCross
from strategies.buy_hold import BuyHold


strategies = {
    "test_strategy": TestStrategy,
    "golden_cross": GoldenCross,
    "buy_hold": BuyHold,
}