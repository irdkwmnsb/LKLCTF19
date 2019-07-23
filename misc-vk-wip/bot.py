import vkapi, json, requests
from secret import GROUP_ID, API_TOKEN

bot = vkapi.API(API_TOKEN)

lp = bot.messages.getLongPollServer(group_id=GROUP_ID).response

blacklist = set()

while True:
    r = requests.get("https://%s?act=a_check&key=%s&ts=%s&wait=25"%(lp.server, lp.key, lp.ts)).json()
    if 'failed' in r:
        lp = bot.messages.getLongPollServer(group_id=GROUP_ID).response
        continue
    lp.ts = r['ts']
    for event in r['updates']:
        if event[0] == 4:
            msg_id = event[1]
            msg = bot.messages.getById(message_ids=msg_id).response.vk_items[0]
            if msg.out: continue
            if msg.user_id not in blacklist:
                blacklist.add(msg.user_id)
                bot.messages.send(peer_id=msg.user_id, message='Пожалуйста, подождите. Вам ответит сотрудник службы поддержки', payload=json.dumps({"flag": "LKLCTF{h1dd3n_me74d4ta}"}))
