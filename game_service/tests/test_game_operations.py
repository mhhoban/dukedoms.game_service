from hamcrest import (
    assert_that,
    equal_to
)

from game_service.controllers.game_operations import (
    player_accept_invite,
    player_decline_invite,
    verify_player_pending
)


def test_verify_player_pending_True():

    pending_players = ['testPlayer1', 'testPlayer2']
    submitted_player = 'testPlayer1'

    assert_that(
        verify_player_pending(
            pending_players=pending_players,
            submitted_player=submitted_player
        ),
        equal_to(True)
    )


def test_verify_player_pending_false():

    pending_players = ['testPlayer1', 'testPlayer2']
    submitted_player = 'pendingPlayer3'

    assert_that(
        verify_player_pending(
            pending_players=pending_players,
            submitted_player=submitted_player
        ),
        equal_to(False)
    )

def test_decline_invitation():

    pending_players = ['testPlayer1', 'testPlayer2']
    declined_player = 'testPlayer2'
    declined_players = []

    player_decline_invite(
        declined_player=declined_player,
        declined_players=declined_players,
        pending_players=pending_players
    )

    assert_that(declined_players, equal_to(['testPlayer2']))
    assert_that(pending_players, equal_to(['testPlayer1']))


def test_accept_invitation():

    pending_players = ['testPlayer1', 'testPlayer2']
    accepted_player = 'testPlayer2'
    accepted_players = []

    player_accept_invite(
        accepted_player=accepted_player,
        accepted_players=accepted_players,
        pending_players=pending_players
    )

    assert_that(accepted_players, equal_to(['testPlayer2']))
    assert_that(pending_players, equal_to(['testPlayer1']))
