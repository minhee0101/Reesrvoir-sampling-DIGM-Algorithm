import random
import matplotlib.pyplot as plt

class Bucket:  #박스 만드는 클래스
	def __init__(self,start,end):
		self.start = start
		self.end = end
	def __repr__(self):
		return f"({self.start},{self.end})"

class Bucket2:  #박스 만드는 클래스
	def __init__(self,start,end,psum):
		self.start = start
		self.end = end
		self.psum = psum
	def __repr__(self):
		return f"({self.start},{self.end},{self.psum})"

class DGIM:
	def __init__(self):
		#상자들을 저장하는 공간?
		#영역={시작timestamp,끝timestamp,크기} 인데 크기는 따로 일단 한데
		#[[(30,30),(29,29)],[(25,26)],[(17,24),(12,16)]...] 요론식?이래
		self.bucket_tower = [[]]
		self.ts =0 #timestamp 몇번쨰로 들어오냐..?
	def put(self, bit):
		if bit == 1: #1이 들어오면
			b = Bucket(self.ts, self.ts) #노랑 박스를 만들어
			self.bucket_tower[0].insert(0,b) #0번자리에 b를 넣어

			layer = 0
			while len(self.bucket_tower[layer]) >2: #박스가 두개 넘으면 합치는 부분인가봐
				if len(self.bucket_tower) <= layer+1: #?? 여기 뭐냐 P01 45:00 쯤
					self.bucket_tower.append([]) #다음 단계 박스 만드는거?

				#layer가 3개가 됐으니 먼저 들어와있던 2개를 떼서 합쳐야 해 (뒤에 2개)
				b1 = self.bucket_tower[layer].pop() #더 빨리 들어옴
				b2 = self.bucket_tower[layer].pop() #그 다음 들어옴

				#어케 합치냐면
				#더 빨리 들어온거(b1)(오른쪽)의 end를 b2의 end로 바꿔주면 합쳐짐 ㅎㅅㅎ
				b1.end = b2.end

				#위에서 레이어(박스)만들어서 layer+1이 있어 거기다가 b1을 넣는거지
				self.bucket_tower[layer+1].insert(0,b1)
				#그러고 다음 레이어 확인하려고 하는거다~ 요말이지?
				layer +=1

		self.ts +=1

# 0010100010[10101]0[101]000[1][1]0
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

class DGIM2:
	def __init__(self):
		# 상자들을 저장하는 공간?
		# 영역={시작timestamp,끝timestamp,크기} 인데 크기는 따로 일단 한데
		# [[(30,30),(29,29)],[(25,26)],[(17,24),(12,16)]...] 요론식?이래
		self.bucket_tower = [[]]
		self.ts = 0  # timestamp 몇번쨰로 들어오냐..?


	def put(self, bit):
		#if bit == 1:  # 1이 들어오면
		b_ = Bucket2(self.ts, self.ts,bit)  # 노랑 박스를 만들어
		self.bucket_tower[0].insert(0, b_)  # 0번자리에 b를 넣어

		layer = 0

		while len(self.bucket_tower[layer]) > 2:  # 박스가 두개 넘으면 합치는 부분인가봐
			if len(self.bucket_tower) <= layer + 1:  # ?? 여기 뭐냐 P01 45:00 쯤
				self.bucket_tower.append([])  # 다음 단계 박스 만드는거?


			# layer가 3개가 됐으니 먼저 들어와있던 2개를 떼서 합쳐야 해 (뒤에 2개)
			b1 = self.bucket_tower[layer].pop()  # 더 빨리 들어옴
			b2 = self.bucket_tower[layer].pop()  # 그 다음 들어옴

			if(b1.psum + b2.psum) <= 2**layer: #b1이랑 b2의 누적합이 2의 레이어제곱보다 작거나 같으면
				b1.end = b2.end  #원래대로 합쳐주고
				b1.psum += b2.psum #누적값 바꿔주고
				self.bucket_tower[layer + 1].insert(0, b1) #layer+1에 b1넣고

				layer += 1

			else: #b1이랑 b2의 누적합이 2의 레이어제곱보다 크다면
				self.bucket_tower[layer + 1].insert(0, b1) #b1만 layer+1에 넣고
				self.bucket_tower[layer].insert(1,b2) #위에서 pop했던 b2 다시 넣어주깅!~!@

				layer += 1

		self.ts += 1

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
					cnt += bucket.psum
				elif s <= bucket.end: #중간지점인경우
					cnt += bucket.psum * (bucket.end -s +1)//(bucket.end - bucket.start+1) #비례하는거 계산
					return cnt
				else:
					return cnt
		return cnt



