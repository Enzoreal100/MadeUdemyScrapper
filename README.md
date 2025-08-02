# Udemy Test Scraper

An automated Python script that extracts questions and answers from Udemy practice tests and exports them to CSV format.

## Features

- Automated test navigation and question extraction
- Captures question titles, answer options, and correctness
- Exports data to CSV file (`questions.csv`)
- Optional Google Sheets import functionality
- Handles multiple test cycles automatically

## Requirements

- Python 3.x
- Required packages:
  ```
  pyautogui
  pyperclip
  python-dotenv
  ```

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install pyautogui pyperclip python-dotenv
   ```
3. Create a `.env` file if needed for environment variables

## Setup

⚠️ **Important**: This script uses hardcoded screen coordinates that are specific to your display setup. You'll need to adjust the coordinate constants at the top of `scrapper.py` to match your screen resolution and browser layout.

### Coordinate Configuration

Update these coordinates in the script based on your screen:
- `CONSOLE_COORDS_X/Y` - Browser developer console location
- `SELECT_ANSWER_X/Y` - Answer selection area
- `SUBMIT_ANSWER_X/Y` - Submit button location
- Other UI element coordinates as needed

## Usage

1. Open Udemy practice test in your browser
2. Open browser developer console
3. Position windows as expected by the coordinate settings
4. Run the script:
   ```bash
   python scrapper.py
   ```

## How It Works

1. **Question Extraction**: Uses browser console to execute JavaScript and extract question text
2. **Answer Collection**: Captures correct, incorrect, and skipped answers using DOM selectors
3. **Data Processing**: Organizes answers with correctness flags
4. **CSV Export**: Appends each question's data to `questions.csv`
5. **Test Navigation**: Automatically cycles through multiple test sessions

## Output Format

The CSV file contains:
- Question number
- Question title
- Answer options
- Correct answers (formatted as 'a' or 'a, b')
- Question type (single/multiple choice)

## Configuration

- Modify the loop variables `i` and `j` to control how many questions to process
- Adjust `auto.PAUSE` to change automation speed
- Update file path in `file` variable if needed

## Limitations

- Screen coordinate dependent - requires manual calibration
- Browser and OS specific
- Requires stable internet connection
- May break if Udemy updates their UI

## Troubleshooting

- **Coordinate Issues**: Use a screen coordinate tool to find exact pixel positions
- **Timing Problems**: Increase sleep delays if actions happen too fast
- **Browser Console**: Ensure developer tools are open and console is accessible

## Project Structure

### Core Files

#### `scrapper.py`
The main automation script that performs the Udemy test scraping. Contains 11 functions:

- `get_question_title()` - Extracts question text using browser console
- `get_answers(type)` - Executes JavaScript to get answer options
- `print_question(dic)` - Displays question data to console
- `put_answers(right_answers, wrong_answers, skipped_answers)` - Populates question dictionary
- `jump_to_next_question()` - Clicks submit button
- `random_answer()` - Selects and submits random answer
- `test_right_answers(question)` - Formats correct answers
- `test_type(question)` - Determines single/multiple choice
- `append_to_sheet(question, i)` - Writes data to CSV
- `end_test()` - Completes test and starts new one
- `import_to_sheets()` - Imports CSV to Google Sheets

#### `calibrate.py`
Utility script for finding screen coordinates:
```python
import time
import pyautogui as auto

time.sleep(3)
pos = auto.position()
print(pos)
```
Run this script and move your mouse to UI elements to get their coordinates for the main script.

### Configuration Files

#### `requirements.txt`
Project dependencies:
```
pyautogui
pyperclip
python-dotenv
```

### Output Files

#### `questions.csv`
Generated CSV file containing extracted question data with columns:
- Question number
- Question title
- Answer options (multiple columns)
- Correct answers
- Question type

## Disclaimer

This tool is for educational purposes. Ensure compliance with Udemy's terms of service and applicable laws when using automated scraping tools.