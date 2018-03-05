import json
from hamcrest import assert_that, equal_to

def test_validate_new_game():
    from game_service.data_validation.data_validators import validate_new_game_request

    test_request = {
        "host_player":"test_player",
        "invited_players": "test_players"
    }
    assert_that(validate_new_game_request(test_request), equal_to(True))

    test_request = {
        "host_player":"test_player",
    }
    assert_that(validate_new_game_request(test_request), equal_to(False))

    test_request = {
        "invited_players":"test_player",
    }
    assert_that(validate_new_game_request(test_request), equal_to(False))
