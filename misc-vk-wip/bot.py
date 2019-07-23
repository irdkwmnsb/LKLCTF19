import vk.api, json, requests
from secret import GROUP_ID, API_TOKEN

bot = vk.api.API(vk.api.Session(access_token=API_TOKEN))

lp = bot.messages.getLongPollServer(group_id=GROUP_ID, v='5.78')

blacklist = set()

while True:
    r = requests.get("https://%s?act=a_check&key=%s&ts=%s&wait=25"%(lp['server'], lp['key'], lp['ts'])).json()
    if 'failed' in r:
        lp = bot.messages.getLongPollServer(group_id=GROUP_ID, v='5.78')
        continue
    lp['ts'] = r['ts']
    for event in r['updates']:
        if event[0] == 4:
            msg_id = event[1]
            msg = bot.messages.getById(message_ids=msg_id, v='5.78')['items'][0]
            if msg['out']: continue
            if msg['user_id'] not in blacklist:
                blacklist.add(msg['user_id'])
                bot.messages.send(peer_id=msg['user_id'], message='Пожалуйста, подождите. Вам ответит сотрудник службы поддержки', payload=json.dumps({"flag": "LKLCTF{h1dd3n_me74d4ta}"}), v='5.78')
