from main import riddles

def test_riddles_have_answers():
    for r in riddles:
        assert "answer" in r
        assert isinstance(r["answer"], str)
