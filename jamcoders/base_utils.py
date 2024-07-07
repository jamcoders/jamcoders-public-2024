import base64

class NotebookTracking:
    tracker = None

    @classmethod
    def is_active(cls):
        return cls.tracker != None
    
    @classmethod
    def set_activation(cls, is_active):
        if is_active:
            # Importing notebook_tracker_client triggers a "!pip install", and imports google.colab,
            #   both of which can fail if executed in the wrong environment (e.g., not not colab).
            #   Therefore, we perform this import only if and when notebook tracking is enabled.  
            from jamcoders.notebook_tracking_client import NotebookTracker
            cls.tracker = NotebookTracker()
            cls.tracker.init()
        else:
            cls.tracker = None

# Turn this line on when tracking is intended
NotebookTracking.set_activation(True)

# For comparison of answers
def assert_equal(want, got):

    assert_passed = (want == got or (type(want) == float and type(got) == float and abs(want - got) < 0.001))

    # if NotebookTracking.is_active():
    #     NotebookTracking.tracker.send_assertion_event(assert_passed)

    if assert_passed:
        print("Test case passed.")
    else:
        print()
        print("--------- Test case failed. ---------")
        print(f"Want: {repr(want)} (type: {type(want).__name__})")
        print(f"Got:  {repr(got)} (type: {type(got).__name__})")
        print("-------------------------------------")
        print()
    return assert_passed

def assert_equal_with_num(want, got, num):

    assert_passed = (want == got or (type(want) == float and type(got) == float and abs(want - got) < 0.001))

    if NotebookTracking.is_active():
        NotebookTracking.tracker.send_assertion_event_with_num(assert_passed, num)

    if assert_passed:
        print("Test case passed.")
    else:
        print()
        print("--------- Test case failed. ---------")
        print(f"Want: {repr(want)} (type: {type(want).__name__})")
        print(f"Got:  {repr(got)} (type: {type(got).__name__})")
        print("-------------------------------------")
        print()

    return assert_passed




# Encodes ASCII string to base64
def encode_base64(str):
    message = str
    message_bytes = message.encode("ascii")
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode("ascii")
    return base64_message


# Decodes base64 to ASCII string
def decode_base64(b64):
    base64_message = b64
    base64_bytes = base64_message.encode("ascii")
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode("ascii")
    return message


DEBUGGABLE_ARGS = "_debuggable_args"
DEBUGGABLE_KWARGS = "_debuggable_kwargs"

def debuggable(f):
    @functools.wraps(f)
    def g(*args, **kwargs):
        try:
            args_copy = copy.deepcopy(args)
            kwargs_copy = copy.deepcopy(kwargs)
        except Exception:
            args_copy = None
            kwargs_copy = None
        result = f(*args, **kwargs)
        setattr(g, DEBUGGABLE_ARGS, args_copy)
        setattr(g, DEBUGGABLE_KWARGS, kwargs_copy)
        return result
    return g

####################################################################################################
# Check answer
####################################################################################################

# For answer checking without revealing the answer

def check_answers_with_num(answer, correct, num):
    check_passed = (correct == answer)

    if NotebookTracking.is_active():
        NotebookTracking.tracker.send_assertion_event_with_num(check_passed, num)
    
    if check_passed:
        print(f"Your answer to Question {num} is correct!")
    else:
        print(f"Your answer to Question {num}: '{answer}' is wrong :( try again!")

def check_answers_multi(answer, correct):
    check_passed = (correct == answer)

    if NotebookTracking.is_active():
        NotebookTracking.tracker.send_assertion_event(check_passed)
    
    if check_passed:
        print(f"All your answers are correct!")
    else:
        print(f"At least one of your answers is wrong :( try again!")

def create_check_answer(correct, num):
    def check_fn(ans):
        check_answers_with_num(ans, correct, num)
    return check_fn

def create_check_answer_multi(correct):
    def check_fn(ans):
        check_answers_multi(ans, correct)
    return check_fn

