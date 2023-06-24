# morse_code.py

# 설명: 이 코드는 영어를 모스 불호로 번역하거나 모스 부호를 영어로 번역하는 기능이 있다. 그리고 부저의 소리의 크기를 바꿀 수 있다.
# 모스 부호: 점과 대시로 형성한다
#           점: 1 단위, 대시: 3 단위, 점과 대시의 간격: 1 단위, 문자의 간격: 3 단위, 단어의 간격: 7 단위

# ASCII: '1'~'2': 48~57, A~Z: 65~90, a~z:  97~122, '-': 45, '.': 46

import RPi.GPIO as GPIO
import time

BUZZER_PIN = 4
LED_PIN = 5
MORSE_INPUT = 6
FREQ_UP = 7
FREQ_DOWN = 8
unit = 0.5      # 1 단위의 기간

dot = 3
dash = 2
# 첫번째 숫자는 점과 대시의 개수
morse = [[2, dot, dash],                        # A
         [4, dash, dot, dot, dot],              # B
         [4, dash, dot, dash, dot],             # C
         [3, dash, dot, dot],                   # D
         [1, dot],                              # E
         [4, dot, dot, dash, dot],              # F
         [3, dash, dash, dot],                  # G
         [4, dot, dot, dot, dot],               # H
         [2, dot, dot],                         # I
         [4, dot, dash, dash, dash],            # J
         [3, dash, dot, dash],                  # K
         [4, dot, dash, dot, dot],              # L
         [2, dash, dash],                       # M
         [2, dash, dot],                        # N
         [3, dash, dash, dash],                 # O
         [4, dot, dash, dash, dot],             # P
         [4, dash, dash, dot, dash],            # Q
         [3, dot, dash, dot],                   # R
         [3, dot, dot, dot],                    # S
         [1, dash],                             # T
         [3, dot, dot, dash],                   # U
         [4, dot, dot, dot, dash],              # V
         [3, dot, dash, dash],                  # W
         [4, dash, dot, dot, dash],             # X
         [4, dash, dot, dash, dash],            # Y
         [4, dash, dash, dot, dot],             # Z
         [5, dash, dash, dash, dash, dash],     # 0
         [5, dot, dash, dash, dash, dash],      # 1
         [5, dot, dot, dash, dash, dash],       # 2
         [5, dot, dot, dot, dash, dash],        # 3
         [5, dot, dot, dot, dot, dash],         # 4
         [5, dot, dot, dot, dot, dot],          # 5
         [5, dash, dot, dot, dot, dot],         # 6
         [5, dash, dash, dot, dot, dot],        # 7
         [5, dash, dash, dash, dot, dot],       # 8
         [5, dash, dash, dash, dash, dot]]      # 9

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(MORSE_INPUT, GPIO.IN)
GPIO.setup(FREQ_DOWN, GPIO.IN)
GPIO.setup(FREQ_UP, GPIO.IN)
GPIO.setup(dot, GPIO.OUT)
GPIO.setup(dash, GPIO.OUT)

notes = [131, 139, 147, 156, 165, 175, 185, 196, 208, 220, 233, 247, 262, 277, 294, 311, 330, 349, 370, 392, 415, 440, 466, 494, 523]
note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B',]
frequency = 12                                # 부저의 소리의 크기. 0일때 소리 없고, 50일때 소리가 가장 큼
buzzer = GPIO.PWM(BUZZER_PIN, notes[frequency])      # DutyCycle = 소리의 크기, 주파수 = 음표

GPIO.output(LED_PIN, GPIO.LOW)

#______________________________________________________________________________________________________________________________________

# 모스 부호의 리스트를 영문 문자로 바꾸는 기능
def morse_char(arr):
    if not arr:                 # arr는 비면 아무것도 안 한다
        pass
    else:
        for i in range(36):         # i로 arr와 morse를 비교한다
            is_letter = True
            ascii = arr[0]
            if ord(ascii)-48 != morse[i][0]:
                continue
            for j in range(1, morse[i][0]+1):
                ascii = arr[j]
                if ord(ascii)-43 != morse[i][j]:     # arr와 morse는 다르면 다음 i로 한다
                    is_letter = False
                    break
            if is_letter:                       # 문자는 맞으면 그 문자를 출력한다
                if i < 26:
                    print("%c" % chr(i+97), end = "", flush = True)
                else:
                    print("%c" % chr(i+22), end = "", flush = True)
                break

#______________________________________________________________________________________________________________________________________

