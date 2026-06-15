# --- chain of responsibility pattern: password recovery ---

from database import find_user_data_by_email, reset_password


class SecurityQuestionHandler:
    def __init__(self, correct_answer):
        self.correct_answer = correct_answer.lower().strip()
        self.next_handler = None
    
    def set_next(self, handler):
        self.next_handler = handler
        return handler
        
    def check(self, answer, remaining_answers):
        if answer.lower().strip() != self.correct_answer:
            return False

        if self.next_handler is not None:
            if len(remaining_answers) == 0:
                return False

            return self.next_handler.check(
                remaining_answers[0],
                remaining_answers[1:]
            )

        return True


def build_recovery_chain(user_data):
    q1_handler = SecurityQuestionHandler(user_data[7])
    q2_handler = SecurityQuestionHandler(user_data[9])
    q3_handler = SecurityQuestionHandler(user_data[11])

    q1_handler.set_next(q2_handler).set_next(q3_handler)

    return q1_handler


def recover_password(email, answer1, answer2, answer3, new_password):
    email = email.strip().lower()
    user_data = find_user_data_by_email(email)

    if user_data is None:
        return False, "Email not found"

    recovery_chain = build_recovery_chain(user_data)

    if recovery_chain.check(answer1, [answer2, answer3]):
        reset_password(email, new_password)
        return True, "Password reset successful"
    else:
        return False, "Incorrect answers to security questions"