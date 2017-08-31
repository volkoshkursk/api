#импорт библиотек для использования URL
import urllib
import urllib.parse
import urllib.request

import logging
import logging.config

import os, vk
from time import *

from all_skips import *

access_token1 = input('input your token:')
active_client = []
all_clients = []
class news:
	def __init__(self, uid):
		self.uid = uid
		self.active = False
		self.sources = []
		self.arg = []
		
	def set_uid(self, uid):
		self.uid = uid
		
	def set_sources_id(self, sources):
		self.sources_id = set(sources)
		
	def set_arg(self, arg = []): 
# заполнение массива аргументов и массива функций
# 
#
		arg.sort(key = lambda x: x[0])
		used = set()
		anti_repeat = [True, True] # для rt защита от повторения: если пользователь выберет категорию новости и общую категорию то без этой переменной и её проверки ему будет выводиться одна и та же категория одного источника дважды
		for i in arg:
			if i[0] == 2:
				self.sources.append(rt)
				self.arg.append([0, 'rus', i[1]])
				if i[1] == '/news':
					anti_repeat[0] = False
				used.add(2)
			elif i[0] == 4:
				self.sources.append(rt)
				self.arg.append([0, 'eng', i[1]])
				if i[1] == '/news':
					anti_repeat[1] = False
				used.add(4)
			elif i[0] == 6:
				self.sources.append(bloomberg_theme)
				self.arg.append([0, i[1]])
				used.add(6)
			elif i[0] == 8:
				self.sources.append(ino_themes)
				self.arg.append([0, i[1]])
				used.add(8)
		for i in self.sources_id.difference(used):
			if i == 1 and anti_repeat[0]:
				self.sources.append(rt)
				self.arg.append([0, 'rus', '/news'])
			elif i == 2:
				self.sources.append(rt)
				self.arg.append([0, 'rus', ''])
			elif i == 3 and anti_repeat[1]:
				self.sources.append(rt)
				self.arg.append([0, 'eng', '/news'])
			elif i == 4:
				self.sources.append(rt)
				self.arg.append([0, 'eng', ''])
			elif i == 5:
				self.sources.append(bloomberg_latest)
				self.arg.append([0, 'europe']) # надо сделать выбор региона
			elif i == 6:
				self.sources.append(bloomberg)
				self.arg.append([0, 'europe']) # надо сделать выбор региона
			elif i == 7:
				self.sources.append(ino)
				self.arg.append([0])
			elif i == 8:
				self.sources.append(ino_themes)
				self.arg.append([0], '')
			
		del used
		log = logging.getLogger('root.news_class')
		log.debug(self.arg)
		log.debug(self.sources)
		
	def set_num(self, num):
		for i in range(len(self.arg)):
			self.arg[i][0] = num
		log = logging.getLogger('root.news_class')
		log.debug(self.arg)
		self.active = True
		log.debug('uid: %s', self.uid)
		log.debug('sources id: %s', self.sources_id)
		log.debug('sources: %s', self.sources)
		log.debug('arg: %s', self.arg)
		log.debug('period: %s', self.period)
		log.debug('time: %s', self.time)
		
	def set_period(self, period):
		self.period = period
		self.time = time() - period
		
	def encode(self): 
		out = ''
		for i in self.sources:
			if i == rt:
				out += 'rt'
			elif i == bloomberg:
				out += 'bg'
			elif i == bloomberg_latest:
				out += 'bl'
			elif i == bloomberg_theme:
				out += 'bt'
			elif i == ino:
				out += 'in'
			elif i == ino_themes:
				out += 'it'
		return out
		
	def decode(self,inp):
		for i in range(0, len(inp), 2):
			if inp[i:i+2] == 'rt':
				self.sources.append(rt)
			elif inp[i:i+2] == 'bg':
				self.sources.append(bloomberg)
			elif inp[i:i+2] == 'bl':
				self.sources.append(bloomberg_latest)
			elif inp[i:i+2] == 'bt':
				self.sources.append(bloomberg_theme)
			elif inp[i:i+2] == 'in':
				self.sources.append(ino)
			elif inp[i:i+2] == 'it':
				self.sources.append(ino_themes)
	
	def read(self,inp):
		# чтение сохранённых данных из строки
		arr = inp.split('|')
		self.uid = int(arr[0])
		self.time = float(arr[1])
		self.period = float(arr[2])
		self.decode(arr[3])
		temp = (arr[4][2:len(arr[4]) - 2].split('], ['))
		arr.clear()
		for i in temp:
			arr.append(i.split(', '))
		temp.clear()
		for i in range(len(arr)):
			for j in range(len(arr[i])):
				if j == 0:
					temp.append(int(arr[i][j]))
				else:
					temp.append(arr[i][j][1:len(arr[i][j])- 1])
			self.arg.append(temp.copy())
			temp.clear()
		del temp, arr
		self.active = True
		
	def check(self):
		if self.active and (int(time()) - int(self.time)) >= self.period:
			out = []
			for i in range(len(self.sources)):
				out += self.sources[i](self.arg[i])
			send(self.uid, out)
			self.time = time()
			
	def __le__(self, other):
		now = time()
		if (now - self.time) % period > (now - other.time) % period:
			return False
		else:
			return True
			
	def __ge__(self, other):
		now = time()
		if (now - self.time) % period < (now - other.time) % period:
			return False
		else:
			return True
	def n_print(self):
		if self.active:
			return(str(self.uid) + '|' + str(self.time) + '|' + str(self.period)+ '|'+ self.encode() + '|' + str(self.arg))

