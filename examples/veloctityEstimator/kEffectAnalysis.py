import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__=="__main__":
    csv_path="./csv/kEffectOnEst.csv"
    plt.figure()
    data=pd.read_csv(filepath_or_buffer=csv_path)
    plt.axhline(y=data['trueVelo'][0],linestyle='-',color="green",label="trueVelo")
    sns.lineplot(x="k",y="velo",data=data,label="estVelo")
    
    plt.show()