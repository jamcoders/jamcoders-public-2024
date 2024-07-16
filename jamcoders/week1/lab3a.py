# For answer checking without revealing the answer
def check_answers_with_num(answer, correct, num):
    if correct == answer:
        print(f"Your answer to Question {num} is correct!")
    else:
        print(f"Your answer to Question {num}: '{answer}' is wrong :( try again!")


def create_check_answer(correct, num):
    def check_fn(ans):
        check_answers_with_num(ans, correct, num)
    return check_fn

check_answer_3a = create_check_answer(3, '3a')
check_answer_3b = create_check_answer(3, '3b')
check_answer_3c = create_check_answer(3, '3c')
check_answer_3d = create_check_answer(1, '3d')
check_answer_4a = create_check_answer(9, '4a')
check_answer_4b = create_check_answer(3, '4b')
check_answer_6 = create_check_answer(25, '6')

check_6_1_100 = create_check_answer(103,'6.1 (100)')
check_6_1_5 = create_check_answer(8,'6.1 (5)')
check_6_1_420 = create_check_answer(422,'6.1 (420)')

check_answer_8_1a = create_check_answer('10 5', '8.1 (a)')
check_answer_8_1b = create_check_answer('0', '8.1 (b)')

