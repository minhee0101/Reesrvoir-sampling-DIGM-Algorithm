#피디엪있다 봐라.
#상자가 있는데 상자에 들어가는 1의 개수가 정해져있어
#스트림에 새로운 값이 들어오면 0일때는 아무것도 안하고
#1일때는 상자를 하나만들어서 같은 상자가 3개가 되면 합치고 또
#커진게 3개가 되면 합치고 ....
#그니까 같은 박스는 최대 2개 까지란 말이지

#타임스템프가 계속 증가하는걸로 구현 ,,, 모듈러안함 ^!^

import random

class Bucket:  #박스 만드는 클래스
	def __init__(self,start,end):
		self.start = start
		self.end = end
	def __repr__(self):
		return f"({self.start},{self.end})"

class DGIM:
	def __init__(self):
		#상자들을 저장하는 공간?
		#영역={시작timestamp,끝timestamp,크기} 인데 크기는 따로 일단 한데
		#[[(30,30),(29,29)],[(25,26)],[(17,24),(12,16)]...] 요론식?이래
		self.bucket_tower = [[]]
		self.ts =0 #timestamp   몇번쨰로 들어오냐..?
	def put(self, bit):
		if bit == 1: #1이 들어오면
			b = Bucket(self.ts, self.ts) #노랑 박스를 만들어
			self.bucket_tower[0].insert(0,b) #0번자리에 b를 넣어

			layer = 0
			while len(self.bucket_tower[layer]) >2: #박스가 두개 넘으면 합치는 부분인가봐
				if len(self.bucket_tower) <= layer+1: #?? 여기 뭐냐 P01 45:00 쯤
					self.bucket_tower.append([]) #다음 단계 박스 만드는거?

				#layer가 3개가 됐으니 먼저 들어와있던 2개를 떼서 합쳐야해 (뒤에 2개)
				b1 = self.bucket_tower[layer].pop() #더 빨리 들어옴
				b2 = self.bucket_tower[layer].pop() #그 다음 들어옴

				#어케 합치냐면 
				#더 빨리 들어온거(b1)(오른쪽)의 end를 b2의 end로 바꿔주면 합쳐짐 ㅎㅅㅎ
				b1.end = b2.end

				#위에서 레이어(박스)만들어서 layer+1이 있어 거기다가 b1을 넣는거지
				self.bucket_tower[layer+1].insert(0,b1)
				#그러고 레이어 하나 추가
				layer +=1

		self.ts +=1

#0010100010[10101]0[101]000[1][1]0
#           s   e

	def count(self, k): #가장 최근 k개에 몇개의 1이 있었냐 세는거
		#ex) 1000101있으면 ts=7이고 최근 3개를 보고싶다 치면 4-6까지 보고싶은거니까 시작지점이 ts-k
		s = self.ts - k #근데 여기서 구현을 최근꺼는 왼쪽에 있는데 걍 0부터 k 아닌가?..

		cnt = 0

		#하나하나 조회해서 검사하는거지
		for layer, buckets in enumerate(self.bucket_tower):
			for bucket in buckets:
				if s <= bucket.start: #검사지점?이 중간이면 비례해서 더해야하니까 중간지점인지 보는겨
					cnt += (1<<layer) #2**layer #중간지점이 아닌경우임
				elif s <= bucket.end: #중간지점인경우
					cnt += (1<<layer) * (bucket.end -s +1)//(bucket.end - bucket.start+1)#비례하는거 계산
					return cnt
				else:
					return cnt
		return cnt



dgim = DGIM()

bitstream = []
for i in range(10):
	prob = random.random() #prob를 랜덤으로 넣어 #얘가 만약 0.9면은
	for j in range(random.randint(20,50)):
		if random.random() < prob:
			bitstream.append(1) #90퍼 확률로 1 이 들어가고
		else:
			bitstream.append(0) #10퍼 확률로 0 이 들어가용



#for b in [0,1,0,1,1,0,1,1,1,1,1,0,0,0,1]:
#	dgim.put(b)
#	print(dgim.bucket_tower)


#실제 1개수랑 dgim했을때 예측한 값 찾으려구...
for b in bitstream: 
	dgim.put(b)

for k in range(1,200):
	print(k, dgim.count(k),sum(bitstream[-k:])) #dgim.count(k)는 실제 1의 개수 sum(bitstream[-k:])는 예측한 1의 개수


#DGIM 을 사용하기 좋은 경우는 들어오는 1의 분포가 시간마다 달라질때도 정확하게 예측하는 경우