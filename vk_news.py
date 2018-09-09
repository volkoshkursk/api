from time import *
from all_skips import *
from all_search import *

def message(api, messages, frozen, uids, text, cache, attachment = []): #uids < 100 штук, attachments < 10
	send = []
#	cache = None
	for i in uids:
		n = search(messages, i, 0, len(messages), False)
		if n == None:
			messages.append(vk_message(i, time()))
			messages.sort(key = lambda x: x.uid)
			send.append(i)
		else:
			if messages[n].check():
				if not(messages[n].msg_warning()):
					send.append(i)
					messages[n].new(time())
				else:
					api.messages.send(user_id = i, message = 'В целях соответствия политике сайта Вконтакте мы ограничиваем количество сообщений робота пользователю. Вы достигли лимита ответов робота и дальнейшая работа будет приостановлена на 1 час')
					cache = (i, text, attachment)
					messages[n].new(time())
					frozen.add(i)
			else:
				frozen.add(i)
				cache.append(i, text, attachment)
	for i in range(0, len(attachment) - 10, 10):
		if len(uids) > 1:
			api.messages.send(user_ids = ','.join(uids), message = text, attachment = ','.join(vk_enc(attachment[i:i+10])))
		else:
			api.messages.send(user_id = uids[0], message = text, attachment = ','.join(vk_enc(attachment[i:i+10])))
	else:
		if len(uids) > 1:
			api.messages.send(user_ids = ','.join(uids), message = text)
		else:
			api.messages.send(user_id = uids[0], message = text)

	return (messages, frozen, cache)
	
def check_cache(cache, api, messages, frozen):
	new_cache = []
	for i in cache:
		(messages, frozen, cache1) = message(api, messages, frozen, i[0], i[1])
	return (messages, frozen, cache1)