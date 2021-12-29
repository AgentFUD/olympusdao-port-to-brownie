import scripts.constants as c

def test_staking_contract_deployed(accounts, staker, ohm, sohm, gohm, authority):
    governor = accounts[0]
    assert len(staker.address) == 42
    assert staker.OHM() == ohm
    assert staker.gOHM() == gohm
    assert staker.sOHM() == sohm

    epoch = staker.epoch()
    assert epoch[0] == c.EPOCH_LENGTH
    assert epoch[1] == c.EPOCH_NUMBER
    assert epoch[2] == c.FUTURE_END_TIME
    assert epoch[3] == 0

    assert authority.governor() == governor