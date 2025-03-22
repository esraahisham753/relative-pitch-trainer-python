from flask import Flask, render_template
import pygame
import time
import math
import csv
import random

app = Flask(__name__)

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
    
    
class Relative_Pitch_Trainer:
    def __init__(self, num_questions, level, direction, cur_question=0):
        self._num_questions = num_questions
        self._level = level
        self._direction = direction
        self._cur_question = cur_question
    
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

@app.route('/')
def main():
    notes = Note.get_notes()
    intervals = Interval.get_intervals()

    print(Interval.get_level_intervals(intervals, 2))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)