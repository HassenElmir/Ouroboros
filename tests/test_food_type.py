from main import random_food

def test_food_type_valid():
    food = random_food()

    assert food["type"] in ["normal", "golden", "poison"]
