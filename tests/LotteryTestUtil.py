from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.wallet.wallet import KeyWallet
from iconsdk.builder.call_builder import CallBuilder
from iconsdk.builder.transaction_builder import TransactionBuilder, CallTransactionBuilder , MessageTransactionBuilder , CallTransaction
from iconsdk.signed_transaction import SignedTransaction
from time import sleep


class LotteryTestUtil:

    def __init__(self, _keystore_path:str, _keystore_pw:str,
                 _node_uri: str, _lottery_score_address: str,
                 _network_id:int):
        self.wallet = KeyWallet.load(_keystore_path, _keystore_pw)
        self.tester_addr = self.wallet.get_address()
        self.icon_service = IconService(HTTPProvider(_node_uri))
        self.lottery_score_address = _lottery_score_address
        self.network_id = _network_id

    def set_wallet(self, _keystore_path:str, _keystore_pw:str):
        self.wallet = KeyWallet.load(_keystore_path, _keystore_pw)
        self.tester_addr = self.wallet.get_address()

    def get_total_prize(self) -> str:
        tester_addr = self.wallet.get_address()
        call = CallBuilder().from_(tester_addr) \
            .to(self.lottery_score_address) \
            .method("get_total_prize") \
            .build()
        result = self.icon_service.call(call)
        return "get_total_prize:" + result

    def get_participants(self) -> str:
        tester_addr = self.wallet.get_address()
        call = CallBuilder().from_(tester_addr) \
            .to(self.lottery_score_address) \
            .method("get_participants") \
            .build()
        result = self.icon_service.call(call)
        return "get_participants:" + result

    def get_luckynums(self) -> str:
        tester_addr = self.wallet.get_address()
        call = CallBuilder().from_(tester_addr) \
            .to(self.lottery_score_address) \
            .method("get_luckynums") \
            .build()
        result = self.icon_service.call(call)
        return "get_luckynums:" + result

    def buy_lottery_ticket(self, luckynum:str, keyword:str) -> str:

        icx_value = 100

        # it's default value is None when using the builder so need to init the instance directly
        # transaction = CallTransactionBuilder()\
        #     .from_(self.tester_addr) \
        #     .to(self.lottery_score_address) \
        #     .value(icx_value) \
        #     .step_limit(2000000) \
        #     .nid(self.network_id) \
        #     .method("buy_lottery_ticket") \
        #     .params({"my_lucky_numbers": luckynum, "lucky_keyword": keyword}) \
        #     .build()

        transaction = CallTransaction(self.tester_addr,self.lottery_score_address,
                                      icx_value,2000000,self.network_id,None,None,None,
                                      "buy_lottery_ticket",
                                      {"my_lucky_numbers": luckynum, "lucky_keyword": keyword})

        signed_transaction = SignedTransaction(transaction, self.wallet)
        tx_hash = self.icon_service.send_transaction(signed_transaction)


        sleep(10)

        result = self.icon_service.get_transaction_result(tx_hash)
        return "buy_lottery_ticket:" + str(result)

    def draw_winner(self) -> str:

        transaction = CallTransactionBuilder()\
            .from_(self.tester_addr) \
            .to(self.lottery_score_address) \
            .step_limit(2000000) \
            .nid(self.network_id) \
            .method("draw_winner") \
            .build()

        signed_transaction = SignedTransaction(transaction, self.wallet)
        tx_hash = self.icon_service.send_transaction(signed_transaction)

        sleep(10)

        result = self.icon_service.get_transaction_result(tx_hash)
        return "draw_winner:" + str(result)

    def get_balance(self, addr:str):
        return "get_balance:" + str(self.icon_service.get_balance(addr)) \
               + "(" + str(addr) + ")"


    # ##########################for test################################
    def get_winning_num(self) -> str:
        tester_addr = self.wallet.get_address()
        call = CallBuilder().from_(tester_addr) \
            .to(self.lottery_score_address) \
            .method("get_winning_num") \
            .build()
        result = self.icon_service.call(call)
        return "get_winning_num:" + result

    def get_winners(self) -> str:
        tester_addr = self.wallet.get_address()
        call = CallBuilder().from_(tester_addr) \
            .to(self.lottery_score_address) \
            .method("get_winners") \
            .build()
        result = self.icon_service.call(call)
        return "get_winners:" + result

    def set_winning_num(self, winnum:str) -> str:
        transaction = CallTransactionBuilder() \
            .from_(self.tester_addr) \
            .to(self.lottery_score_address) \
            .step_limit(2000000) \
            .nid(self.network_id) \
            .method("set_winning_num") \
            .params({"winnum": winnum}) \
            .build()

        signed_transaction = SignedTransaction(transaction, self.wallet)
        tx_hash = self.icon_service.send_transaction(signed_transaction)

        sleep(10)

        result = self.icon_service.get_transaction_result(tx_hash)
        return "draw_winner:" + str(result)