dgim = DGIM()

bitstream = []

#첫번째 방법
a=[]
b=[]
c=[]
d=[]

dgima = DGIM()
dgimb = DGIM()
dgimc = DGIM()
dgimd = DGIM()

#요기 밑에는 스트림 랜덤으로 받는부분
for i in range(10000): #10000개의 정수
	prob = random.randrange(16) #0~15까지 랜덤으로 난수(정수) 생성
	bitstream.append(prob)
	a.append(((1 << 3) & prob) >> 3) #1000
	b.append(((1 << 2) & prob) >> 2) #0100
	c.append(((1 << 1) & prob) >> 1) #0010
	d.append((1 & prob))			 #0001

#각각 비트 쪼갠거를 dgim에 넣은거지
for i in a:
	dgima.put(i)
for i in b:
	dgimb.put(i)
for i in c:
	dgimc.put(i)
for i in d:
	dgimd.put(i)


#두번째 방법
dgim2 = DGIM2()
for i in bitstream:
	dgim2.put(i)



realsum = [] #실제합
sum1 = [] #첫번째합
sum2 = [] #두번째합
sum1_ = []
sum2_ = []

for i in range(2000):
	realsum_ = 0
	for j in range(i):
		realsum_ += bitstream[j]
	realsum.append(realsum_)

	sum1.append(dgima.count(i)*8 + dgimb.count(i)*4 + dgimc.count(i)*2 + dgimd.count(i))

	sum2.append(dgim2.count(i))

	sum1_.append(realsum_-(dgima.count(i)*8 + dgimb.count(i)*4 + dgimc.count(i)*2 + dgimd.count(i)))
	sum2_.append(realsum_-(dgim2.count(i)))

	#print(realsum[i],sum1[i],sum2[i]) #값 출력
#plt.subplot(2,2,1)
#plt.plot(realsum,'k')
#plt.subplot(2,2,2)
#plt.plot(sum1,'b')
#plt.subplot(2,2,3)
#plt.plot(sum2,'r')
#plt.subplot(2,2,4)
#plt.plot(realsum,'k')
#plt.plot(sum1,'b')
#plt.plot(sum2,'r')
y=[0,0]
x=[0,0]
plt.ylim(-400,400)
plt.plot(x,y,'k')
plt.plot(sum1_,'b')
plt.plot(sum2_,'r')
plt.show()


#	for j in range(random.randint(0,15)):
#		if random.random() < prob:
#			bitstream.append(1) #90퍼 확률로 1 이 들어가고
#		else:
#			bitstream.append(0) #10퍼 확률로 0 이 들어가용



#for b in [0,1,0,1,1,0,1,1,1,1,1,0,0,0,1]:
#	dgim.put(b)
#	print(dgim.bucket_tower)


#실제 1개수랑 dgim했을때 예측한 값 찾으려구...

#for k in range(1,200):
#	print(k, dgim.count(k),sum(bitstream[-k:])) #dgim.count(k)는 실제 1의 개수 sum(bitstream[-k:])는 예측한 1의 개수


#DGIM 을 사용하기 좋은 경우는 들어오는 1의 분포가 시간마다 달라질때도 정확하게 예측하는 경우