# 영어 문장을 입력받고 모스 부호로 출력하는 기능
# 문자의 ascii 부호를 쓴다
def eng_morse():
    global frequency
    buzzer.start(0)
    buzzer.ChangeFrequency(notes[frequency])
    sentence = input('영문 문장을 입력해 주십시오.\n')              # 영어 문장을 입력받기
    letters = list(sentence)                                      # 문장을 리스트로 바꾸기
    for i in range(len(sentence)):
        ascii = letters[i]                                        # ord(letters[i])는 안 되기 때문에 이렇게 한다
        if ascii >= 'a' and ascii <= 'z':                 # 영문자는 소문자일 때
            index = ord(ascii) - 97
            for j in range(morse[ord(ascii) - 97][0]):
                code = morse[index][j+1]
                print("%c" % chr(code+43), end="", flush = True)    # end=""일 때 다음 print는 같은 줄에 출력되고, flush = True일 때 실시간으로 출력한다
                GPIO.output(code, GPIO.HIGH)            # 7 segment의 점이나 대시(G)를 켠다
                GPIO.output(LED_PIN, GPIO.HIGH)
                buzzer.ChangeDutyCycle(50)
                if code == dot:
                    time.sleep(unit)
                else:
                    time.sleep(3*unit)
                GPIO.output(code, GPIO.LOW)
                GPIO.output(LED_PIN, GPIO.LOW)
                buzzer.ChangeDutyCycle(0)
                time.sleep(unit)
        elif ascii >= 'A' and ascii <= 'Z':       # 영문자는 댓문자일 때
            index = ord(ascii) - 65
            for j in range(morse[ord(ascii) - 65][0]):
                code = morse[index][j+1]
                print("%c" % chr(code+43), end="", flush = True)
                GPIO.output(code, GPIO.HIGH)
                GPIO.output(LED_PIN, GPIO.HIGH)
                buzzer.ChangeDutyCycle(50)          # 부저를 켠다. 소리를 바꾸는 기능 있으니 변수로 한다
                if code == dot:
                    time.sleep(unit)
                else:
                    time.sleep(3*unit)
                GPIO.output(code, GPIO.LOW)
                GPIO.output(LED_PIN, GPIO.LOW)
                buzzer.ChangeDutyCycle(0)
                time.sleep(unit)
        elif ascii >= '0' and ascii <= '9':           # 문자는 숫자일 때
            index = ord(ascii) - 22
            for j in range(5):                                  # 숫자의 모스 부호는 다 5 개 있다
                code = morse[index][j+1]
                print("%c" % chr(code+43), end="", flush = True)
                GPIO.output(code, GPIO.HIGH)
                GPIO.output(LED_PIN, GPIO.HIGH)
                buzzer.ChangeDutyCycle(50)
                if code == dot:
                    time.sleep(unit)
                else:
                    time.sleep(3*unit)
                GPIO.output(code, GPIO.LOW)
                GPIO.output(LED_PIN, GPIO.LOW)
                buzzer.ChangeDutyCycle(0)
                time.sleep(unit)
        elif letters[i] == ' ':                 # 단어의 간격일 때
            print(" / ", end="", flush = True)
            time.sleep(7*unit)
        else:
            print("이 문자를 모스 부호로 번역할 수 없습니다. 글자를 화긴해 주십시오.")
            break
        print(" ", end="", flush = True)    # 한 문자를 출력하는 후 띄어쓰기 한다
        time.sleep(2*unit)                  # 이것은 3 단위이어야하는데 어차피 한 문자은 끝나기 후에 1 단위 기다리니까 2 단위 더한다
    buzzer.stop()
    print("\n번역하기 끝냈습니다.")

#______________________________________________________________________________________________________________________________________

# 모스 부호의 리스트를 영어 문장으로 바꾸는 기능
def morse_eng_keyboard(letters):
    arr = ['0', '0', '0', '0', '0', '0']                    # 모스 부호를 가지는 리스트
    count = 0                 # morse의 요소들의 첫번째 숫자는 다 모스 문자의 개수 있으니 비교하려고 arr에 개수를 추가해야 한다
    for i in range(len(letters)):
        if count > 5:
            print("Index out of range: %s" % letters)
        ascii = letters[i]
        if ascii == " ":        # 문자는 띄어쓰기이면 한 영문자는 끝난 뜻이다
            arr[0] = chr(count+48)
            morse_char(arr)
            count = 0
            for j in range(5):
                arr[j] = '0'
            continue
        elif ascii == "/":      # 문자는 "/"이면 한 영어 단어는 끝난 뜻이다
            print(" ", end = "", flush = True)
            continue
        count += 1
        arr[count] = ascii
    arr[0] = chr(count+48)
    morse_char(arr)
    print("\n번역하기 끝냈습니다.")

#______________________________________________________________________________________________________________________________________

