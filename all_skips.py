import logging
def skip(k, link_text, arg, arg2 = '!@!', death = '!@!'):
	while (link_text[k:k+len(arg)] != arg) and (link_text[k:k+len(arg2)] != arg2) and (link_text[k:k+len(death)] != death):
		if k >= len(link_text):
			sk_log = logging.getLogger("all_skips.skip")
			sk_log.info("k >= len(link_text)")
			print('info')
			break
		else:
			k += 1
	if link_text[k:k+len(death)] == death:
		k = len(link_text)
	return k

def skip_back(k, link_text, arg, arg2 = '!@!', death = '!@!'):
	while (link_text[k-len(arg):k] != arg) and (link_text[k-len(arg2):k] != arg2) and (link_text[k-len(death):k] != death):
		if k <= 0:
			sk_log = logging.getLogger("all_skips.skip_back")
			sk_log.info("k <= 0")
			print('info')
			k = 0
			break
		else:
			k -= 1
	if link_text[k-len(death):k] == death:
		k = 0
	return k
	
def skip_s(k, link_text, arg, arg2 = '!@!', death = '!@!'):
	while (link_text[k:k+len(arg)] != arg) and (link_text[k:k+len(arg2)] != arg2) and (link_text[k:k+len(death)] != death):
		if k >= len(link_text):
			sk_log = logging.getLogger("all_skips.skip_s")
			sk_log.info("k >= len(link_text)")
			print('info')
			break
		else:
			k += 1
	return k
	
def skip_not(k, link_text, arg, arg2 = '!@!'):
	while (link_text[k:k+len(arg)] == arg) or (link_text[k:k+len(arg2)] == arg2):
		
		if k >= len(link_text):
			sk_log = logging.getLogger("all_skips.skip_not")
			sk_log.info("k >= len(link_text)")
			print('info')
			break
		k += 1
	return k

def skip_to_int(k, link_text, another = {0}): # another - это множество
	try:
		int(link_text[k])
	except Exception as E:
		t = True
	else:
		t = False
	if k < len(link_text):
		an = not(link_text[k] in another)
	else:
		an = False
	while k < len(link_text) and (t and an):
		try:
			int(link_text[k])
		except Exception as E:
			t = True
		else:
			t = False
		an = not(link_text[k] in another)
		if t and an:
			k += 1
	return k
		
def skip_while_int(k, link_text, another = {0}): # another - это множество
	try:
		int(link_text[k])
	except Exception as E:
		t = False
	else:
		t = True
		
	if k < len(link_text):
		an = link_text[k] in another
	else:
		an = False
#	if k < len(link_text):
#		print(t)
#		print(link_text[k] in another)
	while k < len(link_text) and (t or an):
#		print(t)
#		print(link_text[k] in another)
		try:
			int(link_text[k])
		except Exception as E:
			t = False
			an = link_text[k] in another
			if an:
				k += 1
		else:
			t = True
			k += 1
	return k

def skip_while(k, link_text, another):
	while k < len(link_text) and (link_text[k] in another):
			k += 1
	return k
