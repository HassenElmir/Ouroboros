from main import make_obstacles

def test_obstacles_not_empty():
    obstacles = make_obstacles()

    assert len(obstacles) > 0
