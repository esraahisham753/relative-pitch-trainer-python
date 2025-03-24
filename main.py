from flask import Flask, render_template
import numpy as np
import pygame
import time
import math
import csv
import random

app = Flask(__name__)

pygame.mixer.init(frequency=44100, size=-16, channels=2)

class Note:
    note_letters = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

    def __init__(self, note, frequency):
        self._note = note
        self._frequency = frequency
    
    def __str__(self):
        return f"{self.note} ({self.frequency} Hz)"
    
    @property
    def note(self):
        return self._note
    
    @note.setter
    def note(self, value):
        if value[:-1] not in Note.note_letters:
            raise ValueError(f"Invalid note: {value}")
        self._note = value
    
    @property
    def frequency(self):
        return self._frequency
    
    @frequency.setter
    def frequency(self, value):
        self._frequency = value
            
    
    @classmethod
    def get_notes(cls):
        with open('musical-notes.csv', 'r') as f:
            reader = csv.DictReader(f)
            notes = []

            for row in reader:
                note = cls(row['Note'] + row['Octave'], row['Frequency'])
                notes.append(note)
            
            return notes
    
    def play(self, duration=1, volume=0.5):
        sample_rate = 44100
        n_samples = int(round(duration * sample_rate))
        buf = pygame.sndarray.make_sound(
            pygame.surfarray.array3d(
                pygame.Surface((n_samples, 2))
            )
        )
        sample_array = buf.get_raw()
        max_sample = 2 ** (16 - 1) - 1

        for i in range(n_samples):
            sample = max_sample * volume * math.sin(2 * math.pi * self.frequency * i / sample_rate)
            sample_array[4*i] = int(sample) & 0xff
            sample_array[4*i + 1] = (int(sample) >> 8) & 0xff
            sample_array[4*i + 2] = int(sample) & 0xff
            sample_array[4*i + 3] = (int(sample) >> 8) & 0xff
        
        buf.play()
        time.sleep(duration)

class Interval:
    interval_names = ['Unison', 'Minor Second', 'Major Second', 'Minor Third', 'Major Third', 'Perfect Fourth', 'Tritone', 'Perfect Fifth', 'Minor Sixth', 'Major Sixth', 'Minor Seventh', 'Major Seventh', 'Octave']

    def __init__(self, first_note, second_note, name, semitones):
        self._first_note = first_note
        self._second_note = second_note
        self._name = name
        self._semitones = semitones
    
    def __str__(self):
        return f"{self.first_note} - {self.second_note} - {self.name} - {self.semitones} semitones"
    
    @property
    def first_note(self):
        return self._first_note
    
    @first_note.setter
    def first_note(self, value):
        self._first_note = value

    @property
    def second_note(self):
        return self._second_note
    
    @second_note.setter
    def second_note(self, value):
        self._second_note = value
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if value not in Interval.interval_names:
            raise ValueError(f"Invalid interval name: {value}")
        self._name = value
    
    @property
    def semitones(self):
        return self._semitones
    
    @semitones.setter
    def semitones(self, value):
        if value < 0 or value > 12:
            raise ValueError("Semitones must be between 0 and 12")
        self._semitones = value
    
    @classmethod
    def get_intervals(cls):
        intervals = []

        with open('intervals.csv', 'r') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                intervals.append({'interval': row['Interval'], 'semitones': int(row['Semitones']), 'level': int(row['Level'])})
        return intervals
    
    @classmethod
    def generate_asc_interval(cls, notes, interval, intervals):
       semitones = cls.map_inter_to_semitones(intervals, interval)
       first_note_ind = random.randint(0, len(notes) - semitones - 1)
       second_note_ind = first_note_ind + semitones

       return cls(notes[first_note_ind], notes[second_note_ind], interval, semitones)
    
    @classmethod
    def generate_desc_interval(cls, notes, interval, intervals):
       semitones = cls.map_inter_to_semitones(intervals, interval)
       first_note_ind = random.randint(semitones, len(notes) - 1)
       second_note_ind = first_note_ind - semitones

       return cls(notes[first_note_ind], notes[second_note_ind], interval, semitones)
    
    @classmethod
    def map_inter_to_semitones(cls, intervals, interval):
        for inter in intervals:
            if inter['interval'] == interval:
                return inter['semitones']
    
    @classmethod
    def get_level_intervals(cls, intervals, level):
        return [inter for inter in intervals if inter['level'] <= level]
    

