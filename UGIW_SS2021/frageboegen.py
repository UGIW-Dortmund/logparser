import numpy as np
from lib_logparser import *
    

y1_names = ['Behindernd', 'Kompliziert', 'Ineffizient', 'Verwirrend', 'Langweilig', 'Uninteressant', 'Konventionell', 'Herkömmlich']
y2_names = ['Unterstützend', 'Einfach', 'Effizient', 'Übersichtlich', 'Spannend', 'Interessant', 'Originell', 'Neuartig']
legend = ['AR: Greifen/Auswählen', 'AR: Bestätigen', 'AR: Fokussieren', 'AR: Fortbewegen', 'VR: Greifen/Auswählen', 'VR: Bestätigen', 'VR: Fokussieren', 'VR: Fortbewegen']

x = np.array([
    [6,6.4,5.8,5.8,5,5.8,5.4,6],
    [6.4,6.4,6.4,6.6,5.6,5.6,5.6,6],
    [5.8,6,5.8,5.8,5.4,5.4,5.8,5.6],
    [4.66666666666667,6.66666666666667,4.33333333333333,6.33333333333333,4.66666666666667,5,4,3.66666666666667],
    [7,7,6.83333333333333,6.66666666666667,6,6.16666666666667,4.6,4.8],
    [6.83333333333333,6.5,6.66666666666667,6.66666666666667,6,6.33333333333333,5.2,4],
    [6.83333333333333,6.5,6.66666666666667,6,5.83333333333333,6,3.8,3.6],
    [5.83333333333333,5.83333333333333,6.16666666666667,5.83333333333333,5.5,5.83333333333333,4.8,4.8]
])

questionaire(x[0], 1, 7, legend[0], 'images/AR_Greifen_Auswaehlen', y1_names, y2_names, 'n=5')
questionaire(x[1], 1, 7, legend[1], 'images/AR_Bestaetigen', y1_names, y2_names, 'n=5')
questionaire(x[2], 1, 7, legend[2], 'images/AR_Fokussieren', y1_names, y2_names, 'n=5')
questionaire(x[3], 1, 7, legend[3], 'images/AR_Fortbewegen', y1_names, y2_names, 'n=3')
questionaire(x[4], 1, 7, legend[4], 'images/VR_Greifen_Auswaehlen', y1_names, y2_names, 'n=5')
questionaire(x[5], 1, 7, legend[5], 'images/VR_Bestaetigen', y1_names, y2_names, 'n=5')
questionaire(x[6], 1, 7, legend[6], 'images/VR_Fokussieren', y1_names, y2_names, 'n=5')
questionaire(x[7], 1, 7, legend[7], 'images/VR_Fortbewegen', y1_names, y2_names, 'n=5')

questionaire(x, 1, 7, 'Actions', 'images/actions', y1_names, y2_names, 'n=5', legend=legend)


x = np.array([[6.166666667,6.25,6.416666667,6.166666667,6,6.5,6.5,6.666666667,4,5,6.5,5.916666667,6.272727273,6.5,6.090909091,5.583333333,6.25,6,6.333333333],
             [6.714285714,6.714285714,6.714285714,6.714285714,6.285714286,6.857142857,6.571428571,6.857142857,3.666666667,5.2,6.571428571,6.142857143,6.333333333,6.714285714,6.142857143,5.857142857,6.571428571,6.428571429,6.714285714],
             [5.4,5.6,6,5.4,5.6,6,6.4,6.4,4.333333333,4.666666667,6.4,5.6,6.2,6.2,6,5.2,5.8,5.4,5.8]])
y_names = ['1. Insgesamt war ich zufrieden, wie einfach die Anwendung zu bedienen war',
           '2. Es war einfach die Anwendung zu benutzen',
           '3. Ich konnte meine Aufgaben effektiv in der Anwendung erledigen',
           '4. Mit dieser Anwendung konnte ich die Aufgaben schnell erledigen',
           '5. Ich war in der Lage, die Aufgabe mit der Anwendung effizient zu erledigen',
           '6. Ich fühle mich wohl im Umgang mit der Anwendung',
           '7. Der Umgang mit der Anwendung war leicht zu erlernen',
           '8. Ich glaube, dass ich schnell produktiv wurde bei der Nutzung der Anwendung',
           '9. Die Anwendung gibt Fehlermeldungen aus, die mir klar sagen, wie ich Probleme beheben kann',
           '10. Sobald ich mit der Anwendung einen Fehler mache, kann ich diesen schnell und einfach rückgängig machen',
           '11. Die mit der Anwendung bereitgestellten Informationen sind klar zu verstehen',
           '12. Es ist leicht, benötigte Informationen zu finden',
           '13. Die Informationen zu dieser Anwendung sind leicht verständlich',
           '14. Die Informationen halfen mir effektiv, die Aufgaben und Szenarien zu erledigen',
           '15. Die Organisation der Informationen auf dem Anwendungsbildschirm ist klar zu verstehen',
           '16. Die Gestaltung (Ästhetik) der Anwendung ist angenehm',
           '17. Ich nutze gerne die Interaktionsmöglichkeiten der Anwendung',
           '18. Die Interaktionen fühlten sich natürlich und intuitiv an',
           '19. Insgesamt bin ich mit der Anwendung zufrieden']
questionaire(x, 1, 7, 'Anwendung', 'images/Anwendung', y_names, text='n=12', legend=['Gesamt', 'VR', 'AR'])








