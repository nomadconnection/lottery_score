# Lottery SCORE
The Simplest yet completely legitimate lottery SCORE

```
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

    def on_install(self) -> None:
        super().on_install()
        self._winningNum.set('tech_sup')

    def on_update(self) -> None:
        super().on_update()

```
- `_winningNum` :  A storage for a number  to be a source to make lottery's winning numbers, The number changed at every single participation transaction
- `_participants` : A storage for participants list
- `_luckynum_storage` : A storage for participants's lucky numbers

# How to participate
If you want to participate , first of all , deploy this project to your blockchain network and send json file like the below
```
{
  "jsonrpc": "2.0",
  "method": "icx_call",
  "params": {
    "from": "hx1e90db3149d686a7106da0dd2911e6114dba00ba",
    "to": "cx72adfe98f0c86b1ea74aa625d92e30c206b262b3",
    "value":"0x100",
    "dataType": "call",
    "data": {
      "method": "buy_lottery_ticket",
      "params": {
	      "my_lucky_numbers":"11223344556677",
	      "lucky_keyword":"gfdgfd"
      }
    }
  },
  "id": 1
}
```
- You need to chainge `from` , `to` , `my_lucky_numbers` , `lucky_keyword` values in context
- `from` : Wallet address to be participated
- `to` : Deployed SCORE's address
- `my_lucky_numbers` : A number to be matched to lottery winning numbers , the number is split up to  seven numbers of two digits , for example, if you write "11223344556677" like the above, this number will be recognized as "11" "22" "33" "44" "55" "66" "77"
- `lucky_keyword` : A source keyword to be used for making a number to be set in `_winningNum` storage


# Structure
Please, Refer to [Github](https://github.com/nomadconnection/lottery_score) if you want full source codes
When you try to participate , The below function will be called
```
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
```
- you need 100 icx in decimal
- when a new participant is not in the `_participants` storage, it's added
- `my_lucky_numbers` will be saved linked to participant's address(key) in `_luckynum_storage` , if the participant tries to participate more than twice , it will be added with `,`(seperator)
- `self.create_keynums(lucky_keyword)` creates new number to be set in `_winningNum` storage

After then deployer can call `draw_winner` 
```
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
            elif cur_score == score:
                winners.append(participant)

    # 3. give back winning prize to winner(s)
    balance = int(self.icx.get_balance(self.address))

    prize = int(balance/len(winners))
    for winner in winners:
        self.icx.transfer(winner, prize)
    self.clear()
```
- `self.is_owned()` : Only deployer can run this function
- First for statement : Make sure there is no duplication in lottery winning numbers
- Second for statement : Search for participant(s) who has numbers that matched most to the created lottery winning numbers
- Then winning prize will be transferred to the winner(s)

# Run test 
- Testcase uses python sdk. You need to install python sdk to run the test.
```
$ pip3 install iconsdk
```
- Go to the tests folder, open test.py, and change the global variables.
```
├── README.md
├── __init__.py
├── lottery_score.py
├── package.json
├── tests
│   ├── LotteryTestUtil.py
│   ├── __pycache__
│   │   └── LotteryTestUtil.cpython-36.pyc
│   ├── keystore_test1
│   ├── test.py
│   ├── test1
│   └── test2
└── ttttt.py


```
Use the actual SCORE addresses.To run the test , keystores should have a positive amount of ICX. Deploy the lottery_score contract with -k `keystore_test1` option, then you can run `draw_winner` function If you test on T-Bears, use the default node_uri. If test on other network, change the node_uri and network_id accordingly.
```
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
```

- Run the test
```
$ python3 test.py
....
----------------------------------------------------------------------
Ran 4 tests in 20.369s

OK
```