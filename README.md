# Es Relative Pitch Trainer
## Video Demo:  https://youtu.be/CIHrItsR0AE?si=jdngLp_-aYBoyjsF
## Description:

### Music Theory Background
To figure out songs, you have to know each note in the melody. Some people are born with perfect pitch which means they can know exactly each single note played. But not all people or even musicians have the perfect pitch gift, so they use a different technique to figure out melody notes. This technique it called Relative Pitch. Instead of detecting single note, this technique depends on knowing the sound of each interval (The distance between two notes) regardless of what the exact notes are. 

### What the app provides
The app introduces 5 training levels, each level contains the intervals of previous level and its own level. You can find the intervals and their levels in intervals.csv file.
You can customize your training session in various ways. Select the level (1-5), number of questions (1-100) and the direction of intervals (Ascending, Descending or Both).

## Project Guide
1. I recommend creating a virtual environment for the project
```bash
python -m venv myenv
```

2. Activate the venv
    - For Windows users
      ```bash
      ./myenv/Scripts/activate
      ```
    - For other users
      ```bash
      source ./myenv/bin/activate
      ```

3. Install packages
```bash
pip install requirements.txt
```

4. Run the app
```bash
python project.py
```

## How to play
1. Choose the level:
    - Level 1: Unison, Perfect 4th, Perfect 5th, Octave
    - Level 2: Minor 3rd, Major 3rd
    - Level 3: Minor 2nd, Major 2nd
    - Level 4: Minor 6th, Major 6th, Minor 7th, Major 7th
    - Level 5: Tritone
2. Choose the interval direction: 
    - Ascending
    - Descending
    - Both
3. Write the number of question in range (1-100)
4. Click the Start button
5. Listen to the two notes of the interval and try to select the correct answer.
6. The result screen will show if your answer is correct or not along with the tracking of your current progress in the session (current question number)
7. When there's no more question you will see your final score and a button to start a new training session.

