from flask import Flask, request, render_template
import sqlite3
import serial, time

app = Flask(__name__)

@app.route('/call-center/find')
# взятие имени из формы html
def get_name(methods = ['POST', 'GET']):
    if request.method == 'POST':
        user_name = str(request.form.get('name'))
        return user_name
    else:
        return render_template('form.html')
        
# взятие смс из формы html (ПРОБЛЕМЫ С КОДИРОВКОЙ ПРИ ОТПРАВЛЕНИИ СООБЩЕНИЯ!!!)
def get_mess():
    if request.method == 'POST':
        message = request.form.get('message')
        return message
    else:
        defolt_mess = 'Zdravstvuite.'
        return defolt_mess


#нахождение номера из базы данных
def find_number():
    
    conn = sqlite3.connect('bd.sqlite')
    name = "'" + get_name() + "'"
    cursor = conn.cursor()
    #запрос:
    cursor.execute("SELECT Number FROM users WHERE Name = {}".format(name))
    #сохранение результата запроса в переменную number
    number = str(cursor.fetchall())
    #корректировка номера из [+7**********,] в +7**********
    number = ''.join(number.split('[', 1))
    number = ''.join(number.split(']'))
    number = ''.join(number.split(','))
    number = ''.join(number.split(')'))
    number = ''.join(number.split('('))
    conn.close()
    return number

#взятие пароля из ГЕНЕРАТОРАПАРОЛЯ(пока что из текстового документа)
def get_pass():
    file = open('pass.txt')
    pass_for_user = file.read()
    file.close()
    return pass_for_user
 
#отправка сообщения пользователю


def send_mess():
    name = get_name()
    number = find_number()
    #text_message = get_mess()
    password = get_pass()
    # НЕ МОГУ ПОДОБРАТЬ КОДИРОВКУ К ОТПРАВЛЯЕМОМУ ТЕКСТУ
    text_message =  "PASSWORD: " + password #+text_message  
    #поиграйся с COM портом
    ser=serial.Serial("COM5",9600)
    start_cmd='AT+CMGF=1\r'
    start_byte=start_cmd.encode('KOI8-R')

    num_cmd='AT+CMGS="'+number+'"\r\n'
    num_byte=num_cmd.encode('KOI8-R')

    msg_cmd = text_message+"\x1A"
    
    msg_byte=msg_cmd.encode('KOI8-R')
    


    ser.write(start_byte)
    time.sleep(1)
    #ser.write('AT+CMGS="'+sender+'"\r\n')
    ser.write(num_byte)

    time.sleep(1)

    #ser.write(message+"x1A")
    ser.write(msg_byte)
    time.sleep(1)
    return render_template('form.html')
    

if __name__ == '__main__':
    app.run(debug = True)