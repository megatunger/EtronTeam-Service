def select_question(field):
    questions = {
        # "name": "Tên của bạn là gì?",
        "phone": "Số điện thoại của {} là gì nhỉ?",
        "address": "Địa chỉ nhà {} ở đâu?",
        # "gender": "Bạn là nam hay nữ?",
        "age": "Năm nay {} bao nhiêu tuổi?",
        "skills": "Những kỹ năng {} có là gì?",
        "ot": "{} có sẵn sàng làm việc sau giờ làm không?",
        "salary_expectation": "Mức lương mong muốn của {} là bao nhiêu?"
    }
    if field not in questions:
        return ""
    return questions[field]