from main import random_food

def test_food_not_on_snake():
    snake = [(100, 100), (120, 100)]
    food = random_food(snake=snake)

    assert food["position"] not in snake
