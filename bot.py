import telebot
import sqlite3
import datetime
from telebot.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import config    


bot = telebot.TeleBot('1640616666:AAH4BSB_8a-75IU0E0mRZHJdk5UgqKpEoLM')


# Клавиатура в боте
hi_kb = InlineKeyboardMarkup(row_width = 1)
moder = InlineKeyboardButton("Отправить на модерацию", callback_data = 'moder')
hi_kb.add(moder)

setDate = InlineKeyboardMarkup(row_width = 1)
datetarif = InlineKeyboardButton("Задать дату", callback_data = 'setData')
setDate.add(datetarif)

set_info = InlineKeyboardMarkup(row_width = 1)
inf = InlineKeyboardButton("Отправить информацию", callback_data = 'set_info')
set_info.add(inf)

begin = ReplyKeyboardMarkup(resize_keyboard = True)
info = KeyboardButton("Начать")
begin.add(info)

compleet = ReplyKeyboardMarkup(resize_keyboard = True)
complet = KeyboardButton("Готово")
compleet.add(complet)

yn = InlineKeyboardMarkup(row_width = 2)
y = InlineKeyboardButton("Да", callback_data = 'y')
n = InlineKeyboardButton("Нет", callback_data = 'n')
yn.add(y, n)

src = InlineKeyboardMarkup(row_width = 2)
set = InlineKeyboardButton('Отправить ссылку', callback_data = 'src')
src.add(set)

adminKB = InlineKeyboardMarkup(row_width = 2)
partner = InlineKeyboardButton('Пaртнёр', callback_data = 'par')
pro = InlineKeyboardButton('Продвинутый', callback_data = 'pro')
vip = InlineKeyboardButton('VIP', callback_data = 'vip')
no = InlineKeyboardButton('Отклонить', callback_data = 'no')
adminKB.add(partner, pro, vip, no)

tarif_kb = InlineKeyboardMarkup(row_width = 2)
ar = InlineKeyboardButton('Серебро', callback_data = 'ar')
au = InlineKeyboardButton('Золото', callback_data = 'au')
pt = InlineKeyboardButton('Платина', callback_data = 'pt')
br = InlineKeyboardButton('Брилиант', callback_data = 'br')
tarif_kb.add(ar, au, pt, br)


@bot.message_handler(commands = ['start', 'help'])
def welcome(message):	
	AddUser(message.from_user.id, '', '', '', '')
	bot.send_message(message.chat.id, f'Пpиветствуем, {message.from_user.first_name}! \n Добро пожаловать в клуб Strike Team🤗\n Введите Ваш логин и затем нажмите на кнопку:', reply_markup = hi_kb)

	
