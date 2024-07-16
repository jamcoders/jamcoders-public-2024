def check_answers(answer, correct, num):
    if correct == answer:
        print(f"Your answer to Question {num} is correct!")
    else:
        print(f"Your answer to Question {num}: '{answer}' is wrong :( try again!")

def warmup_check1(answer, orr_counter):
    check_answers(answer, 14, "WWPD #1")
    if orr_counter == 0 and answer == 14:
        print("Congrats! You got it on your first try. Call Orr over to congratulate you :)")

def warmup_check2(answer):
    check_answers(answer, 0, "WWPD #2")

def warmup_check3(answer):
    check_answers(answer, [3, 2, 1, 0, 1, 2, 3], "WWPD #3")