def search(arr, el, beg, end, spec = True):
	if len(arr) == 0:
		return None
	if spec:
		i = (end - beg) // 2 + beg
		if end - beg == 1 and arr[beg][0] != el:
			return None
		if el == arr[i][0]:
			return i
		elif el < arr[i][0]:
			return search(arr, el, 0, i)
		else:
			return search(arr, el, i, len(arr))
	else:
		i = (end - beg) // 2 + beg
		if end - beg == 1 and arr[beg].uid != el:
			return None
		if el == arr[i].uid:
			return i
		elif el < arr[i].uid:
			return search(arr, el, 0, i, spec = False)
		else:
			return search(arr, el, i, len(arr), spec = False)

def silly_search(arr, el):
	for i in range(len(arr) - 1, -1, -1):
		if arr[i].uid == el:
			return i
	return None
def open_hyperlink(web_link, code):
	op_hyp = logging.getLogger('root.open_hyperlink')
	op_hyp.debug('link %s opened' , web_link)
	try:
		#попытка открыть страницу
		link_results = urllib.request.urlopen(web_link)
	except Exception as E:
		op_hyp.error(E)
	else:
		try:
			link_text = link_results.read().decode(code)
		except Exception as E:
			op_hyp.error(E)
		return link_text
#print(open_hyperlink('https://api.vk.com/method/messages.getHistory?v=5.41&access_token='+ access_token +'&peer_id=283620276&offset=0&count=10 ' , 'UTF-8'))

def themes(type_): # type: 1 -rt rus, 2 - rt eng, 3 - bloomberg, 4 - inoSMI
# выделяет темы для новостных источников
# возвращает массив с парами ссылка - название
#
	arr = []
	if type_ == 1:
		text = open_hyperlink('http://russian.rt.com/', 'UTF-8')
		k = skip(0, text, '<a class="nav__link nav__link_header  link" href="', death = '<div class="layout__wrapper')+ 50
		while k < len(text):
			j = skip(k, text, '"')
			link = text[k:j]
			k = skip_while(skip(j+1, text, '\n') + 1, text, {' ', '\n'})
			j = skip(k, text, '\n')
			arr.append([text[k:j], link, 2])
			k = skip(j, text, '<a class="nav__link nav__link_header  link" href="', death = '<div class="layout__wrapper')+ 50
	elif type_ == 2:
		#<a class="nav__link
		text = open_hyperlink('http://www.rt.com', 'UTF-8')
		k = skip(0, text, '<a class="nav__link  " href="', death = '<div class="layout__wrapper')+ 29
		while k < len(text):
			j = skip(k, text, '"')
			link = text[k:j]
			k = j + 2
			j = skip(k, text, '<')
			arr.append([text[k:j], link, 4])
			k = skip(j, text, '<a class="nav__link  " href="', death = '<div class="layout__wrapper')+ 29
	elif type_ == 3:
		text = open_hyperlink('http://www.bloomberg.com', 'UTF-8')
		k = skip(1000, text, '<h2 class="bb-that-category__title">Media</h2>') + 46
		k = skip(k, text, 'href="', death = '</ul>') + 6
		while k < len(text):
			j = skip(k, text, '"')
			link = text[k:j]
			k = j + 2
			j = skip(k, text, '<')
			arr.append([text[k:j], link, 6])
			k = skip(j, text, 'href="', death = '</ul>') + 6
	elif type_ == 4:
		text = open_hyperlink('http://www.inosmi.ru', 'UTF-8')
		k = skip(skip(0, text, '<div class="navigator-main-adaptive" id="navigator-main-adaptive-accordion">'),text,'href="', death = '</a></h3><div></div></div><script>') + 6
		while k < len(text):
			j = skip(k, text, '"')
			link = text[k:j]
			k = j + 2
			j = skip(k, text, '<')
			arr.append([text[k:j], link, 8])
			k = skip(j,text,'href="', death = '</a></h3><div></div></div><script>') + 6
	return arr
