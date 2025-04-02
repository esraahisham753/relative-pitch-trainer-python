from project import get_notes, get_intervals, map_inter_to_semitones
from music import Note

def test_get_notes():
    notes = get_notes()
    assert isinstance(notes[0], Note)
    assert len(notes) == 108
    assert notes[0].note == "C0"
    assert notes[0].midi == 12

def test_get_intervals():
    intervals = get_intervals()
    assert len(intervals) == 13
    assert intervals[0]['interval'] == 'Unison'
    assert intervals[0]['semitones'] == 0
    assert intervals[0]['level'] == 1

def test_map_inter_to_semitones():
    intervals = get_intervals()
    assert map_inter_to_semitones(intervals, 'Major Third') == 4
    assert map_inter_to_semitones(intervals, 'Perfect Fifth') == 7