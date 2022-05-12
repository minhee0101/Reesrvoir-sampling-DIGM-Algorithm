import random
import matplotlib.pyplot as plt

arr = [0 for i in range(1000)]

class Reservoir:
    def __init__(self, k):  # 생성자 만드는거?
        self.sampled = []  # sampling 한 애들 담을 리스트
        self.k = k  # 초기화
        self.cnt = 0  # 지금 들어오는 아이템이 몇번째인지? 개수?

    def put(self, item):  # put 함수는 스트림에서 아이템하나가 들어오면 어떻게 처리할거냐
        if self.cnt < self.k:  # 작아야 넣고 더한다..? 왓..?
            # self.sampled[self.cnt] = item
            self.sampled.append(item)
            arr[item] += 1
        else:
            r = random.randint(0, self.cnt)  # 인클루시브 익스클루시브 차이래 randint랑 randrange랑
            # randint(0,10)은 0~10 리턴 , randrange(0,10)은 0~9 리턴
            if r < self.k:  # 랜덤으로 뽑은 r가 k보다 작으면
                arr[self.sampled[r]] -= 1
                self.sampled[r] = item  # sampled[r] 에다가 item 넣기
                arr[item] += 1

        self.cnt += 1




for i in range(10000):
    reservoir = Reservoir(100)  # <--요기 괄호안에 있는게 그 추출할 크기??인가봄 ~@~!2
    for j in range(1000):
        reservoir.put(j)
        #print(reservoir.sampled)
        ##0~999까지 100개를 10000번

plt.plot(arr)
plt.ylim([0, 2000])
plt.show()