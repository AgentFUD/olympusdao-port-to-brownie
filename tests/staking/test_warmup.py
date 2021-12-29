import brownie


def test_sets_the_number_of_epochs_of_warmup_are_required(staker):
    assert staker.warmupPeriod() == 0
    staker.setWarmupLength(2)
    assert staker.warmupPeriod() == 2


def test_set_warmup_emits_event(staker):
    tx = staker.setWarmupLength(2)
    assert "WarmupSet" in tx.events.keys()


def test_warmup_canot_be_set_by_non_governor(accounts, staker):
    malicious_account = accounts[1]
    with brownie.reverts():
        staker.setWarmupLength(2, {"from": malicious_account})
