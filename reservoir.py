import random

class Reservoir:
	def __init__(self, k): #생성자 만드는거?
		self.sampled = [] #sampling 한 애들 담을 리스트
		self.k = k #초기화
		self.cnt = 0 #지금 들어오는 아이템이 몇번째인지? 개수?

	def put(self, item): #put 함수는 스트림에서 아이템하나가 들어오면 어떻게 처리할거냐
		if self.cnt < self.k: #작아야 넣고 더한다..? 왓..?
			#self.sampled[self.cnt] = item
			self.sampled.append(item)
		else:
			r = random.randint(0, self.cnt) #인클루시브 익스클루시브 차이래 randint랑 randrange랑
			#randint(0,10)은 0~10 리턴 , randrange(0,10)은 0~9 리턴
			if r<self.k: #랜덤으로 뽑은 r가 k보다 작으면
				self.sampled[r] = item #sampled[r] 에다가 item 넣기


		self.cnt +=1

reservoir = Reservoir(20)

for i in range(1000):
	reservoir.put(i)
	print(reservoir.sampled)

