# Mealy 

## Todo:

- ReadMe
- Comments
- RND Button Small > syntax for inputs?
- Muster-Erkennung
- Bugs/Features:
- Aktuell werden bei "Schon-lange-her-Items" auch Dinge ausgegeben,
  welche in der Zukunft liegen aber nicht, in den letzten 30 Tagen
  gekocht wurden. Wer die Zeit nicht linear betrachtet ist hier klar
  im Vorteil.
- Anzeigefehler mit zu wenig Input. Tage müssen der Reihe nach geplant werden. Kein Tag darf ausgelassen werden.
- -Affinity analysis

## What is Mealy
Mealy serves as a tool to organize your weekly meals, to inspire your planning, to plan "like" you would 
and to deliver in-depth information about your daily dinners.
To be more precise, the tool can do the following:
- Take data, store and organise it. The only data needed are the different meals. Eg: "Pasta" or "Pizza".
- Automatically assigns each input the corresponding date and weekday. Eg: I type "Pizza" and it gets saved as "Pizza, Monday, 15.04.2022".
- Shows that information in a user-friendly and oversee-able way.
- Allows the user to change data in the past and plan way in to the future. 
- Analyses the data and returns insightful feedback to the user:
  - Shows all the different meals.
  - Shows how often they have been prepared.
  - Shows which meals the user hasn't prepared in a long time.
  - Shows whether certain meals are only cooked on certain days.
- Allows the user to plan his weeks according to the analyses.

### But why?
The inspiration behind the project comes from an old Excel file on my personal computer.
Today it is quite a long list, which I used every week before going out tu buy groceries or each day, to see
what I planned to cook that evening. Quite often I checked the file for inspiration to get some ideas, because I simply
didn't know what to buy or eat for the following week. But it had a problem, it simply could only return me information,
which I put in. 

With this project I tried to reorganize my data and my tedious process into a more user-friendly experience, advance my 
programming skills and hopefully create a piece of code, which can take work away from me personally.

Problembeschreibung/Motivation
 - Warum dieses Projekt
 - Welches Problem löst das Projekt
 - Was macht das Projekt
Lückenfüller wie: "Dieses Projekt wurde im Rahmen des Programmieren2 Modules an der FHGR gemacht" oder ähnlich sind unnötig. Auch sollten keine Klarnamen, oder Orte genannt werden.


### How two use?

Betrieb
 - Welche zusätzliche Pakete müssen bei Bedarf installiert werden. (Muss im Normalfall nicht beachtet werden. Python muss nicht erwähnt werden, da das bei einem Python Projekt impliziert ist.)
 - Was muss man bei der Ausführung beachten. Was muss eventuell davor noch gemacht werden.
 - Welch Datei muss ausgeführt werden

Benutzung
- Wie wird das Projekt benutzt
- Welche Optionen oder auch Spezialitäten existieren

### Architecture
- Hier bei Bedarf eine kurze Beschreibung des Ablaufs des Programms auf Code Ebene z.B. als Ablaufdiagramm.

### Current issues and possible features
 - Was wurde nicht gelöst
 - Welche Verbesserungen könnten noch gemacht werden.


### Special input: affinity analysis
"The main idea behind this analysis is to achieve valuable insights by identifying which items are
frequently purchased together." (Saygın, 2022)Tr
Since I wanted from the beginning to somehow show, if the user always eats a specific meal on a specific day,
I spent quite some time thinking about a way to calculate exactly that.
After some clueless googling I found on the website https://www.python-exemplarisch.ch/ some information about,
affinity analysis. Now with some more precise searches I found the following pages:

- https://towardsdatascience.com/affinity-analysis-market-basket-analysis-c8e7fcc61a21
- https://www.heise.de/ratgeber/Data-Science-Warenkorbanalyse-in-30-Minuten-4425737.html

Those two website include alot of background knowledge and coding examples in python.

As mentioned I was looking for a way to show if a weekday and a meal correlate. The affinity analyse is mostly used,
to check if two things are often bought together. But in our context it is used to see if they simply "appear" together.


Of course, as the amount of data increases, the analysis becomes more accurate.
At the moment, the "support" value is particularly important. As it shows whether, for example, 
"pasta" is always eaten on Mondays.


### Sources
Saygın, E. (2022, 31. Mai). Affinity Analysis (Market Basket Analysis) - Towards Data Science. Medium. 
Abgerufen am 6. Oktober 2022, von https://towardsdatascience.com/affinity-analysis-market-basket-analysis-c8e7fcc61a21