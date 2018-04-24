from game_service.controllers.game_operations import (
    verify_player_pending
)

pending_players = ['testPlayer1', 'testPlayer2']

def test_verify_player_pending_True():

    submitted_player = 'pendingPlayer1'

    assert_that(
        verify_player_pending(
            pending_players=pending_players,
            submitted_player=submitted_player
        ),
        equal_to(True)
    )


def test_verify_player_pending_false():

    submitted_player = 'pendingPlayer3'

    assert_that(
        verify_player_pending(
            pending_players=pending_players,
            submitted_player=submitted_player
        ),
        equal_to(False)
    )

def test_decline_invitation():

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

    accepted_player = 'testPlayer2'
    accepted_players = []

    player_accept_invite(
        accepted_player=declined_player,
        accepted_players=declined_players,
        pending_players=pending_players
    )

    assert_that(accepted_players, equal_to(['testPlayer2']))
    assert_that(pending_players, equal_to(['testPlayer1']))