# Обработчик клавиатуры
@bot.callback_query_handler(func=lambda c:True)
def keyboard(c):
	db = sqlite3.connect('users.db')
	sql = db.cursor()
	if c.data == 'par' or c.data == 'pro' or c.data == 'ar' or c.data == 'au' or c.data == 'pt' or c.data == 'br':
		config.tarif = {
				c.data == 'par': 'ПАРТНЕР',
				c.data == 'pro': 'ПРОДВИНУТЫЙ',
				c.data == 'ar': 'СЕРЕБРО',
				c.data == 'au': 'ЗОЛОТО',
				c.data == 'pt': 'ПЛАТИНА',
				c.data == 'br': 'БРИЛИАНТ'
		}[True]		
		
	if c.data == 'moder' and c.message.chat.id != config.admin:
		text = config.message + '\n' + 'id: ' + str(config.ID)
		setLogin(config.ID,  config.message)
		try:			
			bot.send_message(c.message.chat.id, "Благодорим. Мы формируем для Вас специальное предложение. Мы вернемся в течении 12 часов.")
			bot.send_message(config.admin, text, reply_markup = adminKB)
		except:
			bot.send_message(c.message.chat.id, 'Вы забыли написать ваш логин. Отправте логин и нажмите на кнопку.', reply_markup = hi_kb)	
		
	if c.data == 'ar' or c.data == 'au' or c.data == 'pt' or c.data == 'br':
			bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text='Готово')
			bot.send_message(config.admin, 'Напишите дату окончанния подписки в формате: ' + str(datetime.date.today()) + ' и затем нажмите на кнопку', reply_markup = setDate)
			bot.send_message(config.id, f'Благодарим за ожидание. \n Ваш тариф {config.tarif} \n Для автоматического постинга и предоставления трафикаответьте  на несколько вопросов \n Начнем?', reply_markup=begin)
			bot.send_message(config.admin, 'Напишите дату окончанния подписки в формате: ' + str(datetime.date.today()) + ' и затем нажмите на кнопку', reply_markup = setDate)
			setTarif(config.id, 'VIP')
			
	if c.data == 'par':
		config.id = c.message.text[c.message.text.find(':') + 2 :]
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text='Готово')
		bot.send_message(config.id, 'Благодарим за ожидание. \n Ваш тариф ПАРТНЕР \n Для автоматического постинга и предоставления трафикаответьте  на несколько вопросов \n Начнем?', reply_markup=begin)
		bot.send_message(config.admin, 'Напишите дату окончанния подписки в формате: ' + str(datetime.date.today()) + ' и затем нажмите на кнопку', reply_markup = setDate)
		setTarif(config.id, 'ПАРТНЕР')
		
	if c.data == 'pro':
		config.id = c.message.text[c.message.text.find(':') + 2 :]
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text='Готово')
		bot.send_message(config.id, 'Благодарим за ожидание. \n Ваш тариф ПРОДВИНУТЫЙ \n Для автоматического постинга и предоставления трафикаответьте  на несколько вопросов \n Начнем?', reply_markup=begin)
		bot.send_message(config.admin, 'Напишите дату окончанния подписки в формате: ' + str(datetime.date.today()) + ' и затем нажмите на кнопку', reply_markup = setDate)
		setTarif(config.id, 'ПРОДВИНУТЫЙ')
		
	if c.data == 'vip':
		config.id = c.message.text[c.message.text.find(':') + 2 :]
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text='Какой именно тариф?', reply_markup = tarif_kb)
		
	if c.data == 'setData':		
		try:
			date = config.message.replace('-', '')
			setData(config.id, date)
			datatime = datetime.datetime.strptime(date, '%Y%m%d').date()
		except:
			bot.send_message(config.admin, 'Неверный формат! Напишите дату окончанния подписки в формате: ' + str(datetime.date.today()) + ' и затем нажмите на кнопку', reply_markup = setDate)
			
	if c.data == 'set_info':
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text= 'Отправте не менее 10 фото с открытым лицом для оформления стиля.')
		setInfo(config.ID, config.message)
		
	if c.data == 'no':
		bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id, text="Не допущено")
		bot.send_message(c.message.chat.id, "Ой... \n Возможно вы забыли оплатить тариф на сайте")
		
	if c.data  == 'y':
		bot.send_message(c.message.chat.id, 'Введите ссылку (канал должен быть публичным)', reply_markup = src)
		
	if c.data  == 'n':
		bot.send_message(c.message.chat.id, 'Как создать канал в телеграм? \n Если у вас ещё нет аккаунта в телеграмм, тогда его нужно создать. Для того, чтобы это сделать необходимо скачать себе приложение на телефон через AppStore (если у вас продукция Apple) или через Google Play (если Android). Или же можно установить приложение с сайта https://telegram.org и зарегистрироваться в нем.  \n ⬇️ \n Когда у вас есть аккаунт, зайдите в раздел чатов Chats и нажмите на карандашик в правом верхнем углу (для создания нового чата).  \n ⬇️ \n Затем нажмите кнопку “New Channel 1�7 для создания нового канала. \n ⬇️ \n Нажмите кнопку «Create Channel 1�7 (создать канал). \n ⬇️ \n Заполните название канала, установите фото канала и добавьте описание канала. \n ⬇️ \nВыберите Public (Публичный) и дополните ссылку названием канала. \n Вот и все, Ваш канал создан. \n Введите ссылку (канал должен быть публичным)', reply_markup = src)
	
	if c.data == 'src':
		chane = config.message.replace('//', '')
		if chane[ : -len(chane) + 1] == '@':
			chanel = chane.replace('@', '')			
		else:
			chanel = chane[chane.find('/') + 1:]	
		setChanel(config.ID, chanel)
		bot.send_message(c.message.chat.id, 'Отлично! \n Теперь добавте бота в администраторы вашего канала, чтобы работал автопостинг.', reply_markup = compleet)
		sql.execute(f'SELECT tarif FROM users WHERE id = "{c.message.chat.id}" ')
		tarif = sql.fetchone()
		sub = str(tarif)
		sub = sub.replace('(', '')
		sub = sub.replace('\'', '')
		sub = sub.replace(',', '')
		sub = sub.replace(')', '')


