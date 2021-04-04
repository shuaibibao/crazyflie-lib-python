import matplotlib.pyplot as plt 
import pandas as pd 
import math

vtracking=[-0.5,0]  #0.5m/s
vsource=[0.1,-0.1]   #0.1m/s
size=5
deltaT=0.1 #100ms sample once as a base unit
sigma=0.03

#read data
disData_path="./distForEstVeloBy100ms.csv"    #using a new dataSet fastSampleDist.csv
data=pd.read_csv(filepath_or_buffer=disData_path)
distances=(data['distance'].values).tolist()

def calcuDis(point1,point2):
    return math.sqrt(math.pow(point1[0]-point2[0],2)+math.pow(point1[1]-point2[1],2))


#remove duplicate information
pre=0
cur=distances[0]
n=len(distances)
for i in range(0,n):   #update length
    if(i==len(distances)):
        break
    while(abs(distances[i]-pre)<0.001):
        distances.remove(distances[i])
        if(i==len(distances)):
            break
    if(i==len(distances)):
        break
    pre=distances[i]
    
# for dis in distances:
#     cur=dis
#     if(abs(cur-pre)<0.001): 
#         distances.remove(cur)
#     else:
#         pre=cur
print(distances)

def preciseVelocityEstimatorByDiffT(start,_k,k,step):  #step=1,2,3....
    A=0.0
    for i in range(0,2*_k+1):
        A+=math.pow(distances[start+i*step],2)
    res=(3*A-(6*_k+3)*distances[k]**2)/(_k*(_k+1)*(2*_k+1)*(deltaT*step)**2)
    if(res<0):
        return -1
    return math.sqrt(res)
if __name__=="__main__":
    n = len(distances)
    if(n%2==0):
        distances.pop(n-1)  #remove last one
        n=n-1
    mid = n//2
    res=[]
    for step in range(1,11):
        curVelo=preciseVelocityEstimatorByDiffT(mid-3*step,3,mid,step)
        res.append([step*deltaT,curVelo])

    trueVValue=calcuDis(vtracking,vsource)
    log_var={'deltaT':0,'velo':0,'trueVelo':0}
    log_data=pd.DataFrame(columns=log_var.keys())
    temp={'deltaT':0,'velo':0,'trueVelo':0}
    for item in res:
        temp['deltaT']=item[0]
        temp['velo']=item[1]
        temp['trueVelo']=trueVValue
        log_data=log_data.append(temp,ignore_index=True)
    csv_path="./csv/tEffectOnEst.csv"
    log_data.to_csv(csv_path,index=False)
    print(res)

    


