# Vegetable Samurai
## 1. Overview
**Vegetable Samurai** is a fast-paced arcade game where players need to slice various types of vegetables as they fly across the screen. Using quick reflexes and precise swipes, players must chop the vegetables into pieces while avoiding obstacles and collecting power-ups. The game features vibrant graphics, challenging levels, and addictive gameplay, making it a fun and engaging experience for all ages. Get ready to show off your slicing skills and achieve high scores in this exciting vegetable slicing game!
The game was implemented in Python, using PyGame library. The main target of the project was to implement a working game with **threading**. For that we've used **threading** library in Python. Lastly, the project was created using OOP paradigm.  
![Screenshot](/images/screenshot.png)
## 2. Installation
To get the project's source code, run:
```commandline
git clone https://github.com/MaksymMalicki/Vegetable-Samurai.git
```
To install all the project's dependencies, run:
```commandline
pip install -r requirements.txt
```
## 3. Gameplay
The game's main goal is to score as much points in given time. The player is granted points, whenever he chops the flying vegetables. The player is punished with a halving of the points, when slicing the flying bombs. Lastly, the chop lasts only for 4 seconds. When that time is gone, user is presented a prompt.
## 4. Implementation
### Threads
Timer thread - responsible for decrementing the timer by 1 each second, until 0 is reached  
Score thread - responsible for displaying the score  
Vegetables generator thread - responsible for generating new Vegetable objects that appear on the screen  
Bomb generator thread - responsible for generating new Vegetable objects that appear on the screen  
Score add thread - responsible for incrementing the score each time the vegetable is slashed  
Score divide thread - responsible for dividing the score by two each time the bomb is slashed  
Timer freeze thread - responsible for freezing time for 10 seconds each 10 points  
### Critical sections
Universal generator:
1. run_generator() - modifies the object_list, by appending the newly generated objects
2. get_objects() - tries to reach the current list of objects
3. clear_objects() - tries to clear the object_list  

Score:
1. add_points() - modifies the points counter by incrementation
2. divide_points() - modifies the points counter by dividing by two  

Timer:
1. run_timer() - locks the timer counter resource and decrements it each second
2. freeze_timer() - locks the timer counter resource and freezes the timer for 10 seconds, using sleep()  





