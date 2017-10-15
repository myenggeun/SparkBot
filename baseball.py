import random

    # 게임을 위한 랜덤 숫자 생성
    
rn = ["0", "0", "0"]
rn[0] = str(random.randrange(1, 9, 1))
rn[1] = rn[0]
rn[2] = rn[0]

while (rn[0] == rn[1]):
    rn[1] = str(random.randrange(1, 9, 1))

while (rn[0] == rn[2] or rn[1] == rn[2]):
    rn[2] = str(random.randrange(1, 9, 1))

#print(rn)

t_cnt = 0 # 시도횟수
s_cnt = 0 # 스트라이크 갯수
b_cnt = 0 # 볼 갯수

print("Let's start baseball game !!!")
print("---------------------------")

while ( s_cnt < 3 ):
    num = str(input("Put any 3 numbers : "))

    s_cnt = 0
    b_cnt = 0

    for i in range(0, 3):
        for j in range(0, 3):
            if(num[i] == str(rn[j]) and i == j):
                s_cnt += 1
            elif(num[i] == str(rn[j]) and i != j):
                b_cnt += 1
                
    print("Result : [" ,s_cnt, "] Strike [" ,b_cnt, "] Ball")
    t_cnt += 1

print("---------------------------")
print("Great, you did it in" , t_cnt , "times")
