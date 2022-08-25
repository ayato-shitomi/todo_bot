# 必須ライブラリをインポート
import discord
import time
import os
from server import keep_alive


# tokenファイルを読みこみ、内容を返す
# 第一引数にトークンのファイルパスを取る
def getToken(filePath):
    f = open(filePath, 'r', encoding="UTF-8")
    data = f.read()
    f.close()
    return data


# トークンと環境変数等を取得する
TOKEN = os.environ['TOKEN']
SERVER_ID = <サーバID>
TXT_ID = <任意のテキストID>
MY_ID = <任意のユーザーID>
TODO_LIST = "todo.list"
DBGMSG = "BOTはオンラインです。"
print("Success > Got token and SERVER and TEXT ID.")

client = discord.Client()


# クライアントクラスを作成する
@client.event
async def on_ready():
    print("Success > Login.")


done_command_list = ["done", "delete", "del", "d"]


def add_todo(todo):
    f = open(TODO_LIST, "a")
    f.write(todo)
    f.close()


def get_todo():
    f = open(TODO_LIST, "r")
    l = f.readlines()
    f.close()
    return (l)


"""
def done_todo(delete):
    todo_lsit = get_todo()
    delete = "['" + delete + "']\n"
    todo_lsit.remove(delete)
    f = open(TODO_LIST, "w")
    f.write("")
    f.close()
    f = open(TODO_LIST, "a")
    for i in todo_lsit:
        f.write(i)
    f.close()
"""


def done_todo(delete):
    if (delete.isdigit() == False):
        return 1
    todo_lsit = get_todo()
    todo_lsit.pop(int(delete) - 1)
    f = open(TODO_LIST, "w")
    f.write("")
    f.close()
    f = open(TODO_LIST, "a")
    for i in todo_lsit:
        f.write(i)
    f.close()
    return 0


def make_msg(msg):
    show = get_todo()
    show_msg = "\n**__ToDo List__**\n```"
    n = 0
    for i in show:
        n = n + 1
        num = str(n)
        if (n < 10):
            num = "0" + str(n)
        show_msg = show_msg + num + " | " + i[2:-3].replace("', '", " ") + "\n"
    show_msg = show_msg + "```\n" + msg
    return show_msg


def patch_todo(number, index):
    if (number.isdigit() == False):
        return 1
    todo_list = get_todo()
    todo_list[int(number) - 1] = str(index).replace("', '", " ") + "\n"
    f = open(TODO_LIST, "w")
    f.write("")
    f.close()
    f = open(TODO_LIST, "a")
    for i in todo_list:
        f.write(i)
    f.close()
    return 0


# テキストチャンネル周り
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は何もしない
    if message.author.bot:
        return
    if message.channel.id != TXT_ID:
        return
    if message.author.id != MY_ID:
        await message.delete()
        return
    msg = message.content
    args = msg.split()
    # 「/botdbg」コマンド
    if msg == "/botdbg":
        print("Info > " + DBGMSG)
        await message.channel.send(DBGMSG)
    elif args[0] == "/todo":
        print("Info > ToDo command was called.")
        if len(args) <= 2:
            sending_msg = "`" + msg + "`" + " was an invalid argment."
            usage_send = await message.channel.send(sending_msg)
            print("Info > ", sending_msg)
            time.sleep(3)
            await usage_send.delete()
            await message.delete()
            return
        if args[1] == "add" or args[1] == "a":
            print("Info > ToDo-add was called.")
            todo = str(args[2:]) + "\n"
            add_todo(todo)
            await message.channel.purge()
            show_msg = make_msg("Added ToDo :muscle:")
            await message.channel.send(show_msg)
            time.sleep(3)
        elif args[1] in done_command_list:
            print("Info > ToDo-done was called.")
            n = done_todo(args[2])
            if (n == 1):
                await message.channel.purge()
                show_msg = make_msg("Invalid Argment :sunglasses:")
                await message.channel.send(show_msg)
            await message.channel.purge()
            show_msg = make_msg("Done ToDo :yum:")
            await message.channel.send(show_msg)
        elif args[1] == "p":
            print("Info > ToDo-Patch was called.")
            if (len(args) < 4):
                await message.channel.purge()
                show_msg = make_msg("Invalid Argment :sunglasses:")
                await message.channel.send(show_msg)
            else:
                number = args[2]
                index = args[3:]
                n = patch_todo(number, index)
                if (n == 1):
                    await message.channel.purge()
                    show_msg = make_msg("Invalid Argment :sunglasses:")
                    await message.channel.send(show_msg)
                else:
                    await message.channel.purge()
                    show_msg = make_msg("Update ToDo :yum:")
                    await message.channel.send(show_msg)
        # 存在しない`/todo`コマンドの引数の場合
        else:
            sending_msg = "`" + msg + "`" + " was an invalid argment."
            usage_send = await message.channel.send(sending_msg)
            time.sleep(3)
            await usage_send.delete()
            await message.delete()
    else:
        await message.channel.purge()
        show_msg = make_msg(":sunglasses:")
        await message.channel.send(show_msg)


keep_alive()

# クライアントクラスを実行する。
client.run(TOKEN)
