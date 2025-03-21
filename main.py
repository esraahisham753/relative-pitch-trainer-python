from flask import Flask, render_template
import pygame
import time
import math
import csv

app = Flask(__name__)

class Note:
    note_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    octaves = range(9)

    def __init__(self, note, octave, frequency):
        self._note = note
        self._frequency = frequency
        self._octave = octave
    
    @property
    def note(self):
        return self._note
    
    @note.setter
    def note(self, value):
        if value not in Note.note_letters:
            raise ValueError(f"Invalid note: {value}")
        self._note = value
    
    @property
    def frequency(self):
        return self._frequency
    
    @frequency.setter
    def frequency(self, value):
        self._frequency = value
    
    @property
    def octave(self):
        return self._octave
    
    @octave.setter
    def octave(self, value):
        if value not in Note.octaves:
            raise ValueError(f"Invalid octave: {value}")
        self._octave = value
    
    @classmethod
    def generate_notes(cls):
        for note in cls.note_letters:
            ...
    
    @classmethod
    def get_notes(cls):
        with open('musical-notes.csv', 'r') as f:
            reader = csv.DictReader(f)
            notes = []

            for i, row in enumerate(reader):
                note = cls(row['Note'], )

class Interval:
    def __init__(self, first_note, second_note):
        self._first_note = first_note
        self._second_note = second_note
    
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
    def second_note(self, value:str):
        self._second_note = value
        

@app.route('/')
def main():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)