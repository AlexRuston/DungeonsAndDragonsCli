from unittest.mock import patch, MagicMock
from Characters.utils import display, race_options, class_options, roll_ability_scores, create_character

def test_display(capfd):
    mock_character = MagicMock()
    mock_character.name = "Test Name"
    mock_character.race = "Elf"
    mock_character.char_class = "Wizard"
    mock_character.background = "Scholar"
    mock_character.alignment = "Chaotic Good"
    mock_character.ability_scores = {
        "Strength": 12,
        "Dexterity": 14,
        "Constitution": 10,
        "Intelligence": 18,
        "Wisdom": 16,
        "Charisma": 8,
    }

    display(mock_character)

    captured = capfd.readouterr()

    assert "Test Name" in captured.out
    assert "Elf" in captured.out
    assert "Wizard" in captured.out
    assert "Scholar" in captured.out
    assert "Chaotic Good" in captured.out
    assert "Strength: 12" in captured.out
    assert "Dexterity: 14" in captured.out
    assert "Constitution: 10" in captured.out
    assert "Intelligence: 18" in captured.out
    assert "Wisdom: 16" in captured.out
    assert "Charisma: 8" in captured.out