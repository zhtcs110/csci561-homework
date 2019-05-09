class Mdp:
	def __init__(self,grid,pro,disc,rp,size,terminals,epsi):
		self.gird=grid
		self.pro=pro
		self.disc=disc
		self.rp=rp
		self.epsi=epsi
		self.terminals=terminals
		self.size=size
		reward={}
		states=set()
		for i in xrange(1,size):
			for j in xrange(1,size):
				if grid[i][j]!=None:
					states.add((i,j))
					reward[(i,j)]=grid[i][j]
		self.states=states
		self.reward=reward
		self.actlist=[(0,1),(1,0),(0,-1),(-1,0)]
		self.trans = {}
		for s in states:
			self.trans[s]={}
			for a in self.actlist:
				self.trans[s][a]=self.transmodel(s,a)

	def getreward(self,state):
		return self.reward[state]

	def transmodel(self,state,action):
		if action:
			i=0
			if action[0]==0:
				i=0
			else:
				i=1
			return [(pro,self.gointo(state,action)),
					((1-pro)/2,self.gointo(state,(1 if i==0 else action[0],1 if i==1 else action[1]))),
					((1-pro)/2,self.gointo(state,(-1 if i==0 else action[0],-1 if i==1 else action[1])))]
		else:
			return [(0.0,state)]

	def gettrans(self,state,action):
		return self.trans[state][action] if action else [(0.0, state)]

	def gointo(self,state,direct):
		if direct==(1,0):
			x=state[0]+1
			y=state[1]
		elif direct==(1,1):
			x=state[0]+1
			y=state[1]+1
		elif direct==(1,-1):
			x=state[0]+1
			y=state[1]-1
		elif direct==(-1,1):
			x=state[0]-1
			y=state[1]+1
		elif direct==(-1,-1):
			x=state[0]-1
			y=state[1]-1
		elif direct==(-1,0):
			x=state[0]-1
			y=state[1]
		elif direct==(0,1):
			y=state[1]+1
			x=state[0]
		elif direct==(0,-1):
			y=state[1]-1
			x=state[0]
		statenew=(x,y)
		return statenew if statenew in self.states else state

	def actions(self,state):
		if state in self.terminals:
			return [None]
		else:
			return self.actlist

	def valueiter(self):
		u1={s: 0 for s in self.states}
		while True:
			delta=0
			u=u1.copy()
			for s in self.states:
				u1[s]=self.getreward(s)+disc*max(sum(p*u[s1] for (p,s1) in self.gettrans(s,a)) for a in self.actions(s))
				delta=max(delta,abs(u1[s]-u[s]))
			if delta<=epsi*(1-disc)/disc:
				return u

	def argmax(self,llist,sorts):
		maxact=llist[0]
		maxnum=sorts(maxact)
		for l in llist:
			lnum = sorts(l)
			if lnum > maxnum:
				maxact, maxnum = l, lnum
		return maxact


	def getoptpolicy(self,U):
		policy = {}
		for s in self.states:
			policy[s] = self.argmax(self.actions(s), lambda a: self.getutility(a, s, U))
		symbol={(1, 0): 'D', (0, 1): 'R', (-1, 0): 'U', (0, -1): 'L', None: 'E'}
		optpol={s: symbol[a] for (s, a) in policy.items()}
		return optpol

	def getutility(self,a, s, U):
		return sum(p*U[s1] for (p, s1) in self.gettrans(s, a))

	def output(self,answer):
		fout=open("output.txt","w")
		for i in xrange(1,self.size):
			str=""
			for j in xrange(1,self.size):
				str=str+answer.get((i, j),'N')+","
			fout.write(str[:-1]+"\n")
		fout.close()

if __name__ == "__main__":
	f=open("input.txt","r")
	size=int(f.readline())
	pos=[[0 for i in xrange(size+1)] for i in xrange(size+1)]
	wallnum=int(f.readline())
	for i in xrange(wallnum):
		ll=map(int,f.readline().split(","))
		pos[ll[0]][ll[1]]=None
	terminnum=int(f.readline())
	terminlist=[]
	for i in xrange(terminnum):
		ll=map(int,f.readline().split(","))
		pos[ll[0]][ll[1]]=ll[2]
		terminlist.append((ll[0],ll[1]))
	pro=float(f.readline())
	rp=float(f.readline())
	for i in xrange(size+1):
		for j in xrange(size+1):
			if pos[i][j]==0 and (i,j) not in terminlist:
				pos[i][j]=rp
	disc=float(f.readline())
	epsi=1
	Mdp =Mdp(pos,pro,disc,rp,size+1,terminlist,epsi)
	Mdp.output(Mdp.getoptpolicy(Mdp.valueiter()))
	f.close()