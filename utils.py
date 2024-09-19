from datetime import datetime, timedelta


def validate_name(name):
    return name.replace(" ", "").isalpha()

def validate_birth_date(birth_date):
    try:
        for fmt in ('%d-%m-%Y', '%d %m %Y', '%d.%m.%Y'):
            try:
                date = datetime.strptime(birth_date, fmt)
                if date <= datetime.now() and (datetime.now() - date).days // 365 <= 100:
                    return True
            except ValueError:
                continue
        return False
    except ValueError:
        return False
    

def get_day_of_week(date):
    date = datetime.strptime(date, '%Y-%m-%d')
    return date.strftime('%A')


def get_patient_word(count):
    if 11 <= count % 100 <= 19:
        return "пациентов"
    elif count % 10 == 1:
        return "пациент"
    elif 2 <= count % 10 <= 4:
        return "пациента"
    else:
        return "пациентов"
