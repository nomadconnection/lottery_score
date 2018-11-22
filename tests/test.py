from tests.LotteryTestUtil import LotteryTestUtil
import unittest


node_uri = "http://localhost:9000/api/v3"
network_id = 3
lottery_score_address = "cx72adfe98f0c86b1ea74aa625d92e30c206b262b3"
keystore_path = "./keystore_test1"
keystore_pw = "test1_Account"
keystore_path2 = "./test1"
keystore_pw2 = "11qqWW@@"
keystore_path3 = "./test2"
keystore_pw3 = "11qqWW@@"
lt = LotteryTestUtil(keystore_path, keystore_pw, node_uri, lottery_score_address,
                     network_id)
# print(dd.draw_winner())


class TestCases(unittest.TestCase):
    # def test_dsadafdafs(self):
    #     print(lt.set_winning_num("11223344556612"))
    #     print(lt.get_winning_num())

    # 1. one participant case
    def test_case_one(self):
        print('1. ##########################################################')
        print('#####################info####################################')
        print(lt.get_total_prize())
        print(lt.get_participants())
        print(lt.get_luckynums())
        print(lt.get_balance(lt.wallet.get_address()))
        print(lt.get_balance(lottery_score_address))

        print('#####################buy ticket###############################')
        print(lt.buy_lottery_ticket("11223344556612", "key"))

        print('#####################after buy ticket#########################')
        print(lt.get_total_prize())
        print(lt.get_participants())
        print(lt.get_luckynums())
        print(lt.get_balance(lt.wallet.get_address()))
        print(lt.get_balance(lottery_score_address))

        print('#####################after draw##############################')
        lt.set_wallet(keystore_path2 , keystore_pw2)
        lt.draw_winner()
        print(lt.get_winning_num())
        print(lt.get_winners())
        lt.set_wallet(keystore_path, keystore_pw)
        lt.draw_winner()
        print(lt.get_balance(lt.wallet.get_address()))
        print(lt.get_balance(lottery_score_address))
        print('###############################################################')

    def test_case_two(self):
        print('2. ############################################################')
        print('#####################info####################################')
        lt.set_wallet(keystore_path, keystore_pw)
        lt.draw_winner()
        print(lt.get_total_prize())
        print(lt.get_participants())
        print(lt.get_luckynums())
        print(lt.get_balance(lt.wallet.get_address()))
        print(lt.get_balance(lottery_score_address))

        print('#####################buy ticket###############################')
        lt.set_wallet(keystore_path, keystore_pw)
        print(lt.buy_lottery_ticket("11223344556612", "key"))
        lt.set_wallet(keystore_path2, keystore_pw2)
        print(lt.buy_lottery_ticket("11223344556613", "key"))
        print(lt.buy_lottery_ticket("11223344556613", "key"))

        lt.set_winning_num("11223344556612")

        print('#####################after buy ticket#########################')
        print(lt.get_total_prize())
        print(lt.get_participants())
        print(lt.get_luckynums())
        lt.set_wallet(keystore_path2, keystore_pw2)
        print(lt.get_balance(lt.wallet.get_address()))
        lt.set_wallet(keystore_path, keystore_pw)
        print(lt.get_balance(lt.wallet.get_address()))
        print(lt.get_balance(lottery_score_address))

        print('#####################after draw##############################')
        lt.set_wallet(keystore_path2, keystore_pw2)
        lt.draw_winner()
        print(lt.get_winning_num())
        print(lt.get_winners())
        print(lt.get_balance(lt.wallet.get_address()))
        lt.set_wallet(keystore_path, keystore_pw)
        print(lt.get_balance(lt.wallet.get_address()))
        print(lt.get_balance(lottery_score_address))
        print('##########################################################')

if __name__ == '__main__':
    unittest.main()