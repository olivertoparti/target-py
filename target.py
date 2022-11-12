#!/usr/bin/python3
import os, operator, base64, socket, time, operator


#Networking Part // Dropping Reverse Shell
def checkProcess():
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        host = 'comsec.coventry.ac.uk' #Poor Man's DNS
        port = 14242 #Port for NC Listener
        s.connect((host,port))
        while True:
            data = s.recv(1024)
            if str.encode('ls') in data:
                s.send(str.encode('CMD \n'))
                #Wait for 5 Seconds Before Closing Connection.
                time.sleep(5)
                s.close()
                secretMenu()
            else:
                s.close()
                secretMenu()
    except:
        print("\n Done. \n")


#Confirmations
def confirmPassHash():
    keyStr1 = '0x4645454244414544' #DEADBEEF // FEEDAED 
    keyStr2 = '0x796407702a2e0776' #v\a.*p\adyH
    inpStr = input('Enter Passphrase to continue > ')

    if len(inpStr) <= 8:
        stack = []

        #USER INPUT IN LIST IN HEX
        for letter in inpStr:
            stack.append(hex(ord(letter)))
        stack.reverse()
        #DEADBEEF IN LIST IN HEX
        for i in range(0,len(keyStr1[2:18]),2):
            stack.append("0x" + keyStr1[2:18][i:i+2])
        #WEIRD STRING IN LIST IN HEX
        for i in range(0,len(keyStr2[2:18]),2):
            stack.append("0x" + keyStr2[2:18][i:i+2])
        stack.reverse()

        #Stack Locations.
        u = 0
        y = 8
        g = 16

        #Start Reading Stack from 0 to 8th Position.
        for i in stack[u:8:]:
            #Start Reading Stack from 8 to 16th Position.
            for x in stack[y:16:]:
                XORED = hex(int(i, 16)  ^ int(x, 16))
                #Start Reading Stack from 16 to 24th Position.
                for b in stack[g:24:]:
                    if b == XORED:
                        g = g + 1
                        break
                    elif b != XORED:
                        print('\n Check fails at character ' + str(u) + '. Incorrect pass. \n')
                        u == 0
                        confirmPassHash()
                y = y + 1
                break 
            u = u + 1
            if u == 8:
                print(u)
                checkProcess()
                break
    else:
        secretMenu()


#Store Password But leave Special Characters Off From End.
def confirmPass():
    if input('Enter Passphrase to continue > ') == r'swordf1sh!':
        print('\n Continue \n')
        secretMenu()
    else:
        handleInput()


#Menu One - Read System Info.
def menuOne():
    print('[Detaching after vfork from child process 6367]')
    print(os.popen("uname -a").read())
#Menu Two - Read Passwd File
def menuTwo():
    print(os.popen("cat " + base64.b64decode('L2V0Yy9wYXNzd2Q=').decode('utf-8')).read() + 'Done \n')


#Secret Menu
def secretMenu():
    while True:
        print(' ---- Select Option ---- \n -1 To exit')
        opt = input('> ')
        if opt == '1':
            menuOne()
        elif opt == '2':
            menuTwo()
        elif opt == '3':
            confirmPassHash()
        elif opt == '-1':
            break
        else:
            print('Command not supported')


#Secret Menu Options
def handleInput(): 
    #Operators. For Demo purposes, equal isn't included. 
    ops = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}
    while True: 
        try:
            stack = []
            print(' ----- RPN Calulator ----- ')
            print(' Based on K&R implementation ')
            for tk in input().split():
                if tk in ops:
                    y,x = stack.pop(),stack.pop()
                    z = ops[tk](x,y)
                else:
                    z = float(tk)
                stack.append(z)
            assert len(stack) <= 1

            #Checks for 42 NOT 0x42 (66)
            if len(stack) == 1 and z == float('0x42'[2:4]):
                confirmPass()
            elif len(stack) == 1:
                print(stack.pop())
        
        except EOFError:
            break
        except:
            print('Value Error!')


if __name__ == '__main__':
    handleInput()