@bot.message_handler(content_types=['text', 'photo'])
def message(message):
	db = sqlite3.connect('users.db')
	sql = db.cursor()
	
	try:
		sql.execute(f'SELECT tarif FROM users WHERE id = "{message.chat.id}" ')
		tarif = sql.fetchone()
		sql.execute(f'SELECT date FROM users WHERE id = "{message.chat.id}" ')
		d = str(sql.fetchone())
		d = d.replace('(', '')
		d = d.replace('\'', '')
		d = d.replace(',', '')
		d = d.replace(')', '')
		dat = datetime.datetime.strptime(d, '%Y%m%d').date()
		sub = str(tarif)
		sub = sub.replace('(', '')
		sub = sub.replace('\'', '')
		sub = sub.replace(',', '')
		sub = sub.replace(')', '')
		if sub != 'no' and dat >= datetime.date.today():
			subscribe = True
		else:
			subscribe = False
	except:
		subscribe = False
		
	config.message = message.text
	config.ID = message.from_user.id
	
	if subscribe == True and message.chat.id != config.post:
		if message.text == 'Начать' and message.chat.id != config.admin:
			bot.send_message(message.chat.id, 'У Вас есть канал в Телеграм?', reply_markup = yn)
			
		if message.text == 'Готово' and message.chat.id != config.admin:
			bot.send_message(message.chat.id, 'Отлично! Теперь Вы автоматически будете получать публикации постов на тему инвестиций и дополнительного заработка в вашем канале.')
			bot.send_message(message.chat.id, 'Eсли Вы хотите дизайн, индивидуальный контентный план, администратора для ведения соц сетей или заказать любую другую услугу пишите в этот чат. Мы поможем Вам зарабатывать больше!')
			if sub == 'VIP':
					bot.send_message(message.chat.id, 'Пришлите информацию о вас: \n Ваше ФИО \n Дату рождения \n Номер телефона \n после этого нажмите на кнопку: \n Внимание присылать одним сообщением!', reply_markup = set_info)
			
		if tarif == 'pro' and message.chat.id != config.admin:
				bot.send_message(message.chat.id, 'Рекомендации к названию канала. \n Можно: \n только фамилию и любое уточнение, \n имя, фамилию без уточнения \n имя, фамилию с уточнениями деятельности \n название деятельности \n Не нужно непонятных, отвлеченных названий. \n \n Примеры: \n Иван Иванов \n Инвестиции с Иваном Ивановым \n ИВАН Иванов Финансы и Крипта \n ИВАН ИВАНОВ | ИНВЕСТОР \n \n Описание канала должно быть конкретным, отражающим пользу для читателя. \n \n Пример: \n 📈 Научу инвестировать \n 💼Мой портфель с реальными цифрами \n 💰Как заработать дома \n ⚠️БЕСПЛАТНАЯ КОНСУЛЬТАЦИЯ \n @ \n 📱МОЙ КАНАЛ \n @')
				bot.send_message(message.chat.id, 'Обязательно сделайте пост-закреп, где укажите все свои реферальные ссылки с описанием рода деятельности. /n По сути Вы рассказываете в закрепе о себе. /n Кто Вы? /n Чем занимаетесь? /n На чем зарабатываете? \n Чем можете быть полезны? /n Сколько у Вас денег? \n Пруфы? \n Опыт \n \n Пример: \n 👋🏽Привет, меня зовут Иван, /n Мне  1�7 лет, более  1�7 лет занимаюсь предпринимательской деятельностью. /n 💵Скажу сразу, развивать в себе предпринимательский потенциал - это лучшее, что может быть, поэтому мы с тобой сейчас знакомимся и начинаем общаться. \n \n На данный момент я имею несколько источников дохода. \n ▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️\n 1) STRIKE TEAM - комaнда инвесторов Strike Team создала комьюнити нового поколения для всех, кому интересны инвестиции. Мы на своем опыте знаем, как сложно начать и еще сложнее не закончить плохо. \n \n Теперь инвестировать можно под контролем наставников. Получать самые актуальные и проверенные схемы. Находить новые возможности для бизнеса за счет грамотного нетворкинга с членами команды и спонсорами. \n \n В команде Strike Team реально начать зарабатывать более 10 000$ в месяц. \n Вы быстро умножите свои деньги и выйдете на новый уровень бизнеса. \n Переходите по ссылке: \n \n ▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️\n 2) QUBITTECH  1�7 квантовое будущее стало настоящим 😱 \n \n QubitTech  1�7 единая экосистема на основе квантовых технологий и распределение ресурсов платформы между пользователями. \n Цель и миссия компании  1�7 дать участникам платформы возможность получить награды и бонусы на основе надежного квантового вычисления. \n \n Доверять свой капитал надёжным платформам  1�7 важный фактор при инвестициях. \n \n Хотите больше информации или прибыль 250%? \n Заходите по ссылке👇🏼\n  ▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️▫️\n Как результат свой деятельности в интернете, я имею сейчас несколько квартир в центре города с отличным ремонтом, дом 450 кв также в центре города, два премиум авто, 3 магазина с собственными коммерческими помещениями и не отказываю себе в регулярных путешествиях заграницу. \n 〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️ \n 🎯Цель моего блога - собирать вокруг себя комьюнити деятельных людей, помогать раскрывать предпринимательский потенциал читателям и себе, обмениваться опытом, повышать свою личную ответственность перед читателями, самому регулярно расти и как, минимум, делать всё возможное для этого. \n 〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️ \n 🤗Если тебе интересен мой ПУТЬ и ты хочешь научиться зарабатывать в интернете, выгодно инвестировать без риска, то добро пожаловать. Дай огня и в следующих публикациях ты узнаешь о каждом моем источнике дохода более подробно! \n \n Для личной консультации пиши поямо в личку')			
		#	bot.send_message(message.chat.id, 'Eсли Вы хотите дизайн, индивидуальный контентный план, администратора для ведения соц сетей или заказать любую другую услугу пишите в это чат. Мы поможем Вам зарабатывать больше!')
		
	if subscribe == False and message.chat.id != config.admin and message.chat.id != config.post:
			bot.send_message(message.chat.id, 'Срок действия вашей подписки истек или вы её не купили. Если подписка куплена приишлите нам свой логин и нажмите на кнопку: ', reply_markup = hi_kb)
			setChanel(message.chat.id, 'KirilIProger')
			setTarif(message.chat.id, 'no')
				

	sql.execute(f'SELECT tarif FROM users WHERE id = "{message.chat.id}" ')
	tarif = sql.fetchone()
	sub = str(tarif)
	sub = sub.replace('(', '')
	sub = sub.replace('\'', '')
	sub = sub.replace(',', '')
	sub = sub.replace(')', '')