pieChart(['Männlich', 'Divers', 'Weiblich', 'Keine Angabe'], [6, 0, 3, 0], '', 'images/Geschlecht', 'n=9')
pieChart(['Rechts', 'Links'], [9, 0], '', 'images/dominante_Hand', 'n=9')
pieChart(['Ja', 'Nein'], [1, 8], '', 'images/Erfahrungen_AR', 'n=9')
pieChart(['Ja', 'Nein'], [4, 5], '', 'images/Erfahrungen_VR', 'n=9')
pieChart(['Unter 18', '18-21', '22-25', '26-30', '31-35', 'Über 35'], [0,1,1,4,1,2], '', 'images/Altersgruppe', 'n=9')









































y1_names = ['Obstructive', 'Complicated', 'Inefficient', 'Confusing', 'Boring', 'Uninteresting', 'Conventional', 'Traditional']
y2_names = ['Supportive', 'Easy', 'Efficient', 'Clear', 'Exciting', 'Interesting', 'Original', 'Innovative']
legend = ['AR: Grab/Select', 'AR: Confirm', 'AR: Focusing', 'AR: Moving', 'VR: Grab/Select', 'VR: Confirm', 'VR: Focusing', 'VR: Moving']

x = np.array([
    [6,6.4,5.8,5.8,5,5.8,5.4,6],
    [6.4,6.4,6.4,6.6,5.6,5.6,5.6,6],
    [5.8,6,5.8,5.8,5.4,5.4,5.8,5.6],
    [4.66666666666667,6.66666666666667,4.33333333333333,6.33333333333333,4.66666666666667,5,4,3.66666666666667],
    [7,7,6.83333333333333,6.66666666666667,6,6.16666666666667,4.6,4.8],
    [6.83333333333333,6.5,6.66666666666667,6.66666666666667,6,6.33333333333333,5.2,4],
    [6.83333333333333,6.5,6.66666666666667,6,5.83333333333333,6,3.8,3.6],
    [5.83333333333333,5.83333333333333,6.16666666666667,5.83333333333333,5.5,5.83333333333333,4.8,4.8]
])

questionaire(x[0], 1, 7, legend[0], 'images/en_AR_Greifen_Auswaehlen', y1_names, y2_names, 'n=5')
questionaire(x[1], 1, 7, legend[1], 'images/en_AR_Bestaetigen', y1_names, y2_names, 'n=5')
questionaire(x[2], 1, 7, legend[2], 'images/en_AR_Fokussieren', y1_names, y2_names, 'n=5')
questionaire(x[3], 1, 7, legend[3], 'images/en_AR_Fortbewegen', y1_names, y2_names, 'n=3')
questionaire(x[4], 1, 7, legend[4], 'images/en_VR_Greifen_Auswaehlen', y1_names, y2_names, 'n=5')
questionaire(x[5], 1, 7, legend[5], 'images/en_VR_Bestaetigen', y1_names, y2_names, 'n=5')
questionaire(x[6], 1, 7, legend[6], 'images/en_VR_Fokussieren', y1_names, y2_names, 'n=5')
questionaire(x[7], 1, 7, legend[7], 'images/en_VR_Fortbewegen', y1_names, y2_names, 'n=5')

questionaire(x, 1, 7, 'Actions', 'images/en_actions', y1_names, y2_names, 'n=5', legend=legend)


x = np.array([[6.166666667,6.25,6.416666667,6.166666667,6,6.5,6.5,6.666666667,4,5,6.5,5.916666667,6.272727273,6.5,6.090909091,5.583333333,6.25,6,6.333333333],
             [6.714285714,6.714285714,6.714285714,6.714285714,6.285714286,6.857142857,6.571428571,6.857142857,3.666666667,5.2,6.571428571,6.142857143,6.333333333,6.714285714,6.142857143,5.857142857,6.571428571,6.428571429,6.714285714],
             [5.4,5.6,6,5.4,5.6,6,6.4,6.4,4.333333333,4.666666667,6.4,5.6,6.2,6.2,6,5.2,5.8,5.4,5.8]])
y_names = ['1. Overall, I was pleased with how easy the application was to use',
           '2. It was easy to use the application',
           '3. I was able to complete my tasks effectively in the application',
           '4. I was able to complete tasks quickly using this application',
           '5. I was able to complete the task efficiently using the application',
           '6. I feel comfortable using the application',
           '7. It was easy to learn how to use the application',
           '8. I believe I quickly became productive in using the application',
           '9. The application gives error messages that clearly tell me how to fix problems',
           '10. Once I make a mistake with the application, I can quickly and easily undo it',
           '11. The information provided with the application is clear to understand',
           '12. It is easy to find needed information',
           '13. The information provided with this application is easy to understand',
           '14.The information effectively helped me to complete the tasks and scenarios',
           '15. The organization of the information on the application screen is clear to understand',
           '16. the design (aesthetics) of the application is pleasant',
           '17. I like using the interaction features of the application',
           '18. The interactions felt natural and intuitive',
           '19. Overall, I am satisfied with the application']
questionaire(x, 1, 7, 'Application', 'images/en_Anwendung', y_names, text='n=12', legend=['Gesamt', 'VR', 'AR'])








pieChart(['Male', 'Divers', 'Female', 'Keine Angabe'], [6, 0, 3, 0], '', 'images/en_Geschlecht', 'n=9')
pieChart(['Right', 'Left'], [9, 0], '', 'images/en_dominante_Hand', 'n=9')
pieChart(['Yes', 'No'], [1, 8], '', 'images/en_Erfahrungen_AR', 'n=9')
pieChart(['JYes', 'No'], [4, 5], '', 'images/en_Erfahrungen_VR', 'n=9')
pieChart(['Under 18', '18-21', '22-25', '26-30', '31-35', 'Over 35'], [0,1,1,4,1,2], '', 'images/en_Altersgruppe', 'n=9')
