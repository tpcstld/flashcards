#!/usr/bin/python
"""
==== How it works ==============================================================

Each line starting with a '*' symbol is treated as the start of a new question.
Each line starting with a '#' symbol is treated as a comment.
Otherwise, the line is treated as part of the answer to the previous question.

If the "unique" option is enabled, no question will be repeated.
If the "colors" option is enabled, terminal colors will be used.
If the "jeopardy" proportion is given, a specified proportion of questions will
be given answer-first.

==== Caveats ===================================================================

Questions cannot be multilined.
No line in an answer can start with '*' or '#'.

==== Style guide ===============================================================

- Keep your questions short. Try to test general knowledge, avoid specific
  examples or application problems.

- All questions should end in '?'
    BAD:  List 3 organs in the human body.
    GOOD: What are 3 organs in the human body?

- When the question could be ambiguous, use with-respect-to (w.r.t).
    BAD:  What is the role of blood?
    GOOD: What is the role of blood w.r.t the immune system?

- Keep all lines in answers within an 80 character limit.

- Use numbering (1., 2., ...) when the question poses a "steps" question, or a
  "list" question.
    e.g. What are 3 organs in the human body?
         1. Heart
         2. Brain
         3. Liver
    e.g. What are the 3 steps for typing on a keyboard?
         1. Press the key.
         2. Watch the character appear.
         3. Release the key.

- End all sentences with more than 2 words with a punctuation.
    BAD:  This is an answer
    GOOD: This is an answer.
"""
import random
import sys
import argparse

class bcolors:
    HEADER = '\033[95m' # Only this really works.
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def gen_cards(data):
    flashcards = []
    question = ""
    answer = ""
    for line in data:
        # Comment
        if line[0].startswith("#"):
            continue

        # Question
        if line[0].startswith("*"):
            if question:
                flashcards.append((question, answer))
                question = ""
                answer = ""
            question = line[1:].strip()
        else:
            answer = answer + line

    if question:
        flashcards.append((question, answer))

    return flashcards

def add_color(text, color, args):
    if not args.colors:
        return text

    return color + text + bcolors.ENDC

def parse_args():
    parser = argparse.ArgumentParser(description="Flashcards")
    parser.add_argument("--no-unique", dest="unique", action="store_false",
            help="Repeat questions")
    parser.add_argument("--no-colors", dest="colors", action="store_false",
            help="Disable terminal colors")
    parser.add_argument("--jeopardy", type=str, default="0",
            help="Proportion of questions to be read answer-first.")

    parser.add_argument("file", type=str, help="Path to flashcards file")
    parser.set_defaults(unique=True, colors=True)
    return parser.parse_args()

def is_jeopardy(args):
    threshold = float(args.jeopardy)
    return random.random() <= threshold

def main():
    args = parse_args()

    file_name = args.file
    with open(file_name, "r") as data:
        cards = gen_cards(data)

    left = [x for x in xrange(0, len(cards))]
    random.shuffle(left);
    while left:
        if args.unique:
            choice = left.pop()
        else:
            choice = random.randrange(0, len(cards))

        if args.unique:
            questions_left = \
                "(" + str(len(cards) - len(left)) + "/" + str(len(cards)) + ")"
        else:
            questions_left = ""

        if is_jeopardy(args):
            question_text = cards[choice][1].strip()
            answer_text = cards[choice][0].strip()
        else:
            question_text = cards[choice][0].strip()
            answer_text = cards[choice][1].strip()

        print add_color("---------- " + questions_left, bcolors.FAIL, args)
        print question_text
        # Wait for user to press enter.
        raw_input()
        print add_color(answer_text, bcolors.HEADER, args)

if __name__ == '__main__':
    try:
        main();
    except KeyboardInterrupt:
        pass