class Question:
    def __init__(self, choices, correct_choice, interval):
        self._choices = choices
        self._correct_choice = correct_choice
        self._interval = interval
    
    def __str__(self):
        return f"{self.choices} - {self.correct_choice} - {self.interval}"
    
    @property
    def choices(self):
        return self._choices
    
    @choices.setter
    def choices(self, value):
        self._choices = value
    
    @property
    def correct_choice(self):
        return self._correct_choice
    
    @correct_choice.setter
    def correct_choice(self, value):
        if value not in self.choices:
            raise ValueError("Correct choice must be one of the choices")
        self._correct_choice = value
    
    @property
    def interval(self):
        return self._interval
    
    @interval.setter
    def interval(self, value):
        self._interval = value
    
    def check_answer(self, choice):
        return choice == self.correct_choice
   

class Relative_Pitch_Trainer:
    def __init__(self, num_questions, level, direction, cur_question=0, intervals=[], notes=[]):
        self._num_questions = num_questions
        self._level = level
        self._direction = direction
        self._cur_question = cur_question
        self._intervals = intervals
        self._notes = notes
    
    @property
    def num_questions(self):
        return self._num_questions
    
    @num_questions.setter
    def num_questions(self, value):
        if value < 1 or value > 100:
            raise ValueError("Number of questions must be between 1 and 100")
        self._num_questions = value
    
    @property
    def level(self):
        return self._level
    
    @level.setter
    def level(self, value):
        if value < 1 or value > 5:
            raise ValueError("Level must be between 1 and 5")
        self._level = value
    
    @property
    def direction(self):
        return self._direction
    
    @direction.setter   
    def direction(self, value):
        if value not in ['asc', 'desc', 'both']:
            raise ValueError("Direction must be either 'asc' or 'desc' or 'both'")
        self._direction = value
    
    @property
    def cur_question(self):
        return self._cur_question
    
    @cur_question.setter
    def cur_question(self, value):
        if value < 0 or value > self.num_questions:
            raise ValueError("Current question must be between 0 and the number of questions")
        self._cur_question = value
    
    @property
    def intervals(self):
        return self._intervals
    
    @intervals.setter
    def intervals(self, value):
        self._intervals = value
    
    @property
    def notes(self):
        return self._notes
    
    @notes.setter
    def notes(self, value):
        self._notes = value
    
    def choose_direction(self):
        if self.direction == 'both':
            return random.choice(['asc', 'desc'])
        return self.direction
    
    def get_choices(self):
        choices = []

        for interval in self.intervals:
            if interval['level'] <= self.level:
                choices.append(interval['interval'])
        
        return choices
    
    def choose_interval(self):
        sub_intervals = Interval.get_level_intervals(self.intervals, self.level)
        return random.choice(sub_intervals)['interval']
    
    def generate_question(self):
        if self.cur_question > self.num_questions:
            return None
        
        if self.choose_direction() == 'asc':
            inter = Interval.generate_asc_interval(self.notes, self.choose_interval(), self.intervals)
        inter = Interval.generate_desc_interval(self.notes, self.choose_interval(), self.intervals)

        return Question(self.get_choices(), inter.name, inter)
   


@app.route('/')
def main():
    notes = Note.get_notes()
    intervals = Interval.get_intervals()

    print(notes[0])
    notes[0].play()

    #game = Relative_Pitch_Trainer(10, 1, 'both', 0, intervals, notes)
    #print(game.generate_question())
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)