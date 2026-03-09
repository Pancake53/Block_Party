


def test_game_init():
    from game import Game
    game = Game()
    assert game.window is not None
    assert game.clock is not None