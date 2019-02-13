import time
import socket
from myconfig import *
from getchar import _Getch
from pykeyboard import PyKeyboard

keyboard = PyKeyboard()

START_TIME = time.time()

# Init TCP connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (SERVER_IP, SERVER_PORT)


def connect():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)

while True:
    try:
        connect()
        break
    except:
        print('False to conect to server')
        time.sleep(1)


def reset_round():
    global START_TIME
    START_TIME = time.time()
    print 'RESET round done.'


def receive_message(threadName):
    global START_TIME
    data = ''
    while True:
        try:
            tmp = sock.recv(32)
            tmp = tmp.decode("utf-8")
            data += tmp
            
            print data
            if '\n' in tmp:
                # xu ly du lieu tu server (start)
                print(type(data))
                if 'START_ROUND' in data:
                    keyboard.press_key('r')
                    if '1' in data:
                        keyboard.press_key('1')
                    else:
                        keyboard.press_key('2')
                elif 'STOP_ROUND' in data:
                    keyboard.press_key('r')
                elif 'RESET_ROUND' in data:
                    keyboard.press_key('r')
                    if '1' in data:
                        keyboard.press_key('1')
                    else:
                        keyboard.press_key('2')
                data = ''
        except Exception as e:
            print(e)
            time.sleep(1)
            connect()
    # time.sleep(3)
    # keyboard.press_key('r')

# Create new threads
thread_receive_message = myThread(2, "thread_receive_message", receive_message)
thread_receive_message.start()


def send_message(data):
    count = 0
    while True:
        try:
            count += 1
            sock.sendall(data.encode())
            break
        except:
            time.sleep(1)
            connect()
            if count > 2:
                print("Send message: %s [FALSE]" % data)
                break


ROUND = ['1', '2']
SENSOR_INDEX = ['1', '2', '3', '4', '5']

def main():
    global START_TIME
    ROUND_NUM = None
    getch = _Getch()
    while(True):
        print 'Cac phim tat co ban:'
        print 'B1: nhap so thu tu cua round (1 hoac 2)'
        print 'B2: nhap moc diem bang cac phim 1,2,3,4,5'
        print 'Phim R de gui tin hieu RESTART round'
        print 'Phim Q de thoat khoi chuong trinh'
        print '------------------------------------------------------------------------------'
        print ''
        while(True):
            print 'Nhap vong dau: ',
            char = getch.__call__()
            if char in ROUND:
                print '\nBAT DAU vong dau thu: %s' % char
                reset_round()
                print 'Nhap so thu tu cua cac moc da di qua (tu 1 - 5)'
                ROUND_NUM = char                
                while (True):
                    char = getch.__call__()
                    # print char
                    if char in SENSOR_INDEX:
                        timestamp = time.time()
                        runtime = timestamp - START_TIME
                        message = "%s:P%s:%s" % (STADIUM + ROUND_NUM, char, runtime)
                        print 'Moc %s duoc gui di: %s' % (char, message)
                        send_message(message)
                        if char == '5':
                            break
                    if char == 'r' or char == 'R':
                        reset_round()
                        break
                    if char == 'q':
                        return
            if char == 'q':
                return
main()
