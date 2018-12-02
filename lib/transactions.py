from flask import Flask, abort, request
from ethblogapp.models import User
from ethblogapp.database import db_session

import requests
import json

#トランザクションを実行するAPIを叩く関数集

base_url = 'https://32f940b4.ngrok.io'

# JS側に新しいuser address を生成してもらい、それを返してもらう。その後、引数にとったuserのaddressと紐づけてDB保存、LINE送信する関数
# wallet_create 引数なし、private_key, address返す
def get_new_user_address(line_id):
    req = requests.get(base_url + '/wallet/create')
    req = req.json()
    print(req)

    address = req['address']
    # private_key = req['privateKey']

    if address is None:
        abort(404)
    content = User.query.filter_by(line_id=line_id).first()

    if content is None:
        raise Exception('This user has not register on line.')
    else:
        content.address = address

    db_session.add(content)
    db_session.commit()

    return req

# Userのaddressからデポジットコントラクトに各データと共に送金する関数
# blog url, デポジット額(全額), expiredAt を引数
# を返す
def deposit_user_eth(address):
    user = User.query.filter_by(address=address).first()
    blog_url = user.url
    expired_at = user.target_date.timestamp
    print(expired_at)
    private_key = "0x2027e44f9c45707dd42d9ba00d1ea2cb7d09df6808839dd49066e6b51a3677bd"

    params = {'address': "0x1bd3f22c1468dd610a9bE0592A3beF4B9c0650dD"}
    req = requests.get(base_url + '/getbalance', params=params)

    current_balance = req.json()['balance']

    req = requests.post(base_url + '/promise/register',
                        json.dumps({
                            'blogUrl': blog_url,
                            'expiredAt': expired_at,
                            'fromAddress': address,
                            'value': current_balance - 0.5,
                            'privateKey': private_key
                        }),
                        headers={'Content-Type': 'application/json'}
                        )
    print(req.json())

    if req.status_code ==  400:
        return False


# JSのロック解除TX APIを叩く
def return_user_deposit(address):
    user = User.query.filter_by(address=address).first()
    # private_key = user.private_key
    private_key = "0x2027e44f9c45707dd42d9ba00d1ea2cb7d09df6808839dd49066e6b51a3677bd"
    req = requests.post(base_url + '/promise/achieve',
                        json.dumps({
                            'fromAddress': address,
                            'privateKey': private_key
                        }),
                        headers={'Content-Type': 'application/json'}
                        )
    print(req.json())


# JSのEther没収TX APIを叩く
def remove_user_deposit(address):
    user = User.query.filter_by(address=address).first()
    # private_key = user.private_key
    private_key = "0x2027e44f9c45707dd42d9ba00d1ea2cb7d09df6808839dd49066e6b51a3677bd"
    req = requests.post(base_url + '/promise/break',
                        json.dumps({
                            'fromAddress': address,
                            'privateKey': private_key
                        }),
                        headers={'Content-Type': 'application/json'}
                        )
    print(req.json())


# 最近登録したUserのアドレスを指定して、getbalanceしてそのbalanceを返すJS側の関数を叩く
def check_deposit(address):
    #addressを引数にしてcurl投げる
    params = { 'address': address }
    req = requests.get(base_url + '/getbalance', params=params)

    current_balance = req.json()['balance']
    print(current_balance)

    if current_balance <= 0.5 or current_balance is None:
        return False
    else:
        user = User.query.filter_by(address=address).first()
        res = deposit_user_eth(address)
        if res == False:
            return False

        return True