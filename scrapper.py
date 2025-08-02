# Dear programmer
# when I made this automation, only god and I knew how it worked.
# Now, only god knows it! (i guess)
# If you are trying to optimize this routine, please increase the counter below as a warning to the next person who tries!
# total hours wasted here = 0
import time
import csv
import pyautogui as auto
import pyperclip as clip
import ast
import dotenv

dotenv.load_dotenv()

auto.PAUSE = 0.3
# where the mouse must click to write at the navigator console
CONSOLE_COORDS_X = 1539
CONSOLE_COORDS_Y = 1057
# set it to click on the first line of the question text
SELECT_ANSWER_X = 598
SELECT_ANSWER_Y = 325
# where the mouse must click to submit the answer
SUBMIT_ANSWER_X = 1031
SUBMIT_ANSWER_Y = 875
# where the mouse must click to end the test
END_TEST_COORDS_X = 884
END_TEST_COORDS_Y = 602
# where the mouse must click to continue to the next test
CONTINUE_COORDS_X = 931
CONTINUE_COORDS_Y = 875
# where the mouse must click to enter practice mode
PRAC_MODE_COORDS_X = 776
PRAC_MODE_COORDS_Y = 503
# where the mouse must click to start the test
START_TEST_COORDS_X = 1027
START_TEST_COORDS_Y = 868
# where the mouse must click to import the csv file to sheets
FILE_BUTTON_COORDS_X = 147
FILE_BUTTON_COORDS_Y = 138
# where the mouse must click to import the csv file
IMPORT_BUTTON_COORDS_X = 165
IMPORT_BUTTON_COORDS_Y = 235
# where the mouse must click to upload the csv file
UPLOAD_COORDS_X = 885
UPLOAD_COORDS_Y = 353
# where the mouse must click to search for the csv file
SEARCH_BUTTON_X = 959
SEARCH_BUTTON_Y = 711
# where the mouse must click to select the csv file
FILE_LOCATION_X = 725
FILE_LOCATION_Y = 334
# where the mouse must click to open the csv file
OPEN_BUTTON_X = 938
OPEN_BUTTON_Y = 598
# where the mouse must click to import the csv file
IMPORT_LOCAL_X = 808
IMPORT_LOCAL_Y = 588
# where the mouse must click to insert a new sheet
INSERT_NEW_SHEET_X = 835
INSERT_NEW_SHEET_Y = 632
# where the mouse must click to import the data
IMPORT_DATA_X = 1013
IMPORT_DATA_Y = 706
file = 'questions.csv'


def get_question_title():
    """Extract question title from the current test question using browser console.
    
    Returns:
        str: The text content of the question prompt.
    """
    auto.moveTo(CONSOLE_COORDS_X, CONSOLE_COORDS_Y)
    auto.click()
    clip.copy("copy(document.getElementById('question-prompt').innerText)")
    auto.hotkey('ctrl','v')
    auto.press('enter')
    return clip.paste()


def get_answers(type):
    """Execute JavaScript code in browser console to extract answer options.
    
    Args:
        type (str): JavaScript code to execute for extracting specific answer types.
        
    Returns:
        list: Parsed list of answer options from the browser.
    """
    auto.moveTo(x=CONSOLE_COORDS_X, y=CONSOLE_COORDS_Y)
    auto.click()
    clip.copy(type)
    auto.hotkey('ctrl', 'v')
    auto.press('enter')
    answers = ast.literal_eval(clip.paste())
    return answers

def print_question(dic):
    """Print question data in a formatted way to console.
    
    Args:
        dic (dict): Question dictionary containing title, answers, and type.
    """
    for key in dic.keys():
        if key == 'answer':
            for key2 in dic[key].keys():
                print(f'{key2}: {dic[key][key2]}')
        else:
            print(f'{key}: {dic[key]}')


def put_answers(right_answers, wrong_answers, skipped_answers):
    """Populate the global question dictionary with answer data.
    
    Args:
        right_answers (list): List of correct answer texts.
        wrong_answers (list): List of incorrect answer texts.
        skipped_answers (list): List of skipped answer texts.
    """
    i=0
    for ans in right_answers:
        question['answer'][f'answer{i}'] = [ans, True]
        i+=1

    for ansNew in wrong_answers + skipped_answers:
        question['answer'][f'answer{i}'] = [ansNew, False]
        i+=1
    return


def jump_to_next_question():
    """Click the submit button to proceed to the next question."""
    auto.click(SUBMIT_ANSWER_X, SUBMIT_ANSWER_Y)
    return 