def rt(arg): # default: num = 0, lang = 'rus', end = '/news'
	num = arg[0]
	lang = arg[1]
	end = arg[2]
	logger = logging.getLogger('root.rt')
	if lang == 'rus':
		text = open_hyperlink('http://russian.rt.com' + end, 'UTF-8')
		out = []
		k = 100
		while text != None and (len(set(out)) < num or num == 0):
			k = skip(k, text, '<a class="link link_color" href="', death ='Сегодня в СМИ') + 33
			if k < len(text):
				j = skip(k, text, '"')
				out.append('http://russian.rt.com' + text[k:j])
				k = j
			else:
				break
	elif lang == 'eng':
		text = open_hyperlink('http://www.rt.com' + end, 'UTF-8')
		out = []
		k = 100
		while text != None and (len(set(out)) < num or num == 0):
			k = skip(k, text, '<a class="link link_hover" href="', death ='</a></strong></div></li></ul><div class="more-links">') + 33
			if k < len(text):
				j = skip(k, text, '"')
				out.append('http://www.rt.com' + text[k:j])
				k = j
			else:
				break
	return set(out)
	
def bloomberg_latest(arg): #default: num = 0, region = 'europe'
	num = arg[0]
	region = arg[1]
	logger = logging.getLogger('root.bloomberg_fast')
	text = open_hyperlink('http://www.bloomberg.com/' + region , 'UTF-8')
	out = []
	k = 100
	while text != None and (len(set(out)) < num or num == 0):
		k = skip(k, text, '<a class="markets-bar-item__link" href="', death ='</span>  </a> </div></div></div> </div> </div></div>') + 40
		if k < len(text):
			j = skip(k, text, '"')
			out.append(text[k:j])
			k = j
		else:
			break
	return set(out)
	
def name(a):
	if a == 1:
		return [['Russia Today (rus)', None]]
	elif a == 2:
		return [['Russia Today (eng)', None]]
	elif a == 3:
		return [['Bloomberg', None]]
	elif a == 4:
		return [['ИноСМИ', None]]

def bloomberg(arg): #default: num = 0, end = 'europe'
	num = arg[0]
	end = arg[1]
	logger = logging.getLogger('root.bloomberg')
	text = open_hyperlink('http://www.bloomberg.com/' + end, 'UTF-8')
	out = set()
	k = 100
	while text != None and (len(out) < num or num == 0):
		k = skip_s(k, text, '<a class="markets-bar-item__link" href="', death ='</span>  </a> </div></div></div> </div> </div></div>') + 40
		if (k < len(text)) and (text[k-40:k+12] != '</span>  </a> </div></div></div> </div> </div></div>'):
			j = skip(k, text, '"')
			out.add(text[k:j])
			k = j
		else:
			break
	while text != None and (len(out) < num or num == 0) and k < len(text):
		k = skip(k, text, '<a href="', death = '</script></body></html>') + 9
		if k < len(text):
			j = skip(k, text, '"')
			logger.debug('* %s *', text[k:j])
			if text[k] == 'h':
				out.add(text[k:j])
			else:
				out.add('http://www.bloomberg.com' + text[k:j])
			k = j
		else:
			break
	return out

def bloomberg_theme(arg):
	num = arg[0]
	end = arg[1]
	out = set()
	logger = logging.getLogger('root.bloomberg')
	if end[0] == 'h':
		text = open_hyperlink(end, 'UTF-8')
	else:
		text = open_hyperlink('http://www.bloomberg.com/' + end, 'UTF-8')
	k = skip(skip(0, text, '<main'), text, 'href="', death = '</main>') + 6
	while text != None and  k < len(text) and (len(out) < num or num == 0):
		j = skip(k, text, '"')
		if k!=j:
			if text[k] == 'h':
				out.add(text[k:j])
			else:
				out.add('http://www.bloomberg.com' + text[k:j])
		k = skip(j, text, 'href="', death = '</main>') + 6
	return out

