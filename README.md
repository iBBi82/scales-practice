# Scales Practice
#### Video Demo:
#### Description: This program enables novice student musicians to learn the common musical major scales through interactive buttons, and by reading clefs and hearing sample audio of the scales. Students can also save their scores (with score multipliers) to a leaderboard, to encourage friendly competition against their fellow classmates and friends.

<br>

## Inspiration
When I first read through the specifications of the Final Project, I was immediately struck with the question “How do I make my project meaningful?” Having acquired an extensive toolbox of problem-solving skills and knowledge of various programming languages, I wished to create something that went beyond making it for the “sake of it.” It needed to have some sort of purpose and ability to impact somebody, while also relating it to any interests of mine.

Given my passion for instrumental music and my desire to educate others, I found the perfect opportunity to develop a system that would help beginning students in Concert Band improve their musical skills and feel confident in their playing ability. After some research and personal reflection on what I personally struggled with as a beginner, I decided to focus on note identification and practicing scales. This topic applies to students playing any instrument and is vital for them to succeed in playing more full pieces. Since it was made by a student for students, it also had to be accessible and easy to use, which is why I chose to implement it in the form of a Flask web application.

<br>

## Structure and Layout
Since I had a limited time span due to other circumstances, I couldn’t go too broad. The goal was simple: let students pick a scale, practice it, and see how well they performed. This roughly meant having options for various scales, a system to let students play the notes of the chosen scale, ways to track how well they are doing, and a plan to display their results. After some brainstorming on paper, I came up with the initial plan explained below:

- Students “log-in” with school email
- Students pick one of the first four major scales they learn
- Students pick a clef
- The chosen scale in the chosen clef is displayed
- Students play the notes
- Their result is displayed and the student can save it to a leaderboard
- Leaderboards for each of the four scales are available and only keep track of highest scores for a certain user; top 3 are highlighted; ranks are same for tied-scores

<br>

## The Immediate Challenge

Inputting audio. Band isn’t band without the instruments. Students don't just learn to read music and be technically fluent with it digitally and on paper. They develop specific motor skills, breathing techniques, and physical abilities to make their instrument sound beautiful. And that means requiring my application to take in audio input and convert it to the literature values for musical notes. After conducting research on the `pyaudio` module, I learned that converting audio input to notes required the use of digital signal processing and a Fast Fourier Transform to convert audio signals to frequencies that can be compared to standard note frequencies. Not only that, but there was an additional challenge of that students play notes back to back, and instruments also have features like timbre, making it more difficult to convert audio to notes. With my short timeframe and relatively newfound skills, I decided to stick to clickable buttons on the site. While it did come as unsettling to me, I simply believe I did not have the ability to implement something of this scope in a few weeks yet. This was my first major design challenge that shaped how the rest of my web application functioned.

<br>

## FILES

### app.py
This file contains the Flask code that allows communication between the HTML pages to the actual “server”. It ensures users are routed to the correct pages at the correct time, and the correct data is sent from page to page and properly updated in the SQL tables.

### layout.html
Defines a template for all the other HTML pages to follow, including the tab title, appropriate favicons, navigation bar, mobile responsiveness, and more. It also defines an “alert” block for each page, which is used to provide instructions or relevant information to the students on each page. For example, on the join page, the alert block is used to instruct users on how to log in, while on the scales page it explains to users how to use the page itself. Finally, it also supports flashed messages as a way to indicate errors to users. For example, if they try saving a score that doesn’t exist because they never attempted the scale, then a flash message alert will pop-up and redirect them to the main page with no data being modified.

### join.html
Follows a basic login page. Every time a user views it, their session id is removed, effectively logging them out. As the application pertains to students in my school, this page ensures that emails have the correct email domain at the right indexes in the inputted text, before logging them in. It also saves the portion of the email before the domain as the username that is displayed in leaderboards.

### index.html
Has drop-down menus for users to choose their scale and clef. Initially this was all that’s present, but I realized that as a percussionist I am used to only reading the scales in Concert Pitch, and that other instruments have to “transpose” to obtain the Concert Pitch. For this reason I included a table at the bottom, for the common transposing instruments found in a concert band to help people choose the correct scale regardless of instrument.

### leaderboard.html
Has a dropdown menu for four leaderboards for each of the four scales. Uses jinja syntax to format a table, where the cell values are not known before hand. For example, I wanted to ensure that if two students had a score of 10, one would not be #1 and the other #2, as it would be unfair to whoever got assigned #2. This ensures that while scores are tied, the rank inputted stays the same.

### scales.html
Shows the clef as an image, and all the buttons as notes. It ensures that each button is linked to the correct audio file. The functionality comes from scales.js which is explained below.

### scales.js
This file is responsible for actually ensuring users can play the scales, and checking if they are correct. Firstly it ensures that when the user clicks start, the list of scale notes from app.py is saved in an appropriate array in scales.js, by using `tojson` with Jinja, when passing the list/array through scales.html. Clicking start also disables the other buttons and enables the actual note buttons, making it so the user cannot accidentally click other buttons and potentially interfere with the scoring process or redirect them somewhere.

The scoring process works by comparing each note that the user presses to the note at the same index in the actual scale. This means that it not only checks for correct notes, but also notes being played at the right position, so a user cannot just play the scale in descending order and still get all 8 notes correct. It relies heavily on the DOM to ensure these processes occur at the right time. After 8 notes are played, the process automatically stops and the user cannot play more notes. The correct notes are displayed in green, while the incorrect ones are displayed in read, and their score out of 8 is shown.

This file also keeps track of if the user has listened to the scale audio or is showing the clef at the time of clicking start. If both the audio has been played and the clef is showing, no multiplier is used. If either the audio has not been played or the clef is hidden, then the score is increased by 25%. If neither has been used, then the score is multiplied by 50%. I originally did not have this feature, but to encourage students to become more experienced and not rely on these features, as well as to increase the range of possible scores on the leaderboard, I included this.

### styles.css
This file really only is responsible for highlighting the #1, #2, and #3 ranks on the leaderboard in gold, silver, and bronze, respectively. It does so by referencing the class name of the table row, which is assigned while the leaderboard is being created through Jinja templating. Most, if not all, of the other CSS, relies on the Bootstrap framework. Bootstrap is openly free to use, and has elegant designs for the drop-down menus, navigation bars, tables, alert boxes, and more.

<br>

## Final Results

I believe this application was successful as I was able to include multiple enhancements that went beyond my original idea. While the essential function of the program was to let users play the scales and check to see if they were correct, my application ended up including support for transposing instruments, score multipliers, a constantly updating leaderboard, and proper verification to ensure students are logging in with their school email.

I am grateful to have had the opportunity to actually share this with Middle School Band students at my school. After deploying my project to Heroku, the MS Band Teacher demonstrated the application to two classes (7th and 8th grade) of 40+ students each, and shared the [URL](https://scales-practice.herokuapp.com/) with them. In the end, 15 students logged on personally and tried out the application.
