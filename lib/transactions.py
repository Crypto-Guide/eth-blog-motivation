from flask import Flask, abort, request
from ethblogapp.models import User
from ethblogapp.database import db_session

import requests
import json

#トランザクションを実行するAPIを叩く関数集

# JS側に新しいuser address を生成してもらい、それを返してもらう。その後、引数にとったuserのaddressと紐づけてDB保存、LINE送信する関数
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


# JSのEther没収TX APIを叩く
def move_user_deposit(address):
    return 0


# JSのロック解除TX APIを叩く
def return_user_deposit(address):
    return 0


# 最近登録したUserのアドレスを指定して、getbalanceしてそのbalanceを返すJS側の関数を叩く
def check_deposit(address):
    return 0