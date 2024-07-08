# For answer checking without revealing the answer
from jamcoders.base_utils import *

def answer_true(ans,num):
    answer = True
    check_answers_with_num(ans, answer,num)

def answer_false(ans,num):
    answer = False
    check_answers_with_num(ans, answer, num)

# Option 1: Trying it for now
def check_answer1(ans): answer_false(ans,1)
def check_answer2(ans): answer_false(ans,2)
def check_answer3(ans): answer_true(ans,3)
def check_answer4(ans): answer_true(ans,4)
def check_answer5(ans): answer_true(ans,5)
def check_answer6(ans): answer_false(ans,6)
def check_answer7(ans): answer_true(ans,7)
def check_answer8(ans): answer_true(ans,8)

def check_answer_2_1(ans): check_answers_with_num(ans, "coder", "2.1")
def check_answer_2_2(ans): check_answers_with_num(ans, "starfruit", "2.2")
def check_answer_2_3(ans): check_answers_with_num(ans, ['orange', 'banana', 'pear'], "2.3")

# Option 2
def check_answer_0_2(ans):
    answers = [False, False, True, True, True, False, True,True]
    for i in range(len(answers)):
        check_answers_with_num(ans[i],answers[i], i+1)

# Trying this
def check_answer_3_4(ans):
    answers = [False,True,False,False,True,True,True]
    for i in range(len(answers)):
        check_answers_with_num(ans[i],answers[i], i+1)