def random_answer():
    """Select a random answer option and submit it."""
    auto.click(SELECT_ANSWER_X, SELECT_ANSWER_Y)
    auto.press('tab')
    auto.press('space')
    time.sleep(1)
    auto.click(SUBMIT_ANSWER_X, SUBMIT_ANSWER_Y)
    return


def test_right_answers(question):
    """Determine the correct answer format based on question data.
    
    Args:
        question (dict): Question dictionary with answer data.
        
    Returns:
        str: Formatted string of correct answers ('a' or 'a, b').
    """
    if question['answer']['answer1'][1] == True:
        return 'a, b'
    return 'a'


def test_type(question):
    """Determine if question is single or multiple choice.
    
    Args:
        question (dict): Question dictionary with answer data.
        
    Returns:
        str: Question type ('single' or 'multiple').
    """
    if range(len(test_right_answers(question)) > 1):
        return 'multiple'
    return 'single'


def append_to_sheet(question, i):
    """Append question data to CSV file.
    
    Args:
        question (dict): Question dictionary containing title and answers.
        i (int): Question number/index.
    """
    new_line = [
        f'{i}',
        question['title'],
    ]

    for key in question['answer'].keys():
        if question['answer'][key] == []:
            break
        new_line.append(question['answer'][key][0])
    new_line.append(test_right_answers(question))
    new_line.append(test_type(question))

    values = new_line

    with open(file, 'a', newline='', encoding='utf=8') as file_csv:
        writer = csv.writer(file_csv)
        writer.writerow(values)


def end_test():
    """Complete current test and start a new practice test.
    
    Clicks through the sequence: End Test -> Continue -> Practice Mode -> Start Test.
    """
    auto.click(x=END_TEST_COORDS_X, y=END_TEST_COORDS_Y)
    time.sleep(3)
    auto.click(x=CONTINUE_COORDS_X, y=CONTINUE_COORDS_Y)
    time.sleep(3)
    auto.click(x=PRAC_MODE_COORDS_X, y=PRAC_MODE_COORDS_Y)
    time.sleep(3)
    auto.click(x=START_TEST_COORDS_X, y=START_TEST_COORDS_Y)
    time.sleep(3)
    return


def import_to_sheets():
    """Import CSV file to Google Sheets through automated UI interactions.
    
    Switches to sheets tab and performs the complete import workflow:
    File -> Import -> Upload -> Select File -> Import to new sheet.
    """
    auto.hotkey('ctrl', 'tab')
    auto.click(x=FILE_BUTTON_COORDS_X, y=FILE_BUTTON_COORDS_Y)
    auto.click(x=IMPORT_BUTTON_COORDS_X, y=IMPORT_BUTTON_COORDS_Y)
    time.sleep(2)
    auto.click(x=UPLOAD_COORDS_X, y=UPLOAD_COORDS_Y)
    auto.click(x=SEARCH_BUTTON_X, y=SEARCH_BUTTON_Y)
    time.sleep(2)
    auto.click(x=FILE_LOCATION_X, y=FILE_LOCATION_Y)
    time.sleep(1)
    auto.click(x=OPEN_BUTTON_X, y=OPEN_BUTTON_Y)
    time.sleep(5)
    auto.click(x=IMPORT_LOCAL_X, y=IMPORT_LOCAL_Y)
    auto.click(x=INSERT_NEW_SHEET_X, y=INSERT_NEW_SHEET_Y)
    auto.click(x=IMPORT_DATA_X, y=IMPORT_DATA_Y)
    return


start_time=time.time()

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
i = 66
j = 2
while j < 7:
    while i < 66*j:
        random_answer()
        question['title'] = get_question_title()
        right_answers = get_answers("copy(Array.from(document.querySelectorAll('.answer-result-pane--answer-correct--PLOEU .answer-result-pane--answer-body--cDGY6 .ud-heading-md.rt-scaffolding')).map(el => el.innerText))")
        wrong_answers = get_answers("copy(Array.from(document.querySelectorAll('.answer-result-pane--answer-incorrect--vFyOv .answer-result-pane--answer-body--cDGY6 .ud-heading-md.rt-scaffolding')).map(el => el.innerText))")
        skipped_answers = get_answers("copy(Array.from(document.querySelectorAll('.answer-result-pane--answer-skipped--1NDPn .answer-result-pane--answer-body--cDGY6 .ud-heading-md.rt-scaffolding')).map(el => el.innerText))")
        put_answers(right_answers, wrong_answers, skipped_answers)
        jump_to_next_question()
        print_question(question)
        append_to_sheet(question, i)
        i+=1
    end_test()
    j+=1


end_time = time.time()
elapsed_sec= end_time - start_time


print(f"Routine executed in: {elapsed_sec}s")