from flask import Flask, abort, request
from ethblogapp.models import User
from ethblogapp.database import db_session

import requests
import json

#トランザクションを実行するAPIを叩く関数集

# JS側に新しいuser address を生成してもらい、それを返してもらう。その後、引数にとったuserのaddressと紐づけてDB保存、LINE送信する関数
# wallet_create 引数なし、private_key, address返す
def get_new_user_address(line_id):
    address = "0xtest" # JS側API叩いた返り値

    if address is None:
        abort(404)
    content = User.query.filter_by(line_id=line_id).first()

    if content is None:
        raise Exception('This user has not register on line.')
    else:
        content.address = address

    db_session.add(content)
    db_session.commit()

    return address

# Userのaddressからデポジットコントラクトに各データと共に送金する関数
# blog url, デポジット額(全額), expiredAt を引数
# を返す
def deposit_user_eth():
    return 0



# JSのEther没収TX APIを叩く

def remove_user_deposit(address):
    return 0


# JSのロック解除TX APIを叩く
def return_user_deposit(address):
    return 0


# 最近登録したUserのアドレスを指定して、getbalanceしてそのbalanceを返すJS側の関数を叩く
def check_deposit(address):
    #addressを引数にしてcurl投げる
    current_balance = 100 #返ってきたBalanceの値

    if current_balance == 0 or current_balance is None:
        return False
    else:
        user = User.query.filter_by(address=address).first()
        # deposit_user_eth(user.url, user.target_date, current_balance)
        print(user.url)
        print(user.target_date)
        return True