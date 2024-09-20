
from main import  validate_name, validate_birth_date, get_day_of_week, get_patient_word



def test_validate_name():
    assert validate_name("Иван Иванов")
    assert not validate_name("12345")
    assert not validate_name("")
    assert not validate_name("Иван1212")
    assert not validate_name("Boris-Иван")

def test_validate_birth_date():
    assert validate_birth_date("01-01-2000")
    assert not validate_birth_date("32-01-2000")
    assert not validate_birth_date("01-01-3000")

def test_get_day_of_week():
    assert get_day_of_week("2023-10-05") == "Четверг"
    assert get_day_of_week("2023-10-06") == "Пятница"
    assert not get_day_of_week("2023-10-07") == "Понедельник"

def test_get_patient_word():
    assert get_patient_word(1) == "пациент"
    assert get_patient_word(2) == "пациента"
    assert get_patient_word(5) == "пациентов"
    assert get_patient_word(11) == "пациентов"
    assert get_patient_word(21) == "пациент"




