# Es Relative Pitch Trainer
## Video Demo:  https://youtu.be/CIHrItsR0AE?si=jdngLp_-aYBoyjsF
## Description:

### Music Theory Background
To figure out songs, you need to identify each note in the melody. Some people are born with perfect pitch, which means they can recognize every single note played. However, not all people, including musicians, have the gift of perfect pitch. Instead, they use a different technique called Relative Pitch. This technique relies on recognizing the sound of each interval (the distance between two notes) without needing to know the exact notes.

### What the App Provides
The app offers 5 training levels. Each level includes the intervals from the previous levels and introduces new ones. You can find the intervals and their corresponding levels in the `intervals.csv` file.  
The app allows you to customize your training session in various ways. You can select the level (1-5), the number of questions (1-100), and the direction of intervals (Ascending, Descending, or Both).

## Project Guide
1. Create a virtual environment for the project:
   ```bash
   python -m venv myenv
   ```

2. Activate the virtual environment:
   - For Windows users:
     ```bash
     ./myenv/Scripts/activate
     ```
   - For other users:
     ```bash
     source ./myenv/bin/activate
     ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:
   ```bash
   python project.py
   ```

## How to Play
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
3. Enter the number of questions (1-100).
4. Click the Start button.
5. Listen to the two notes of the interval and try to select the correct answer.
6. The result screen will show whether your answer is correct or not, along with your current progress in the session (current question number).
7. When there are no more questions, you will see your final score and a button to start a new training session.

## Code Structure

```python
project/
|
|- project.py          # Contains the Pygame UI and controls drawing functions
|- music.py            # Contains the music building blocks as encapsulated classes
|- test_project.py     # Contains custom function tests
|- requirements.txt    # Lists project dependencies
|- intervals.csv       # Contains interval information
|- musical-notes.csv   # Contains piano note information
|- background.jpg      # The UI background image
```