def ino(arg):
	num = arg[0]
	logger = logging.getLogger('root.inosmi')
	text = open_hyperlink('http://inosmi.ru', 'UTF-8')
	k = skip(100, text, '<div class="index-main-news__article-main-wrapper">', death = '<div class="main main_adaptive main_index-bottom-lg">')
	out = set()
	while text != None and (len(set(out)) < num or num == 0):
		k = skip(k, text, '<a href="', death = '<div class="main main_adaptive main_index-bottom-lg">') + 9
		if k < len(text):
			j = skip(k, text, '"')
			if text[j-4:j] == 'html':
				out.add('http://inosmi.ru' + text[k:j])
			k = j
		else:
			break
	return out

def ino_themes(arg):
	num = arg[0]
	end = arg[1]
	logger = logging.getLogger('root.inosmi_themes')
	text = open_hyperlink('http://inosmi.ru' + end, 'UTF-8')
	out = set()
	k = skip(100, text, '<div class="main__row">', death = '<section class="most-popular most-popular_most-viewed">')
	while text != None and (len(set(out)) < num or num == 0):
		k = skip(k, text, '<a href="', death = '<section class="most-popular most-popular_most-viewed">') + 9
		if k < len(text):
			j = skip(k, text, '"')
			if text[j-4:j] == 'html':
				out.add('http://inosmi.ru' + text[k:j])
			k = j
		else:
			break
	return out

def head(i):
# получение заголовка новости
	text = open_hyperlink(i, 'UTF-8')
	return text[skip(10, text, '<title>') + 7 : skip(10, text, '</title>')]
		
def send(user_id, arr):
	for i in arr:
		try:
			api.messages.send(user_id = user_id, message = head(i) + '\n'+ i)
		except Exception as E:
			logger = logging.getLogger('root.send')
			logger.error('%s with ' + i, E)
			
def receive():
	global active_client
	logger = logging.getLogger('root.receive')
#	sleep(0.3)
	try:
		messages = api.messages.getDialogs(unanswered = 1)
		logger.debug(messages)
	except Exception as E:
		logger.error(E)
	try:
		for i in messages:
			if type(i) is int:
				continue
