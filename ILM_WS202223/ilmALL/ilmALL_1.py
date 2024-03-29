import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import table
from pandas.plotting import table
import sys
sys.path.append('C:/Users/Benedikt/Documents/dev/MA_LogParser/logparser/ILM_WS202223')
import generalfunctions as gf

if __name__ == '__main__':

    # Setup
    allValues = []
    descArray = []
    db = gf.get_database()
    tresor = db["tresor"]

    # Teleport
    T_1 = tresor.find_one({'name': 'T-1'})
    T_1 = gf.convertToFloat1D(T_1)
    T_2 = tresor.find_one({'name': 'T-2'})
    T_2 = gf.convertToFloat1D(T_2)
    allValues.append(T_1)
    allValues.append(T_2)
    descArray.append('T-1')
    descArray.append('T-2')

    # Sn
    Sn_1 = tresor.find_one({'name': 'Sn-1'})
    Sn_1 = gf.convertToFloat1D(Sn_1)
    Sn_2 = tresor.find_one({'name': 'Sn-2'})
    Sn_2 = gf.convertToFloat1D(Sn_2)
    allValues.append(Sn_1)
    allValues.append(Sn_2)
    descArray.append('Sn-1')
    descArray.append('Sn-2')

    # Sf
    Sf_1 = tresor.find_one({'name': 'Sf-1'})
    Sf_1 = gf.convertToFloat1D(Sf_1)
    Sf_2 = tresor.find_one({'name': 'Sf-2'})
    Sf_2 = gf.convertToFloat1D(Sf_2)
    allValues.append(Sf_1)
    allValues.append(Sf_2)
    descArray.append('Sf-1')
    descArray.append('Sf-2')

    # Ga
    Ga_AR_1 = tresor.find_one({'name': 'Ga-AR-1'})
    Ga_AR_1 = gf.convertToFloat1D(Ga_AR_1)
    Ga_AR_2 = tresor.find_one({'name': 'Ga-AR-2'})
    Ga_AR_2 = gf.convertToFloat1D(Ga_AR_2)
    Ga_VR = tresor.find_one({'name': 'Ga-VR'})
    Ga_VR = gf.convertToFloat1D(Ga_VR)
    allValues.append(Ga_AR_1)
    allValues.append(Ga_AR_2)
    allValues.append(Ga_VR)
    descArray.append('Ga-AR-1')
    descArray.append('Ga-AR-2')
    descArray.append('Ga-VR')



    # Plot

    num, val, df = gf.setXTicks_param(allValues, descArray)
    plt.title('Werte aller ILM-Operatoren', fontsize=15)
    plt.grid(axis='y', linestyle='-', which='major', color='lightgray', alpha=0.5)
    sns.boxplot(allValues, showmeans=True, orient='v', color='skyblue')
    # sns.violinplot(allValues, showmeans=True, color="skyblue", inner="stick")
    # sns.swarmplot(allValues, color="black")
    ttable = table(plt.gca(), df, loc='bottom', colLoc='center', cellLoc='center')
    for key, cell in ttable.get_celld().items():
        cell.set_edgecolor('white')
        cell.set_height(0.05)
    plt.ylabel('Sekunden', fontsize=12)
    ttable.set_fontsize(12)
    ttable.auto_set_font_size(False)
    plt.xticks([])

    plt.show()