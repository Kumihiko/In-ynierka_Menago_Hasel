import pytest
import os
from src.core.password_policy import PasswordPolicyManager

@pytest.fixture
def dummy_files(tmp_path):
    #tworzymy falszywe pliki na czas testu
    dict_file = tmp_path / "test_dict.txt"
    dict_file.write_text("jeden\ndwa\ntrzy\ncztery\npiec\n", encoding="utf-8")
    
    black_file = tmp_path / "test_blacklist.txt"
    black_file.write_text("qwerty\nhaslo123\nadmin1\nbardzodlugiehaslo\n", encoding="utf-8")
    
    return str(dict_file), str(black_file)


def test_init_raises_error_on_missing_files():
    #rzuca błąd jesli pliki nie istnieja
    with pytest.raises(FileNotFoundError) as excinfo:
        PasswordPolicyManager("nieistniejacy_slownik.txt", "nieistniejaca_lista.txt")
    assert "Błąd krytyczny bezpieczeństwa" in str(excinfo.value)

def test_init_loads_data_correctly(dummy_files):
    #sprawdza czy dane sie poprawnie ładują
    dict_path, black_path = dummy_files
    manager = PasswordPolicyManager(dict_path, black_path)
    
    assert len(manager.word_list) == 5
    assert "jeden" in manager.word_list
    assert isinstance(manager.blacklist, set)
    assert "qwerty" in manager.blacklist


def test_generate_diceware_password(dummy_files):
    #generator ma zwracac polaczony string
    dict_path, black_path = dummy_files
    manager = PasswordPolicyManager(dict_path, black_path)
    
    password = manager.generate_diceware_password(num_words=4)
    assert isinstance(password, str)
    assert len(password) > 0
    assert len(password) >= 12


def test_validate_password_too_short(dummy_files):
    #odrzucanie zbyt krótkich haseł
    dict_path, black_path = dummy_files
    manager = PasswordPolicyManager(dict_path, black_path)
    
    is_valid, msg = manager.validate_password("Krotkie123!")
    
    assert is_valid is False
    assert "zbyt krótkie" in msg 

def test_validate_password_in_blacklist(dummy_files):
    #odrzucanie hasel z czarnej listy
    dict_path, black_path = dummy_files
    manager = PasswordPolicyManager(dict_path, black_path)
    
    is_valid, msg = manager.validate_password("BardzoDlugieHaslo")
    assert is_valid is False
    assert "wycieków" in msg

def test_validate_password_success(dummy_files):
    #poprawna walidacja dobrego hasla
    dict_path, black_path = dummy_files
    manager = PasswordPolicyManager(dict_path, black_path)
    
    is_valid, msg = manager.validate_password("ToJestBardzoDobreHasloKtregoNieMaWSlowniku123!")
    assert is_valid is True
    assert "rekomendacje" in msg 