import secrets
import os
from typing import Tuple

class PasswordPolicyManager:
    def __init__(self, dictionary_path: str, blacklist_path: str):
        # Fail-Fast: program musi wiedzieć, że brakuje plików już na etapie uruchamiania
        if not os.path.exists(dictionary_path):
            raise FileNotFoundError(f"Błąd krytyczny bezpieczeństwa: Brak pliku słownika pod ścieżką {dictionary_path}")
        if not os.path.exists(blacklist_path):
            raise FileNotFoundError(f"Błąd krytyczny bezpieczeństwa: Brak pliku czarnej listy pod ścieżką {blacklist_path}")

        # Wczytujemy pliki od razu przy inicjalizacji menedżera
        self.word_list = self._load_lines(dictionary_path)
        
        # Czarną listę rzutujemy na strukturę typu 'set' (zbiór).
        # To inżynieryjny wymóg dla wydajności: wyszukiwanie w secie ma złożoność O(1),
        # podczas gdy w liście miałoby O(N). Szukanie w 100 tysiącach haseł będzie natychmiastowe.
        self.blacklist = set(self._load_lines(blacklist_path))

        if not self.word_list:
            raise ValueError("Plik słownika jest pusty!")
        if not self.blacklist:
            raise ValueError("Plik czarnej listy jest pusty!")

    def _load_lines(self, path: str) -> list[str]:
        """Pobiera i formatuje linie z pliku tekstowego."""
        with open(path, 'r', encoding='utf-8') as f:
            return [line.strip().lower() for line in f if line.strip()]

    def generate_diceware_password(self, num_words: int = 5) -> str:
        """Generuje bezpieczne hasło składające się z losowych słów (CSPRNG)."""
        selected_words = [secrets.choice(self.word_list).capitalize() for _ in range(num_words)]
        return "".join(selected_words)

    def validate_password(self, password: str) -> Tuple[bool, str]:
        """
        Waliduje hasło zgodnie z rekomendacjami CERT Polska.
        """
        if len(password) < 14:
            return False, "Hasło jest zbyt krótkie. Wymagane minimum to 14 znaków."
            
        if password.lower() in self.blacklist:
            return False, "Hasło znajduje się na liście powszechnie znanych wycieków. Użyj innego."
            
        if len(password) > 64:
            return False, "Hasło jest zbyt długie (maksimum 64 znaki)."

        return True, "Hasło spełnia rekomendacje bezpieczeństwa."