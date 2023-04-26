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



    # P
    P_AR = tresor.find_one({'name': 'P-AR'})
    P_AR = gf.convertToFloat1D(P_AR)
    P_VR = tresor.find_one({'name': 'P-VR'})
    P_VR = gf.convertToFloat1D(P_VR)
    allValues.append(P_AR)
    descArray.append('P-AR')
    allValues.append(P_VR)
    descArray.append('P-VR')

    # Gr
    Gr_AR = tresor.find_one({'name': 'Gr-AR'})
    Gr_AR = gf.convertToFloat1D(Gr_AR)
    Gr_VR_1 = tresor.find_one({'name': 'Gr-VR-1'})
    Gr_VR_1 = gf.convertToFloat1D(Gr_VR_1)
    Gr_VR_2 = tresor.find_one({'name': 'Gr-VR-2'})
    Gr_VR_2 = gf.convertToFloat1D(Gr_VR_2)
    allValues.append(Gr_AR)
    descArray.append('Gr-AR')
    allValues.append(Gr_VR_1)
    descArray.append('Gr-VR-1')
    allValues.append(Gr_VR_2)
    descArray.append('Gr-VR-2')

    # M
    M_AR = tresor.find_one({'name': 'M-AR'})
    M_AR = gf.convertToFloat1D(M_AR)
    M_VR = tresor.find_one({'name': 'M-VR'})
    M_VR = gf.convertToFloat1D(M_VR)
    allValues.append(M_AR)
    descArray.append('M-AR')
    allValues.append(M_VR)
    descArray.append('M-VR')


    # Plot

    num, val, df = gf.setXTicks_param(allValues, descArray)
    plt.title('Werte aller ILM-Operatoren', fontsize=15)
    plt.grid(axis='y', linestyle='-', which='major', color='lightgrey', alpha=0.5)
    sns.boxplot(allValues, showmeans=True, orient='v', color='skyblue')
    # sns.violinplot(allValues, showmeans=True, color="skyblue", inner="stick")
    # sns.swarmplot(allValues, color="black")
    ttable = table(plt.gca(), df, loc='bottom', colLoc='center', cellLoc='center')
    for key, cell in ttable.get_celld().items():
        cell.set_edgecolor('lightgrey')
        cell.set_height(0.05)
    plt.ylabel('Sekunden', fontsize=12)
    ttable.set_fontsize(12)
    ttable.auto_set_font_size(False)
    plt.xticks([])

    plt.show()