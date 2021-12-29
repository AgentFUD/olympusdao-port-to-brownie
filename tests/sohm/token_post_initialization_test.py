def test_set_allowed_value_between_sender_and_spender(
    accounts, sohm, gohm, staker, treasury
):
    alice = accounts[1]
    bob = accounts[2]

    sohm.setIndex(1)
    sohm.setgOHM(gohm.address)
    sohm.initialize(staker.address, treasury.address)
    sohm.approve(bob, 10, {"from": alice})
    assert sohm.allowance(alice, bob) == 10


def test_allowance_emits_event(accounts, sohm):
    alice = accounts[1]
    bob = accounts[2]
    tx = sohm.approve(bob, 10, {"from": alice})
    assert "Approval" in tx.events.keys()


def test_increases_allowance(accounts, sohm):
    alice = accounts[1]
    bob = accounts[2]
    sohm.approve(bob, 10, {"from": alice})
    sohm.increaseAllowance(bob, 4, {"from": alice})
    assert sohm.allowance(alice, bob) == 14


def test_increase_allowance_emits_approval_event(accounts, sohm):
    alice = accounts[1]
    bob = accounts[2]
    tx = sohm.increaseAllowance(bob, 4, {"from": alice})
    assert "Approval" in tx.events.keys()


def test_decreases_allowance_between_sender_and_spender(accounts, sohm):
    alice = accounts[1]
    bob = accounts[2]
    sohm.approve(bob, 10, {"from": alice})
    sohm.decreaseAllowance(bob, 4, {"from": alice})
    assert sohm.allowance(alice, bob) == 6


def test_decreases_allowance_cannot_make_allowance_value_negative(accounts, sohm):
    alice = accounts[1]
    bob = accounts[2]
    sohm.approve(bob, 10, {"from": alice})
    sohm.decreaseAllowance(bob, 11, {"from": alice})
    assert sohm.allowance(alice, bob) == 0


def test_decrease_allowance_emits_approval_event(accounts, sohm):
    alice = accounts[1]
    bob = accounts[2]
    sohm.approve(bob, 10, {"from": alice})
    tx = sohm.decreaseAllowance(bob, 4, {"from": alice})
    assert "Approval" in tx.events.keys()
