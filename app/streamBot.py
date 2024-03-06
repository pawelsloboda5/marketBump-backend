import requests
import json



api_key = 'MTIxNDEwNjA0NjQ2MTkwNjk2NA.GeChRC.69zbzxWARdhoantscV_LzSYMJeeM5eJuN_w8PA'
channel_id = '1193011030100557844'

def retireve_messages(channel_id):
    headers = {
        'authorization':'MjExMjcxMDg2MDQwNDE2MjU2.GTaVqT.wmnEajKiytq0bvKvHsxm8hQShGHlaSP4JW7Ieg'
    }
    r = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers=headers)
    jsonn = json.loads(r.text)
    for value in jsonn:
        print(value['content'],'\n')
    #find the most recent message
    return (jsonn[0]['content'])
