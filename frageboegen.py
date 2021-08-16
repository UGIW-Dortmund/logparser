import matplotlib.pyplot as plt
import numpy as np


def questionaire(rating, ratingMin, ratingMax, title, names1, names2=None, text=None, legend=None):
    y = np.arange(rating.shape[-1], 0, -1)
    
    fig, ax1 = plt.subplots()
    plt.xticks(np.arange(ratingMin, ratingMax+1, 1))
    plt.yticks(y, names1)
    ax1.set_xlim(ratingMin, ratingMax)
    ax1.grid()
    ax1.set(xlabel='Wertung', title=title)
        
    
    if (len(rating.shape) == 1):
        ax1.plot(rating, y)
    else:
        for r in rating:
            ax1.plot(r, y)
    
    if names2 != None:
        ax2 = ax1.twinx()
        ax2.set_xlim(ratingMin, ratingMax)
        plt.xticks(np.arange(ratingMin, ratingMax+1, 1))
        plt.yticks(y, names2)
    
    props = dict(boxstyle='round', facecolor='wheat', alpha=1.0)
    ax1.text(0.1, 0.95, text, transform=ax1.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)
    
    ax1.set_box_aspect(2)
    if legend != None:
        ax1.legend(legend, loc="lower left")
    
    fig.savefig(title + '.svg')
    plt.show()
    
def pieChart(labels, sizes, title, text):
    fig, ax = plt.subplots()
    ax.set(title=title)
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    props = dict(boxstyle='round', facecolor='wheat', alpha=1.0)
    ax.text(0.1, 0.95, text, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

    fig.savefig(title + '.svg')
    plt.show()
    

y1_names = ['Behindernd', 'Kompliziert', 'Ineffizient', 'Verwirrend', 'Langweilig', 'Uninteressant', 'Konventionell', 'Herkömmlich']
y2_names = ['Unterstützend', 'Einfach', 'Effizient', 'Übersichtlich', 'Spannend', 'Interessant', 'Originell', 'Neuartig']

x = np.array([6,6.4,5.8,5.8,5,5.8,5.4,6])
questionaire(x, 1, 7, 'AR: Greifen Auswählen', y1_names, y2_names, 'n=5')

x = np.array([6.4,6.4,6.4,6.6,5.6,5.6,5.6,6])
questionaire(x, 1, 7, 'AR: Bestätigen', y1_names, y2_names, 'n=5')

x = np.array([5.8,6,5.8,5.8,5.4,5.4,5.8,5.6])
questionaire(x, 1, 7, 'AR: Fokussieren', y1_names, y2_names, 'n=5')

x = np.array([4.66666666666667,6.66666666666667,4.33333333333333,6.33333333333333,4.66666666666667,5,4,3.66666666666667])
questionaire(x, 1, 7, 'AR: Fortbewegen', y1_names, y2_names, 'n=3')



x = np.array([7,7,6.83333333333333,6.66666666666667,6,6.16666666666667,4.6,4.8])
questionaire(x, 1, 7, 'VR: Greifen Auswählen', y1_names, y2_names, 'n=5')

x = np.array([6.83333333333333,6.5,6.66666666666667,6.66666666666667,6,6.33333333333333,5.2,4])
questionaire(x, 1, 7, 'VR: Bestätigen', y1_names, y2_names, 'n=5')

x = np.array([6.83333333333333,6.5,6.66666666666667,6,5.83333333333333,6,3.8,3.6])
questionaire(x, 1, 7, 'VR: Fokussieren', y1_names, y2_names, 'n=5')

x = np.array([5.83333333333333,5.83333333333333,6.16666666666667,5.83333333333333,5.5,5.83333333333333,4.8,4.8])
questionaire(x, 1, 7, 'VR: Fortbewegen', y1_names, y2_names, 'n=5')


x = np.array([[6.166666667,6.25,6.416666667,6.166666667,6,6.5,6.5,6.666666667,4,5,6.5,5.916666667,6.272727273,6.5,6.090909091,5.583333333,6.25,6,6.333333333],
             [6.714285714,6.714285714,6.714285714,6.714285714,6.285714286,6.857142857,6.571428571,6.857142857,3.666666667,5.2,6.571428571,6.142857143,6.333333333,6.714285714,6.142857143,5.857142857,6.571428571,6.428571429,6.714285714],
             [5.4,5.6,6,5.4,5.6,6,6.4,6.4,4.333333333,4.666666667,6.4,5.6,6.2,6.2,6,5.2,5.8,5.4,5.8]])
y_names = ['1. Insgesamt war ich zufrieden, wie einfach die Anwendung zu bedienen war','2. Es war einfach die Anwendung zu benutzen','3. Ich konnte meine Aufgaben effektiv in der Anwendung erledigen','4. Mit dieser Anwendung konnte ich die Aufgaben schnell erledigen','5. Ich war in der Lage, die Aufgabe mit der Anwendung effizient zu erledigen','6. Ich fühle mich wohl im Umgang mit der Anwendung','7. Der Umgang mit der Anwendung war leicht zu erlernen','8. Ich glaube, dass ich schnell produktiv wurde bei der Nutzung der Anwendung','9. Die Anwendung gibt Fehlermeldungen aus, die mir klar sagen, wie ich Probleme beheben kann','10. Sobald ich mit der Anwendung einen Fehler mache, kann ich diesen schnell und einfach rückgängig machen','11. Die mit der Anwendung bereitgestellten Informationen (Einweisung, Bildschirmmeldungen, UI-Abbildungen) sind klar zu verstehen','12. Es ist leicht, benötigte Informationen zu finden','13. Die Informationen zu dieser Anwendung sind leicht verständlich','14. Die Informationen halfen mir effektiv, die Aufgaben und Szenarien zu erledigen','15. Die Organisation der Informationen auf dem Anwendungsbildschirm ist klar zu verstehen','16. Die Gestaltung (Ästhetik) der Anwendung ist angenehm','17. Ich nutze gerne die Interaktionsmöglichkeiten der Anwendung','18. Die Interaktionen fühlten sich natürlich und intuitiv an','19. Insgesamt bin ich mit der Anwendung zufrieden']
questionaire(x, 1, 7, 'Anwendung', y_names, text='n=12', legend=['Gesamt', 'VR', 'AR'])








pieChart(['Männlich', 'Weiblich'], [6, 3], 'Geschlecht', 'n=9')
pieChart(['Rechts', 'Links'], [9, 0], 'Ihre dominante Hand', 'n=9')
pieChart(['Ja', 'Nein'], [1, 8], 'Haben Sie Erfahrung im Umgang mit Augmented Reality (AR)?', 'n=9')
pieChart(['Ja', 'Nein'], [4, 5], 'Haben Sie Erfahrung im Umgang mit Virtual Reality (VR)?', 'n=9')
