from typing import Self


class Course:
    def __init__(self, name, startDate, endDate, weeklyHours, currentHours):
        Self.name = name;
        Self.startDate = startDate;
        Self.endDate = endDate;
        Self.weeklyHours = weeklyHours;
        Self.currentHours = currentHours;

def hours_left():
        return Self.weeklyHours - Self.currentHours

def setweeklyhours(hours):
     weeklyHours = hours

def setcurrentHours(hours):
     currentHours = hours

