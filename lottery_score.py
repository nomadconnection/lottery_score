from iconservice import *
from iconservice import DictDB

TAG = 'Lottery'


class Lottery(IconScoreBase):

    _WINNINGNUM = 'winning_number'
    _TOTAL_PRIZE = 'total_prize'
    _PARTICIPANTS = 'participants'
    _LUCKYNUM_STORAGE = 'luckynum_storage'

    def __init__(self, db: IconScoreDatabase) -> None:
        super().__init__(db)
        self._winningNum = VarDB(self._WINNINGNUM, db, value_type=str)
        self._participants = ArrayDB(self._PARTICIPANTS, db, value_type=Address)
        self._luckynum_storage = DictDB(self._LUCKYNUM_STORAGE, db, value_type=str)
        # #######only for test #######################
        self.wwww = ''
        # #######only for test #######################

        # ################################
        # self._winners = ArrayDB('winners' , db , value_type=Address)
        # ################################

    def on_install(self) -> None:
        super().on_install()
        self._winningNum.set('tech_sup')

    def on_update(self) -> None:
        super().on_update()
        # self._winningNum.set('tech_sup')

    '''
        get functions
    '''
    @external
    def get_total_prize(self) -> str:
        return str(self.icx.get_balance(self.address))

    @external
    def get_participants(self) -> str:
        re_str = ''
        for idx, participant in enumerate(self._participants):
            re_str += str(idx) + ':' + str(participant) + ' '
        return 'participants are ' + re_str

    @external
    def get_luckynums(self) -> str:

        re_str = ''
        for participant in self._participants:
            re_str += self._luckynum_storage[participant]+'(' + str(participant) + ') '

        return re_str

    '''
        executed when a participant try to participate
        condition:
            1. sendtx's value must be 0x100
            2. when a participant trys more than twice , append the lucky numbers
                subjected after the previous numbers with ','
            3. the lucky numbers subjected must be a string having length of 14
    '''
    @external
    @payable
    def buy_lottery_ticket(self, my_lucky_numbers: str, lucky_keyword: str):
        if self.msg.value != 100 or len(my_lucky_numbers) != 14:
            revert('please , make sure that value is 100 '
                   'and lucky numbers are 14 digits')

        sender = self.msg.sender
        if not self._participants.__contains__(sender):
            self._participants.put(sender)
            self._luckynum_storage.__setitem__(sender, my_lucky_numbers)
        else:
            self._luckynum_storage[sender] += ',' + my_lucky_numbers
        self.create_keynums(lucky_keyword)

    '''
        random number creator 
    '''
    def create_keynums(self, key: str):
        val = str(sha3_256(bytes(key + self._winningNum.get(), 'utf-8'))
                  .hex()).replace('a', '').replace('b', '').replace('c', '')\
            .replace('d', '').replace('e', '').replace('f', '')
        val = str(int((int(val) % 1000000000000000 + 1000000000000000)/3))
        self._winningNum.set(val)

    '''
        draw a winner
        # json_dumps()    object to json
    '''
    @external
    def draw_winner(self):
        # permission check
        self.is_owned()
        # 1. checking the winning number has duplicated number
        # -count : a break for infinite loop
        _list = list()
        for count in range(100):
            flag = False
            _list = self.create_win_num_list()
            # check there is a duplicated number and if so , set a flag True
            for i in range(0, len(_list)):
                flag = self.is_dupplicated(_list, i)
                if flag:
                    break
            # when there is a duplicated number , create a new winning numbers
            if flag:
                self.create_keynums('salt')
                # get out of the infinite loop
                if count == 99:
                    revert('like it\'s in the infinite loop')
            else:
                break
        # 2. checking the score about how many numbers matches lucky nums
        # and draw winners
        winning_nums = _list
        # winning_nums= ['12', '23', '34', '45', '67', '89']
        winners = list()
        score = 0

        for participant in self._participants:
            dict_val_list = self._luckynum_storage[participant].split(',')
            for i in range(0, len(dict_val_list)):
                cur_score = 0
                if winning_nums.__contains__(dict_val_list[i][:2]):
                    cur_score += 1
                if winning_nums.__contains__(dict_val_list[i][2:4]):
                    cur_score += 1
                if winning_nums.__contains__(dict_val_list[i][4:6]):
                    cur_score += 1
                if winning_nums.__contains__(dict_val_list[i][6:8]):
                    cur_score += 1
                if winning_nums.__contains__(dict_val_list[i][8:10]):
                    cur_score += 1
                if winning_nums.__contains__(dict_val_list[i][10:12]):
                    cur_score += 1
                if winning_nums.__contains__(dict_val_list[i][12:14]):
                    cur_score += 1

                if cur_score > score:
                    score = cur_score
                    winners = list()
                    winners.append(participant)
                    # ################################
                    # for winner in self._winners:
                    #     self._winners.pop()
                    # self._winners.put(participant)
                    # ################################
                elif cur_score == score:
                    winners.append(participant)
                    # ################################
                    # self._winners.put(participant)
                    # ################################

        # 3. give back winning prize to winner(s)
        balance = int(self.icx.get_balance(self.address))
        # if there is no one in winners list (but this is not possible in this logic)
        # if len(winners) == 0:
        #     self.clear()
        #     revert('no winner there, prize will be added to next lottery\'s prize')

        prize = int(balance/len(winners))
        for winner in winners:
            self.icx.transfer(winner, prize)
        self.clear()
        # #######only for test #######################
        self.wwww = winners
        # #######only for test #######################

    def create_win_num_list(self) -> list:
        winnum = self._winningNum.get()
        winnum = str(int(winnum) % 100000000000000)
        gap = 0
        if len(winnum) < 14:
            gap = 14 - len(winnum)
        while gap > 0:
            gap -= 1
            winnum = '0' + winnum

        _list = self.create_num_list(winnum)
        return _list

    def create_num_list(self, num_str: str) -> list:
        _list = list()
        _list.append(num_str[:2])
        _list.append(num_str[2:4])
        _list.append(num_str[4:6])
        _list.append(num_str[6:8])
        _list.append(num_str[8:10])
        _list.append(num_str[10:12])
        _list.append(num_str[12:14])
        return _list

    def is_dupplicated(self, _list: list, idx: int) -> bool:
        for i in range(idx+1, len(_list)):
                if _list[idx].__eq__(_list[i]):
                        return True
        return False

    '''
        for fucntions that only deployer can do 
    '''
    def is_owned(self):
        if self.msg.sender != self.owner:
            revert('permission error')

    '''
        fallback for plain transaction 
    '''
    @payable
    def fallback(self):
        Logger.info('fallback is called', TAG)

    @external
    def clear(self):
        for i in range(0, len(self._participants)):
            self._participants.pop()

    # ############################only for test#################################3

    # @external
    # def get_sha256_test(self) -> str:
    #     return str(sha3_256(bytes('1', 'utf-8')).hex())

    @external  # this must not be external after test
    def get_winning_num(self) -> str:
        # return str(self.icx.get_balance(self.address))
        return str(self._winningNum.get())

    @external
    def set_winning_num(self, winnum: str):
        self._winningNum.set(winnum)

    # ################################
    @external
    def get_winners(self) -> str:
        winner_str = ''
        for winner in self.wwww:
            winner_str += str(winner) + ' '
        return winner_str
    # ################################