#			print(messages)
			user_id = i['uid']
			api.messages.markAsAnsweredDialog(peer_id = user_id,answered = 1)
			api.messages.markAsRead(peer_id = user_id)
			if i['body'][1:9] == 'астроить' or i['body'][1:3] == 'et' or i['body'][1:9] == 'астройка':
				num = search(all_clients, user_id, 0, len(all_clients), spec = False)
				if num != None:
					all_clients.pop(num)
				del num
				all_clients.append(news(user_id))
				setting_info(0, user_id)
				active_client.append([user_id, 2])
			elif i['body'][1:4] == 'top' and user_id == 283620276:
				logger.info('programm stopped')
				print('stop')
				save()
				return True
			elif i['body'][1:6] == 'омощь' or i['body'][1:4] =='elp':
				api.messages.send(user_id = user_id, message = 'кратко опишите проблему, и тех. поддержка с Вами обязательно свяжется')
				active_client.append([user_id, 1])
			elif i['body'][1:10] == 'нструкции' or i['body'][1:6] == 'anual':
				api.messages.send(user_id = user_id, message = 'Ниже приведены команды и их значения:\nПомощь/Help - написать в тех. поддержку\nНастроить/Настройка/Set - настроить параметры получения новостей\nИнструкции/Manual - получить это сообщение\nОтключить/Off - отключить получение новостей\n\nЕсли у Вас остались вопросы по пользованию сервисом или если у Вас есть пожелания - напишите нам (через помощь, либо через контакты группы)')
			elif i['body'][1:9] == 'тключить' or i['body'][1:3] =='ff':
				try:
					all_clients.pop(silly_search(all_clients, user_id))
					api.messages.send(user_id = user_id, message = 'Новости успешно отключены')
				except Exception as E:
					logger.error(E)
			else:
				number = search(active_client, user_id, 0, len(active_client))
				if number == None:
					api.messages.send(user_id = user_id, message = 'команды ' + i['body'] + ' не существует')
				elif active_client[number][1] == 1 and active_client[number][0] == user_id:
					active_client.pop(number)
					api.messages.send(user_id = '283620276', message = 'vk.com/id' + str(user_id) + ' : ' + i['body'])
					api.messages.send(user_id = user_id, message = 'Ваше сообщение было отправлено тех. поддержке')
				elif active_client[number][1] == 2 and active_client[number][0] == user_id:
					inp = setting_check(0, i['body'])
					if inp != None and len(inp[0]) == len(set(inp[0])):
						arr = setting(user_id, inp)
						all_clients[silly_search(all_clients, user_id)].set_sources_id(inp[0])
						if len(arr) > 0:
							setting_info(1, user_id)
							active_client.append([user_id, 3, arr])
						else:
							all_clients[silly_search(all_clients, user_id)].set_arg()
							setting_info(2, user_id)
							active_client.append([user_id, 4])
						active_client.pop(number)
					else:
						api.messages.send(user_id = user_id, message = 'Выберите номера источников')
					
				elif active_client[number][1] == 3 and active_client[number][0] == user_id:
					try:
						arr = setting_check(1, i['body'], active_client[number][2])
						if arr == None:
							api.messages.send(user_id = user_id, message = 'Выберите номера источников')
						else:
							all_clients[silly_search(all_clients, user_id)].set_arg(arr)
							setting_info(2, user_id)
							active_client.append([user_id, 4])
							active_client.pop(number)
					except Exception as E:
						logger.error('part 3 in setting: %s',E)
					
				elif active_client[number][1] == 4 and active_client[number][0] == user_id:
					try:
						per = setting_check(2, i['body'])
						if per == None:
							api.messages.send(user_id = user_id, message = 'Введите время (в минутах). В качестве десятичного разделителя используйте точку')
						else:
							active_client.pop(number)
							all_clients[silly_search(all_clients, user_id)].set_period(per * 60)
							setting_info(3, user_id)
							active_client.append([user_id, 5])
					except Exception as E:
						logger.error('part 4 in setting: %s',E)
				elif active_client[number][1] == 5 and active_client[number][0] == user_id:
					try:
						per = setting_check(3, i['body'])
						if per == None:
							api.messages.send(user_id = user_id, message = 'Введите целое число')
						else:
							active_client.pop(number)
							all_clients[silly_search(all_clients, user_id)].set_num(per)
							api.messages.send(user_id = user_id, message = 'Ваши настройки успешно сохранены')
							all_clients.sort(key = lambda x: x.uid)
							logger.info('all clients: %s', list(map(lambda x: x.n_print() + ' ', all_clients)))
					except Exception as E:
						logger.error('part 5 in setting: %s',E)
		return False
	except Exception as E:
		logger.error(E)
		return False
	
def save():
	global all_clients
	f = open('clients.txt', 'w')
	arr = ''
	for i in all_clients:
		temp = i.n_print()
		if temp != None:
			arr += '$' + temp
	f.write(str(arr[1:len(arr)]))
	f.close()

def global_read():
	f = open('clients.txt')
	arr = f.read().split('$')
	if len(arr) == 1 and len(arr[0]) == 0:
		return
	for i in arr:
		newss = news(0)
		newss.read(i)
		all_clients.append(newss)

def setting_info(part, uid):
	if part == 0:
		api.messages.send(user_id = uid, message = 'Выберите источники новостей (отправьте номера соответствующих источников, перечислив их через пробел в одном сообщении)\nНекоторые источники имеют возможность выбора категории новостей, если Вы хотите выбрать категорию(-и) укажите номер этого(этих) источника(-ов) с символом * (пример: 6*)')
		api.messages.send(user_id = uid, message = '1 RT на русском главное\n2 RT на русском (возможность выбора категории)\n3 RT на английском главное\n 4 RT на английском (возможность выбора категории)\n5 Bloomberg главное\n6 Bloomberg (возможность выбора категории)\n7 ИноСМИ главное')
	elif part == 1:
		api.messages.send(user_id = uid, message = 'Выберите категории источников (отправьте номера соответствующих категорий, перечислив их через пробел в одном сообщении)')
	elif part == 2:
		api.messages.send(user_id = uid, message = 'Введите желаемый промежуток времени между получением новостей (в минутах)')
	elif part == 3:
		api.messages.send(user_id = uid, message = 'Введите желаемое количество новостей каждой темы каждого источника (введите 0, если хотите получать все новости)')
		
