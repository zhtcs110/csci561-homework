#!/usr/bin/env python
class Plane:
	def __init__(self,remainmin,landmin,gatemin,takeoffmin,complainmin,idd,landtime,takeofftime):
		self.landmin=landmin
		self.gatemin=gatemin
		self.takeoffmin=takeoffmin
		self.landtime=landtime
		self.takeofftime=takeofftime
		self.remainmin=remainmin
		self.complainmin=complainmin
		self.idd=idd
class Constraints:
	def __init__(self,landnum,gatenum,takeoffnum,planelist):
		self.landnum = landnum
		self.gatenum=gatenum
		self.takeoffnum=takeoffnum
		self.planelist=planelist

	def satisfiedland(self,schedulednum,landtime):
		landflight=1
		gateflight=1
		for i in xrange(schedulednum):
			if planelist[i].landtime+planelist[i].landmin>landtime and planelist[i].landtime<landtime+planelist[schedulednum].landmin:
				landflight+=1
			if planelist[i].takeofftime>landtime+planelist[schedulednum].landmin and landtime+planelist[schedulednum].landmin+planelist[schedulednum].gatemin>planelist[i].landtime+planelist[i].landmin:
				gateflight+=1
		if landflight>landnum:
			return False
		if gateflight>gatenum:
			return False
		return True

	def satisfiedtakeoff(self,schedulednum,takeofftime):
		takeoffflight=1
		for i in xrange(schedulednum):
			if planelist[i].takeofftime+planelist[i].takeoffmin>takeofftime and planelist[i].takeofftime<takeofftime+planelist[schedulednum].takeoffmin:
				takeoffflight+=1
		if takeoffflight>takeoffnum:
			return False
		return True

class Csp:
	def __init__(self, landnum,gatenum,takeoffnum,constraints,planenum,planelist,step,maxnum):
		self.landnum = landnum
		self.gatenum=gatenum
		self.takeoffnum=takeoffnum
		self.constraints=constraints
		self.planenum=planenum
		self.planelist=planelist
		self.step=step
		self.maxnum=maxnum

	def backtrack(self,schedulednum,islandtime):
		if islandtime:
			if schedulednum==planenum:
				self.output()
				return 1
			else:
				num=0
				plane=planelist[schedulednum]
				while num<=maxnum:
					if num>plane.remainmin:
							break
					if constraints.satisfiedland(schedulednum,num):
						plane.landtime=num
						if self.backtrack(schedulednum,not islandtime):
							return 1
					num=num+step
				return 0
		else:
			plane=planelist[schedulednum]
			num=plane.landtime+plane.landmin+plane.gatemin
			while num<=maxnum:
				if (num-plane.landtime-plane.landmin)>plane.complainmin:
					break
				if constraints.satisfiedtakeoff(schedulednum,num):
					plane.takeofftime=num
					if self.backtrack(schedulednum+1,not islandtime):
						return 1
				num=num+step
			return 0

	def output(self):
		fout=open("output.txt","w")
		dict={}
		for lll in planelist:
			dict[lll.idd]=lll
		for x in dict.keys():
			fout.write(str(dict[x].landtime)+" "+str(dict[x].takeofftime)+"\n")
		fout.close()

if __name__ == "__main__":
	f=open("input.txt","r")
	firstline=f.readline().split(" ")
	landnum=int(firstline[0])
	gatenum=int(firstline[1])
	takeoffnum=int(firstline[2])
	planenum=int(f.readline())
	splist=[]
	idd=1
	for line in f.readlines():
		intlist=map(int,line.split(" "))
		intlist.append(idd)
		splist.append(intlist)
		idd+=1
	maxnum=0
	for ll in splist:
		maxnum=max(ll)+maxnum
	step=1
	planelist=[]
	plist=sorted(splist,cmp=lambda x,y:cmp(x[0]+x[1],y[0]+y[1]))
	for x in xrange(planenum):
		locals()['plane'+str(x)]=Plane(plist[x][0],plist[x][1],plist[x][2],plist[x][3],plist[x][4],plist[x][5],0,0)
		planelist.append(locals()['plane'+str(x)])
	constraints=Constraints(landnum,gatenum,takeoffnum,planelist)
	csp=Csp(landnum,gatenum,takeoffnum,constraints,planenum,planelist,step,maxnum)
	csp.backtrack(0,True)
	f.close()
