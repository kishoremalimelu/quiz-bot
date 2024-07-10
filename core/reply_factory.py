
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    if not isinstance(answer,str):
        return False," answer must be a string"
    if current_question_id is None:
        return False,"current question ID is not set"
    if current_question_id>= len(PYTHON_QUESTION_LIST) or current_question_id<0:
        return False,"Ivalid question ID."
    if "answers" not in session:
        session["answer"]={}
    session["answer"][current_question_id]=answer
    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    next_question_id= current_question_id +1
    if next_quedtion_id>=len(PYTHON_QUESTION_LIST):
        return None,None
    next_question=PYTHON_QUEZTION_LIST[next_question_id]
    

    return next_question,next_question_id


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    answers = session.get("answer",{})
    score=sum(1 for q_id, ans in answers.items() if ans)
    return f"Final result:{score} out of {len(PYTHON_QUESTION_LIST)}"