# 모스 부호를 키보드나 버튼으로 입력받고 영어 문장으로 출력하는 기능
def morse_eng():
    val = input("1: 키보드로 하기, 2: 버튼으로 하기, 9: 취소 > ")           # 선택을 입력받기
    if val == '1':                                                       # 인터페이스로 모스 부호를 입력받기
        sentence = input("문장을 모스 부호로 입력해 주십시오.\n예) .... . .-.. .-.. --- / .-- --- .-. .-.. -.. => hello world (간격도 중요한다)\n")
        letters = list(sentence)
        morse_eng_keyboard(letters)
    elif val == '2':                        # 라즈베리파이에 있는 버튼으로 모스 부호를 입력받기
        global frequency
        buzzer.start(0)
        buzzer.ChangeFrequency(notes[frequency])
        arr = []
        first = True
        while True:
            pin = GPIO.input(MORSE_INPUT)
            count = 0
            while pin == 0:                 # 안 누르고 있을 때 아무것도 안 한다
                if first == False and count > 80:              # 8초보다 긴 기간 동안 안 누르면 while반복문을 그만한다
                    break
                pin = GPIO.input(MORSE_INPUT)
                count += 1
                time.sleep(0.1)
            if first:                       # 시작하는 후 첫째 안 누른 기간을 안 센다
                count = 0
                first = False
            else:                           # 시작이 아니면 버튼을 안 누른 기간을 센다
                # 15 미만이면 점, 대시의 간격이라서 아무것도 안 한다
                if count > 15 and count <= 35:  # 이때는 영문자의 간격이라서 띄어쓰기 출력한다
                    arr.append(" ")
                    print(" ", end = "", flush = True)
                    count = 0
                elif count > 35 and count <= 80:    # 이때 영어의 단어의 간격이라서 " / " 출력한다
                    arr.append(" ")
                    arr.append("/")
                    arr.append(" ")
                    print(" / ", end = "", flush = True)
                    count = 0
                elif count > 80:                    # 위에 있는 break문은 한 while 문을 멈췄으니 다시 해야 한다
                    break
            while pin == 1:                         # 버튼을 누른 기간을 센다
                if count > 35:                      # 3.5초보다 긴 기간 동안 누르면 입력받기를 그만한다
                    break
                elif count <= 10:
                    GPIO.output(dot, GPIO.HIGH)
                else:
                    GPIO.output(dot, GPIO.LOW)
                    GPIO.output(dash, GPIO.HIGH)
                buzzer.ChangeDutyCycle(50)
                GPIO.output(LED_PIN, GPIO.HIGH)
                pin = GPIO.input(MORSE_INPUT)
                count += 1
                time.sleep(0.1)
            buzzer.ChangeDutyCycle(0)
            GPIO.output(LED_PIN, GPIO.LOW)
            GPIO.output(dot, GPIO.LOW)
            GPIO.output(dash, GPIO.LOW)
            if count <= 10:             # 점의 기간
                arr.append(".")
                print(".", end = "", flush = True)
            elif count <= 35:           # 대시의 기간
                arr.append("-")
                print("-", end = "", flush = True)
            else:                       # 다시 break 해야 한다
                break
        print("\n")
        morse_eng_keyboard(arr)
        buzzer.stop()
    elif val == '9':
        pass
    else:
        print('없는 선택입니다.')
    print("\n")

#______________________________________________________________________________________________________________________________________

# 부저의 주파수의 높기를 바꾸는 기능
def frequency_change():
    global frequency
    down = 0            # 주파수를 낮추는 정도
    up = 0              # 주파수를 올리는 정도
    buzzer.start(50)
    while True:
        buzzer.ChangeFrequency(notes[frequency])
        down = GPIO.input(FREQ_DOWN)
        up = GPIO.input(FREQ_UP)
        note = note_names[frequency%8]
        print("Current frequency = %s" % note)
        if down == 1 and up == 1:               # 두 버튼을 함께 누르면 그만한다
            buzzer.stop()
            break
        if frequency == 24:          # 주파수는 24일 때 가장 높아서 멈춘다
            up = 0
        elif frequency == 0:           # 주파수는 0 보다 작을 수 없다
            down = 0
        if down == 1:             # FREQ_DOWN는 눌리고 있으면 주파수를 낮춘다
            frequency -= 1
        elif up == 1:               # FREQ_UP는 눌리고 있으면 주파수를 올린다
            frequency += 1
        time.sleep(0.5)             # 0.5초마다 입력받는다

#______________________________________________________________________________________________________________________________________

# main function
try:
    while True:
        val = input('1: 영어 -> 모스, 2: 모스 -> 영어, 3: 주파수 변하기, 9: 종료 > ')
        if val == '1':
            eng_morse()
        elif val == '2':
            morse_eng()
        elif val == '3':
            frequency_change()
        elif val == '9':
            break
        else:
            print('없는 선택입니다.')
finally:
    GPIO.cleanup()
    print('\ncleanup and exit')
