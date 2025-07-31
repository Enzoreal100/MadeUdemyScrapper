import time
import csv
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pyautogui as auto
import pyperclip as clip
import ast
import dotenv

dotenv.load_dotenv()

auto.PAUSE = 0.7
CONSOLE_COORDS_X = 3048
CONSOLE_COORDS_Y = 2105
QUESTIONS_SCROOL_X = 759
QUESTIONS_SCROOL_Y = 492
SELECT_ANSWER_X = 1563
SELECT_ANSWER_Y = 760
SUBMIT_ANSWER_X = 2044
SUBMIT_ANSWER_Y = 1825
GOOGLE_PROJECT_ID = os.environ.get("GOOGLE_PROJECT_ID"),
GOOGLE_PRIVATE_KEY = os.environ.get("GOOGLE_PRIVATE_KEY")
GOOGLE_CLIENT_EMAIL = os.environ.get("GOOGLE_CLIENT_EMAIL")
file = 'questions.csv'


def get_question_title():
    auto.moveTo(CONSOLE_COORDS_X, CONSOLE_COORDS_Y)
    auto.click()
    clip.copy("copy(document.getElementById('question-prompt').innerText)")
    auto.hotkey('ctrl','v')
    auto.press('enter')
    return clip.paste()


def get_answers(type):
    auto.moveTo(x=CONSOLE_COORDS_X, y=CONSOLE_COORDS_Y)
    auto.click()
    clip.copy(type)
    auto.hotkey('ctrl', 'v')
    auto.press('enter')
    answers = ast.literal_eval(clip.paste())
    return answers

def print_question(dic):
    for key in dic.keys():
        if key == 'answer':
            for key2 in dic[key].keys():
                print(f'{key2}: {dic[key][key2]}')
        else:
            print(f'{key}: {dic[key]}')


def put_answers(right_answers, wrong_answers, skipped_answers):
    i=0
    for ans in right_answers:
        question['answer'][f'answer{i}'] = [ans, True]
        i+=1

    for ansNew in wrong_answers + skipped_answers:
        question['answer'][f'answer{i}'] = [ansNew, False]
        i+=1
    return


def jump_to_next_question():
    i = 0
    auto.click(QUESTIONS_SCROOL_X, QUESTIONS_SCROOL_Y)
    auto.press('tab')
    auto.press('tab')
    auto.press('enter')
    return 


question = {
    'title': '',
    'answer': {
        'answer0': [],
        'answer1': [],
        'answer2': [],
        'answer3': [],
        'answer4': []
    },
    'type': ''
}


def random_answer():
    auto.click(SELECT_ANSWER_X, SELECT_ANSWER_Y)
    auto.click(SUBMIT_ANSWER_X, SUBMIT_ANSWER_Y)
    return


def append_to_sheet(question):
    new_line = [
        'teste',
        question['title'],
    ]

    for key in question['answer'].keys():
        if question['answer'][key] == []:
            break
        new_line.append(question['answer'][key][0])
    new_line.append('testeCorreta')
    new_line.append('testeTipo')

    values = new_line


    with open(file, 'a', newline='', encoding='utf=8') as file_csv:
        writer = csv.writer(file_csv)
        writer.writerow(values)
    


question['title'] = get_question_title()
right_answers = get_answers("copy(Array.from(document.querySelectorAll('.answer-result-pane--answer-correct--PLOEU .answer-result-pane--answer-body--cDGY6 .ud-heading-md.rt-scaffolding')).map(el => el.innerText))")
wrong_answers = get_answers("copy(Array.from(document.querySelectorAll('.answer-result-pane--answer-incorrect--vFyOv .answer-result-pane--answer-body--cDGY6 .ud-heading-md.rt-scaffolding')).map(el => el.innerText))")
skipped_answers = get_answers("copy(Array.from(document.querySelectorAll('.answer-result-pane--answer-skipped--1NDPn .answer-result-pane--answer-body--cDGY6 .ud-heading-md.rt-scaffolding')).map(el => el.innerText))")
put_answers(right_answers, wrong_answers, skipped_answers)
jump_to_next_question()
# print_question(question)
append_to_sheet(question)
#random_answer()
