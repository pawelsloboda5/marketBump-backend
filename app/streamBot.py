import requests
import json



discord_api_key = 'MTIxNDEwNjA0NjQ2MTkwNjk2NA.GeChRC.69zbzxWARdhoantscV_LzSYMJeeM5eJuN_w8PA'
discord_auth_key = 'MjExMjcxMDg2MDQwNDE2MjU2.Gfjysr.QszGgFIoBxbU7cLWvcEcN29ZGIXDdpPYCtFWKE'

def retrieve_messages(channel_id,discord_auth_key):
    headers = {
        'authorization':'MjExMjcxMDg2MDQwNDE2MjU2.GTaVqT.wmnEajKiytq0bvKvHsxm8hQShGHlaSP4JW7Ieg'
    }
    r = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers=headers)
    jsonn = json.loads(r.text)
    for value in jsonn:
        print(value['content'],'\n')
    #find the most recent message
    return (jsonn[0]['content'],jsonn[0]['author']['username'])
