import numpy as np
import matplotlib.pyplot as plt

def statistics(list):
    min = list[0]
    max = list[0]
    avg = list[0]
    meanDeviation = np.mean(list)
    standardDeviation = np.std(list)
    count = len(list)

    for i in list:
        if (min > i):
            min = i
        if (max < i):
            max = i
        avg += i

    avg /= count
    print(list)
    return min, max, avg, meanDeviation, standardDeviation, count


def printStatistic(statistic, name):
    print(name + ':')
    print('\tMin:', statistic[0])
    print('\tMax:', statistic[1])
    print('\tAvg:', statistic[2])
    print('\tMean:', statistic[3])
    print('\tStandard:', statistic[4])
    print('\tCount:', statistic[5])





EXTENSION = '.png'


def questionaire(rating, ratingMin, ratingMax, title, filename, names1, names2=None, text=None, legend=None):
    y = np.arange(rating.shape[-1], 0, -1)

    fig, ax1 = plt.subplots()
    plt.xticks(np.arange(ratingMin, ratingMax+1, 1))
    plt.yticks(y, names1)
    ax1.set_xlim(ratingMin-0.5, ratingMax+0.5)
    ax1.grid()
    ax1.set(xlabel='Wertung', title=title)
    ax1.set_box_aspect(2)

    if names2 != None:
        ax2 = ax1.twinx()
        plt.yticks(y, names2)
        ax2.set_box_aspect(2)

    if (len(rating.shape) == 1):
        ax1.plot(rating, y)
        if names2 != None:
            ax2.plot(rating, y)
    else:
        for r in rating:
            ax1.plot(r, y)
            if names2 != None:
                ax2.plot(r, y)


    props = dict(boxstyle='round', facecolor='wheat', alpha=1.0)
    ax1.text(0.1, 0.95, text, transform=ax1.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)


    if legend != None:
        ax1.legend(legend, loc="lower left")

    fig.savefig(filename + EXTENSION, bbox_inches='tight')
    plt.show()

    plt.close()

def pieChart(labels, sizes, title, filename, text):
    fig, ax = plt.subplots()
    explode = np.zeros(len(sizes)) + 0.0
    ax.set(title=title)
    ax.pie(sizes, labels=labels, explode=explode, autopct='%1.1f%%', shadow=True, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    props = dict(boxstyle='round', facecolor='wheat', alpha=1.0)
    ax.text(0.1, 0.95, text, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

    fig.savefig(filename + EXTENSION, bbox_inches='tight')
    plt.show()
    plt.close()
