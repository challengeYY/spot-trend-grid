import requests,json

# windows
from app.authorization import dingding_token, recv_window,api_secret,api_key
from app.HuobiAPI import HuobiAPI
# linux
# from app.authorization import dingding_token

class Message:
    def show_accounts(self):
        '''
            展示所有账号
        :return:
        '''
        try:
            res = HuobiAPI(api_key,api_secret).get_accounts()
        except BaseException as e:
            error_info = "报警：账号列表获取失败"
            self.dingding_warn(error_info)
            return res

    def buy_market_msg(self, market, quantity):
        '''
            市价买单
        :param market: 交易对
        :param quantity: 购买的数量
        :return:
        '''
        try:
            res = HuobiAPI(api_key,api_secret).buy_market(market, quantity)
            if type(res)==int and res>10000*10000*10000:
                buy_info = "报警：币种为：{cointype}。买单量为：{num}".format(cointype=market,num=quantity)
                print(buy_info)
                self.dingding_warn(buy_info)
                return res
            else:
                error_info = "报警：币种为：{cointype},买单失败.{info}".format(cointype=market, info=res)
                self.dingding_warn(error_info)
        except BaseException as e:
            print("-------buy报错信息------")
            print(str(e)) # 报错内容输出到 nohup,out
            error_info = "报警：币种为：{cointype},买单失败.{info}".format(cointype=market,info=str(e))
            self.dingding_warn(error_info)
            return error_info

    def buy_limit_msg(self, market, quantity,price):
        '''
            限价买单
        :param market: 交易对
        :param quantity: 购买的数量
        :param price : 挂单价格
        :return:
        '''
        try:
            res = BinanceAPI(api_key,api_secret).buy_limit(market, quantity,price)
            if 'orderId' in res:
                buy_info = "报警：币种为：{cointype}。买单量为：{num}.买单价格为：{price}".format(cointype=market,num=quantity,price=float(res['fills'][0]['price']))
                self.dingding_warn(buy_info)
                return res
            else:
                error_info = "报警：币种为：{cointype},买单失败.{info}".format(cointype=market, info=res)
                self.dingding_warn(error_info)
        except BaseException as e:
            print("-------报错信息------")
            print(BaseException) # 报错内容输出到 nohup,out
            error_info = "报警：币种为：{cointype},买单失败.{info}".format(cointype=market,info=str(e))
            self.dingding_warn(error_info)
            return error_info

    def sell_market_msg(self,market, quantity,profit_usdt=0):
        '''
           市价卖单
        :param market:交易对
        :param quantity: 数量
        :param rate: 价格
        :return:
        '''
        try:
            print(4343)
            res = HuobiAPI(api_key,api_secret).sell_market(market, quantity)
            if type(res)==int and  res>10000*10000*10000:
                buy_info = "报警：币种为：{cointype}。卖单量为：{num}。预计盈利{profit_num}U".format(cointype=market,num=quantity,profit_num=round(profit_usdt,2))
                print(buy_info)
                self.dingding_warn(buy_info)
                return res
            else:
                error_info = "报警：币种为：{cointype},卖单失败.{info}".format(cointype=market, info=res)
                self.dingding_warn(error_info)

        except BaseException as e:
            print("-------sell报错信息------")
            print(str(e)) # 报错内容输出到 nohup,out
            error_info = "报警：币种为：{cointype},卖单失败.{info}".format(cointype=market,info=str(e))
            self.dingding_warn(error_info+str(res))
            return error_info



    def sell_limit_msg(self,market, quantity,price,profit_usdt=0):
        '''
        限价卖单
        :param market:交易对
        :param quantity: 数量
        :param price: 价格
        :return:
        '''
        try:
            res = BinanceAPI(api_key,api_secret).sell_limit(market, quantity,price)
            if 'orderId' in res:
                buy_info = "报警：币种为：{cointype}。卖单量为：{num}。预计盈利{profit_num}U".format(cointype=market,num=quantity,profit_num=round(profit_usdt,2))
                self.dingding_warn(buy_info)
                return res
            else:
                error_info = "报警：币种为：{cointype},卖单失败.{info}".format(cointype=market, info=res)
                self.dingding_warn(error_info)

        except BaseException as e:
            print("-------报错信息------")
            print(BaseException) # 报错内容输出到 nohup,out
            error_info = "报警：币种为：{cointype},卖单失败.{info}".format(cointype=market,info=str(e))
            self.dingding_warn(error_info+str(res))
            return res


    def dingding_warn(self,text):
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        api_url = "https://oapi.dingtalk.com/robot/send?access_token=%s" % dingding_token
        json_text = self._msg(text)
        requests.post(api_url, json.dumps(json_text), headers=headers).content

    def _msg(self,text):
        json_text = {
            "msgtype": "text",
            "at": {
                "atMobiles": [
                    "11111"
                ],
                "isAtAll": False
            },
            "text": {
                "content": text
            }
        }
        return json_text

if __name__ == "__main__":
    msg = Message()