# Отправка информации от VIP клиентов
	if sub == 'VIP':
		try:
			idphoto = message.photo[0].file_id
			sql.execute(f" SELECT info FROM users WHERE id = '{message.chat.id}' ")
			info = sql.fetchone()
			bot.send_photo(config.info, idphoto, info)
		except:
			pass
		
		
	# Автопостинг
	try:
		sql.execute(f" SELECT chanel FROM users ")
		chanels = sql.fetchall()
		if message.chat.id == config.post:
			try:
				photo = message.photo[0].file_id
			except:
				pass
			caption = message.caption
			text = message.text
			ch = list(chanels)
			for e in ch:
					el = str(e)
					el = el.replace('(', '')
					el = el.replace(')', '')
					el = el.replace('\'', '')
					el = el.replace(',', '')
					try:
						bot.send_photo(el, photo, caption)
					except Exception as e:
						bot.send_message(el, text)
	except:
		pass
		
# Функции для работы с базой данных			
def AddUser(id, login, tarif, data, chanel):
	db = sqlite3.connect('users.db')
	sql = db.cursor()
	sql.execute("""CREATE TABLE IF NOT EXISTS users (
			id INT,
			login TEXT,
			tarif TEXT,
			date TEXT,
			chanel TEXT,
			info TEXT
	)""")
	db.commit()
	sql.execute(f"SELECT id FROM users WHERE id = '{id}' ")
	if sql.fetchone() is None:
		sql.execute("SELECT id FROM users")
		sql.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)", (id, login, 'no', data, chanel, ''))
		db.commit()

