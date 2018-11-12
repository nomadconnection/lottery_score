from iconservice import *

TAG = 'lottery_score'


class Lottery(IconScoreBase):


    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)

    def on_install(self, initialSupply: int, decimals: int) -> None:
        super().on_install()
        self._totalPrize
        self._

    def on_update(self) -> None:
        super().on_update()

    @external(readonly=True)
    def name(self) -> str:
        return "SampleToken"
'''branch'''