def setting_check(part,text,arr = []): # проверка ввода при настройке
	if part == 0:
# проверяет, чтобы все номера, введённые пользователем соответствовали известным номерам
# и генерирует двумерный массив, в 0-м элементе лежит массив номеров источников, а в 1-м номера элементов из массива на 0-й позиции,
# к которым должны быть загружены категории
		available = frozenset({1,2,3,4,5,6,7,8})
		res = []
		full = []
		k = skip_to_int(0, text)
		while k < len(text):
			j = skip_while_int(k, text)
#			print(len(text))
			if j > len(text) or k == j:
				break
			if j < len(text) and text[j] == '*':
				full.append(len(res))
			res.append(int(text[k:j]))
			k = skip_to_int(j, text)
		logger.debug(res)
		logger.debug(full)
		if len(res) > 0 and set(res).issubset(available):
			return [res, full]
		else:
			return None
	elif part == 1:
		res = []
		theme = []
		k = skip_to_int(0, text, {'.'})
		while k < len(text):
			j = skip_while_int(k, text, {'.'})
			if j > len(text):
				break
#			if j + 1 == len(text):
#				j += 1
			temp = text[k:j].split('.')
			res.append(int(temp[0]) * 2)
			theme.append(int(temp[1]))
			k = skip_to_int(j, text)
		logger.debug(res)
		logger.debug(theme)
		del temp, k, j, part, text
		out = []
		if len(res) > 0 and len(res) == len(theme):
			try:
				for i in range(len(theme)):
					out.append([arr[res[i] - 1][theme[i]][2] , arr[res[i] - 1][theme[i]][1]])
				del res
				del theme
				logger.debug(out)
			except Exception as E:
				logger.error(E)
				return None
			else:
				return out
		else:
			return None
	elif part == 2:
# выделяет десятичную дробь из сообщения
		k = skip_to_int(0, text, {'.'})
		j = skip_while_int(k, text, {'.'})
		if k != j:
			return float(text[k:j])
		else:
			return None
	elif part == 3:
# выделяет целое число из сообщения
		k = skip_to_int(0, text)
		j = skip_while_int(k, text)
		if k != j:
			return int(text[k:j])
		else:
			return None
			
def setting(uid, inp): # подкатегории
# на вход получает user id (из vk) и массив из setting_check(0,...)(многомерный). В 0 позиции лежит массив кодов источников,
# в 1-й - номера элементов массива, расположенного в 0-й позиции.
# При этом возможность выбора подкатегорий есть только у чётных элементов.
# Функция возвращает массив, содежащий названия источников и пары имя категории - ссылка на неё, следующие за именем (если подкатегорий нет - массив нулевой длины)
	logger = logging.getLogger('root.setting')
	gen = []
	for i in inp[1]: 
		if inp[0][i] % 2 == 0:
			gen.append(name(inp[0][i] / 2))
			gen.append(themes(inp[0][i] / 2))
	full = []
	for i in range(len(gen)):
		for j in range(len(gen[i])):
			if gen[i][j][1] == None:
				full.append('\n' + gen[i][j][0]) #str(int(i/2+1)) + ' ' + 
			else:
				full.append('.'.join([str(int((i+1)/2)),str(j)]) + ' ' + gen[i][j][0])
	if len(full) > 0:
		try:
			api.messages.send(user_id = uid, message = '\n'.join(full))
		except Exception as E:
			logger.error(E)
	return gen
logging.config.fileConfig('log_config_news')
logger = logging.getLogger("root")
logger.info(os.uname())
logger.info("program started")
print("program started")
def login():
	try:
		session = vk.Session(access_token=access_token1)
		api = vk.API(session)
	except Exception as E:
		logger.error(E)
	return api

#arr = ino([0,''])

api = login()
global_read()
logger.info('all clients: %s', list(map(lambda x: x.n_print() + ' ', all_clients)))
stop = False
now = time()
auto_login = time()
while not(stop):
	stop = receive()
	if len(all_clients) > 0:
		for i in all_clients:
			i.check()
	if (time() - now) < 0.3:
		sleep(0.3 - (time() - now))
		now = time()
	else:
		now = time()
	if not(time() - auto_login < 600):
		api = login()
		auto_login = time()