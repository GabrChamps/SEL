import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
#%matplotlib inline

from datetime import datetime
import os.path

#--------------------------------------

def openSER(file_name):
#---OPEN


    rData = open('../'+file_name, "r").read()
    sData = rData.splitlines()
    sData = rData.splitlines()
    h=['#', 'Date', 'Time', 'Element', 'State', 'Date-Time']

    for i in range(len(sData)):
        if "#" in sData[i]:
            info =  sData[0:i]
            header = sData[i]
            data = sData[i+3:]
            break
    dataSize = len(data)

    #---Convert to df
    mx=[]
    for line in data:
        row=line.split(' ')
        nline=[]
        for x in row:
            if str(x) != '':
                nline.append(x)
        dateTime = datetime.strptime(nline[1]+' '+nline[2], "%m/%d/%y %H:%M:%S.%f")
        nline.append(dateTime)    


        mx.append(nline)
        del nline

    df = pd.DataFrame(data=mx, columns=h)
    del mx

    df.drop(columns=['Date','Time'],inplace=True)            
    elements = df['Element'].unique()
    nElements = len(elements)

    for i in range(dataSize):
        if df['State'][i]=='Asserted':
            df['State'][i]=1

        else:
            df['State'][i]=0

    #---States matrix

    samplesTime = df['Date-Time'].unique()
    nSamplesTime = len(samplesTime)

    nan=np.zeros((nSamplesTime,nElements))
    nan[:][:]=np.nan
    statesR = pd.DataFrame(nan, index=samplesTime, columns=elements)

    for i in range(dataSize):
        statesR[df['Element'][i]][df['Date-Time'][i]]=df['State'][i]
    statesF=statesR.copy()

    #---Fill nan data

    for el in elements:
        for i in range(nSamplesTime):
            if statesF[el][i] == 1 or statesF[el][i] == 0:
                if statesF[el][i] ==1:
                    statesF[el][0:i] =0
                else:
                    statesF[el][0:i] =1

                break
    statesF.fillna(method='ffill', inplace=True)

    #---Print

    for i in info:
        print(i)
    print('n Samples:', dataSize)
    print('\nTrigged times:', nSamplesTime)
    print('\t-First time:', samplesTime[0])
    print('\t-Last time:', samplesTime[-1])
    print('\nn elements:',nElements)
    for el in elements:
        count=0
        for t in samplesTime:
            if not np.isnan(statesR[el][t]):
                count=count+1
        print('\t-',el,':  \t',count)


    #---Grafico
    print('\n\n\t\t\t\t\t--- SER to Graphic ---')
    plt.figure(figsize=(15,nElements*0.6),frameon=False)
    plt.title('SER to Graphic')
    for i in range(nElements):
        plt.subplot(nElements,1,i+1)
        plt.step(statesF.index,statesF[elements[i]], where='post')
        plt.fill_between(statesF.index,statesF[elements[i]], step="post", alpha=0.2)
        plt.plot(statesR[elements[i]],'.k')
        #plt.tick_params(axis='x',labelcolor='k', bottom=False)
        plt.tick_params(axis='y',labelcolor='none', left=False)

        plt.xlim(samplesTime[0],samplesTime[-1])
        plt.ylim(-0.2,1.2)

        plt.grid()

        plt.ylabel(elements[i])
    plt.suptitle('SER to Graphic: '+file_name,fontsize=12)
    plt.show()

#print(' -----  SER 2 GRAPH  -----')
#print('Convert Sequencial Event Report to graphical visualization') 
    
while True:
    file = input('SER file (.txt): ')
    if file.find('.txt')==-1:
        file=file+'.txt'

# --- Validation
    #try:
    #        data = open('../'+file, "r")

    #        openSER(data.read())
    #except IOError:
    #        print("File does not exist")
    #finally:
    #        #data.close()


    if os.path.isfile('../'+file):
        openSER(file)
    else:
        print ("File '"+file+"' not exist")


    #print('----------------------------------------------------------------------------')
