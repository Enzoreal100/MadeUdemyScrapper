import time
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pyautogui as auto
import pyperclip as clip
import ast
auto.PAUSE = 0.7

def get_question_title():
    auto.moveTo(x=7816, y=2570)
    auto.click()
    clip.copy("copy(document.getElementById('question-prompt').innerText)")
    auto.hotkey('ctrl','v')
    auto.press('enter')
    return clip.paste()


def get_answers(type):
    auto.moveTo(x=7816, y=2570)
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
        print(question['answer'][f'answer{i}'])
        question['answer'][f'answer{i}'] = [ans, True]
        i+=1

    for ansNew in wrong_answers + skipped_answers:
        print(question['answer'][f'answer{i}'])
        question['answer'][f'answer{i}'] = [ansNew, False]
        i+=1
    return


def jump_to_next_question():
    i = 0
    auto.click(x=5878, y=963)
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
    auto.click(x=6589, y=1196)
    auto.click(x=7197, y=2307)
    return


def append_to_sheet(question):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    credentials_dict = {
        "type": "service_account",
        "project_id": os.environ.get("GOOGLE_PROJECT_ID"),
        "private_key": os.environ.get("GOOGLE_PRIVATE_KEY").replace('\\n', '\n'),
        "client_email": os.environ.get("GOOGLE_CLIENT_EMAIL"),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "universe_domain": "googleapis.com"
    }

    creds = service_account.Credentials.from_service_account_info(
        credentials_dict, 
        scopes=SCOPES
    )
    service = build('sheets', 'v4', credentials=creds)
    SPREADSHEET_ID = os.environ.get("FOLDER")
    RANGE_NAME = 'Sheet7!A:F'  # Ajuste conforme necessário
    # Prepara os dados para inserção
    values = [[
        question['title'],
        str(question['answer']['answer0']),
        str(question['answer']['answer1']),
        str(question['answer']['answer2']),
        str(question['answer']['answer3']),
        str(question['answer']['answer4'])
    ]]

    body = {
        'values': values,
        'majorDimension': 'ROWS'
    }

    # Append na planilha
    request = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body=body
    )
    return request.execute()
    


question['title'] = get_question_title()
right_answers = get_answers("copy(Array.from(document.querySelectorAll('.answer-result-pane--answer-correct--PLOEU .answer-result-pane--answer-body--cDGY6 .ud-heading-md.rt-scaffolding')).map(el => el.innerText))")
wrong_answers = get_answers("copy(Array.from(document.querySelectorAll('.answer-result-pane--answer-incorrect--vFyOv .answer-result-pane--answer-body--cDGY6 .ud-heading-md.rt-scaffolding')).map(el => el.innerText))")
skipped_answers = get_answers("copy(Array.from(document.querySelectorAll('.answer-result-pane--answer-skipped--1NDPn .answer-result-pane--answer-body--cDGY6 .ud-heading-md.rt-scaffolding')).map(el => el.innerText))")
put_answers(right_answers, wrong_answers, skipped_answers)
jump_to_next_question()
print_question(question)
append_to_sheet(question)
#random_answer()

