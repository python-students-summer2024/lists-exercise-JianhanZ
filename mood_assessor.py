
import datetime
import os

def assess_mood():
    today = str(datetime.date.today())
    
    if not os.path.exists('data'):
        os.makedirs('data')

    if is_mood_recorded(today):
        print("Sorry, you have already entered your mood today.")
        return

    mood = get_valid_mood()
    mood_value = mood_to_int(mood)
    record_mood(today, mood_value)

    diagnose_disorder()

def is_mood_recorded(today):
    try:
        with open('data/mood_diary.txt', 'r') as file:
            lines = file.readlines()
            if any(today in line for line in lines):
                return True
    except FileNotFoundError:
        return False
    return False

def get_valid_mood():
    valid_moods = {"happy", "relaxed", "apathetic", "sad", "angry"}
    while True:
        mood = input("Please enter your current mood (happy, relaxed, apathetic, sad, angry): ").strip().lower()
        if mood in valid_moods:
            return mood
        print("Invalid input, please try again.")

def mood_to_int(mood):
    mood_mapping = {
        "happy": 2,
        "relaxed": 1,
        "apathetic": 0,
        "sad": -1,
        "angry": -2
    }
    return mood_mapping[mood]

def record_mood(date, mood_value):
    with open('data/mood_diary.txt', 'a') as file:
        file.write(f"{date},{mood_value}\n")

def diagnose_disorder():
    try:
        with open('data/mood_diary.txt', 'r') as file:
            lines = file.readlines()
            if len(lines) < 7:
                return
            last_7_days = lines[-7:]
            moods = [int(line.split(',')[1]) for line in last_7_days]
            diagnose_based_on_moods(moods)
    except FileNotFoundError:
        return

def diagnose_based_on_moods(moods):
    mood_strings = ["angry", "sad", "apathetic", "relaxed", "happy"]
    mood_count = {"happy": 0, "sad": 0, "apathetic": 0}

    for mood in moods:
        if mood == 2:
            mood_count["happy"] += 1
        elif mood == -1:
            mood_count["sad"] += 1
        elif mood == 0:
            mood_count["apathetic"] += 1

    if mood_count["happy"] >= 5:
        diagnosis = "manic"
    elif mood_count["sad"] >= 4:
        diagnosis = "depressive"
    elif mood_count["apathetic"] >= 6:
        diagnosis = "schizoid"
    else:
        avg_mood = round(sum(moods) / 7)
        diagnosis = mood_strings[avg_mood + 2]

    print(f"Your diagnosis: {diagnosis}!")