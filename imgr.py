import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import time
from collections import Counter

def createExamples():
    numberArrayExamples=open('numArEx.txt','a')
    numbersWeHave=range(0,10)
    versionsWeHave=range(1,10)

    for eachNum in numbersWeHave:
        for eachVer in versionsWeHave:
             #print  str(eachNum)+'.'+str(versionsWeHave)
             imageFilePath='images/numbers/'+str(eachNum)+'.'+str(eachVer)+'.png'
             ei=Image.open(imageFilePath)
             eiar=np.array(ei)
             eiar1=str(eiar.tolist())
             
             lineToWrite=str(eachNum)+'::'+eiar1+'\n'
             numberArrayExamples.write(lineToWrite)


#this fn converts colored pixel into white or black ie threshold that pixel
def threshold(imageArray):
    balanceAr = []
    newAr = imageArray

    for eachRow in imageArray:
        for eachPix in eachRow:
            avgNum=reduce(lambda x,y:x+y,eachPix[:3])/len(eachPix[:3])
            balanceAr.append(avgNum)
    balance=reduce(lambda x,y:x+y,balanceAr)/len(balanceAr)

    for eachRow in newAr:
        for eachPix in eachRow:
            if reduce(lambda x,y:x+y,eachPix[:3])/len(eachPix[:3]) > balance:
                eachPix[0]=255
                eachPix[1]=255
                eachPix[2]=255
                eachPix[3]=255

            else:
                eachPix[0]=0
                eachPix[1]=0
                eachPix[2]=0
                eachPix[3]=255
    return newAr


#this fn compare our image with the array of sample images which we have to compare in database
def whatNumIsThis(filepath):
	matchedArr=[]
	loadDatabase=open('numArEx.txt','r').read()
	loadDatabase=loadDatabase.split('\n')

	i=Image.open(filepath)
	iar=np.array(i)
	iarl=iar.tolist()

	inQuestion=str(iarl)
	for eachExample in loadDatabase:
		if len(eachExample)> 3:
			splitEx=eachExample.split('::')
			currentNum=splitEx[0]
			currentArr=splitEx[1]

			eachPixEx=currentArr.split('],')
			eachPixInQ=inQuestion.split('],')
			x=0
			while x<len(eachPixEx):
				if eachPixEx[x]==eachPixInQ[x]:
					matchedArr.append(int(currentNum))

				x+=1;

	#print matchedArr
	x=Counter(matchedArr)
	print x
        
	graphX=[]
	graphY=[]

	ylimi=0

	for eachThing in x:
		print eachThing
		graphX.append(eachThing)
		print x[eachThing]
		graphY.append(x[eachThing])
		ylimi=x[eachThing]

	fig=plt.figure()
	ax1=plt.subplot2grid((4,4),(0,0),rowspan=1,colspan=4)
	ax2=plt.subplot2grid((4,4),(1,0),rowspan=3,colspan=4)
	ax1.imshow(iar)
	ax2.bar(graphX,graphY,align='center')
	plt.ylim(400)
	xloc=plt.MaxNLocator(12)
	ax2.xaxis.set_major_locator(xloc)
	plt.show()

whatNumIsThis('images/numbers/6.1.png')
					