def setTarif(id, tarif):
	db = sqlite3.connect('users.db')
	sql = db.cursor()
	sql.execute("""CREATE TABLE IF NOT EXISTS users (
			id INT,
			login TEXT,
			tarif TEXT,
			date TEXT,
			chanel TEXT,
			info TEXT
	)""")
	db.commit()
	sql.execute(f'SELECT id FROM users WHERE id = "{id}" ')
	if sql.fetchone() is None:
		pass #('NONE	USER')
	else:
		sql.execute(f' UPDATE users SET tarif = "{tarif}" WHERE id = "{id}" ')
		db.commit()
		
		
def setLogin(id, login):
	db = sqlite3.connect('users.db')
	sql = db.cursor()
	sql.execute("""CREATE TABLE IF NOT EXISTS users (
			id INT,
			login TEXT,
			tarif TEXT,
			date TEXT,
			chanel TEXT,
			info TEXT
	)""")
	db.commit()
	sql.execute(f'SELECT id FROM users WHERE id = "{id}" ')
	if sql.fetchone() is None:
		pass #('NONE	USER')
	else:
		sql.execute(f' UPDATE users SET login = "{login}" WHERE id = "{id}" ')
		db.commit()
		
def setData(id, date):
	db = sqlite3.connect('users.db')
	sql = db.cursor()
	sql.execute("""CREATE TABLE IF NOT EXISTS users (
			id INT,
			login TEXT,
			tarif TEXT,
			date TEXT,
			chanel TEXT,
			info TEXT
	)""")
	db.commit()
	sql.execute(f'SELECT id FROM users WHERE id = "{id}" ')
	if sql.fetchone() is None:
		pass #('NONE	USER')
	else:
		sql.execute(f' UPDATE users SET date = "{date}" WHERE id = "{id}" ')
		db.commit()
		
def setChanel(id, chanel):
	db = sqlite3.connect('users.db')
	sql = db.cursor()
	sql.execute("""CREATE TABLE IF NOT EXISTS users (
			id INT,
			login TEXT,
			tarif TEXT,
			date TEXT,
			chanel TEXT,
			info TEXT
	)""")
	db.commit()
	sql.execute(f'SELECT id FROM users WHERE id = "{id}" ')
	if sql.fetchone() is None:
		pass #('NONE	USER')
	else:
		chan = '@' + chanel
		sql.execute(f' UPDATE users SET chanel = "{chan}" WHERE id = "{id}" ')
		db.commit()
		
def setInfo(id, info):
	db = sqlite3.connect('users.db')
	sql = db.cursor()
	sql.execute("""CREATE TABLE IF NOT EXISTS users (
			id INT,
			login TEXT,
			tarif TEXT,
			date TEXT,
			chanel TEXT,
			info TEXT
	)""")
	db.commit()
	sql.execute(f'SELECT id FROM users WHERE id = "{id}" ')
	if sql.fetchone() is None:
		pass #('NONE	USER')
	else:
		sql.execute(f' UPDATE users SET info = "{info}" WHERE id = "{id}" ')
		db.commit()
	

bot.polling()