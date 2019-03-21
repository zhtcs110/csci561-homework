#!/usr/bin/env python
import copy
def alphabeta(a,b,player,size,list,level,depth):
	if depth==0 or searchPos(list,size)==[]:
		return checkAdvantage(list,size)	
	if player:
		for child in searchPos(list,size):
			newlist=copy.deepcopy(list)
			alist=placeEmitter(child[0],child[1],newlist,player,size)
			childScore=alphabeta(a,b,not player,size,alist,level+1,depth-1)
			if a<childScore:
				a=childScore
				answer=(child[0],child[1])
			if a>=b:
				answer=(child[0],child[1])				
				break
		if level==1:
			print answer
			print a
	 		output(answer)
		return a
	else:
		for child in searchPos(list,size):
			newlist=copy.deepcopy(list)
			blist=placeEmitter(child[0],child[1],newlist,player,size)
			b=min(b,alphabeta(a,b,not player,size,blist,level+1,depth-1))
			if a>=b:
				break
		return b



def searchPos(list,size):
	res=[]
	for i in xrange(size):
		for j in xrange(size):
			if list[i][j]==0:
				res.append((i,j))
	return res

def checkAdvantage(list,size):
	res=0
	for i in xrange(size):
		for j in xrange(size):
			if list[i][j]==1 or list[i][j]==5 or list[i][j]==4:
				res+=1
			if list[i][j]==2 or list[i][j]==6 or list[i][j]==4:
				res-=1
	return res

def placeEmitter(x,y,list,player,n):
	pos=1
	if not player:
		pos=2
	list[x][y]=pos
	i=1
	while (x+i)<n:
		if list[x+i][y]==3:
			break
		if list[x+i][y]==0 or list[x+i][y]==(pos+4):
			list[x+i][y]=(pos+4)
		else:
			list[x+i][y]=4
		i+=1
	i=1
	while (x-i)>=0:
		if list[x-i][y]==3:
			break
		if list[x-i][y]==0 or list[x-i][y]==(pos+4):
			list[x-i][y]=(pos+4)
		else:
			list[x-i][y]=4
		i+=1
	i=1
	while (y+i)<n:
		if list[x][y+i]==3:
			break
		if list[x][y+i]==0 or list[x][y+i]==(pos+4):
			list[x][y+i]=(pos+4)
		else:
			list[x][y+i]=4
		i+=1	
	i=1
	while (y-i)>=0:
		if list[x][y-i]==3:
			break
		if list[x][y-i]==0 or list[x][y-i]==(pos+4):
			list[x][y-i]=(pos+4)
		else:
			list[x][y-i]=4
		i+=1
	i=1
	while (x+i)<n and (y+i)<n:
		if list[x+i][y+i]==3:
			break
		if list[x+i][y+i]==0 or list[x+i][y+i]==(pos+4):
			list[x+i][y+i]=(pos+4)
		else:
			list[x+i][y+i]=4
		i+=1
	i=1
	while (x+i)<n and (y-i)>=0:
		if list[x+i][y-i]==3:
			break
		if list[x+i][y-i]==0 or list[x+i][y-i]==(pos+4):
			list[x+i][y-i]=(pos+4)
		else:
			list[x+i][y-i]=4
		i+=1
	i=1
	while (x-i)>=0 and (y+i)<n:
		if list[x-i][y+i]==3:
			break
		if list[x-i][y+i]==0 or list[x-i][y+i]==(pos+4):
			list[x-i][y+i]=(pos+4)
		else:
			list[x-i][y+i]=4
		i+=1
	i=1
	while (x-i)>=0 and (y-i)>=0:
		if list[x-i][y-i]==3:
			break
		if list[x-i][y-i]==0 or list[x-i][y-i]==(pos+4):
			list[x-i][y-i]=(pos+4)
		else:
			list[x-i][y-i]=4
		i+=1
	return list

def output(answer):
	fout=open("output.txt","w")
	fout.write(str(answer[0])+" "+str(answer[1]))
	fout.close()

def main():
	f=open("input3.txt","r")
	size=int(f.readline())
	depth=6
	list=[[0 for i in xrange(size)] for i in xrange(size)]
	row=0
	for line in f.readlines():
		for j in xrange(size):
			list[row][j]=int(line[j])
		row+=1
	newlist=[[0 for i in xrange(size)] for i in xrange(size)]
	newlist=list
	for i in xrange(size):
		for j in xrange(size):
			if list[i][j]==1:
				newlist=placeEmitter(i,j,newlist,True,size)
			elif list[i][j]==2:
				newlist=placeEmitter(i,j,newlist,False,size)	#initialize completed	

	alphabeta(-10000000,10000000,True,size,newlist,1,depth)     # alpha minimum, beta maximum
	f.close()

if __name__ == "__main__":
    main()

