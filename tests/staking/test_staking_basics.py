import brownie
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


def test_will_not_allow_zero_ohm_address(accounts, OlympusStaking, sohm, gohm):
    owner = accounts[0]
    with brownie.reverts():
        OlympusStaking.deploy(
            c.ZERO_ADDRESS,
            sohm.address,
            gohm.address,
            c.EPOCH_LENGTH,
            c.EPOCH_NUMBER,
            c.FUTURE_END_TIME,
            owner,
            {"from": owner},
        )


def test_will_not_allow_zero_gohm_address(accounts, OlympusStaking, ohm, sohm):
    owner = accounts[0]
    with brownie.reverts():
        OlympusStaking.deploy(
            ohm.address,
            sohm.address,
            c.ZERO_ADDRESS,
            c.EPOCH_LENGTH,
            c.EPOCH_NUMBER,
            c.FUTURE_END_TIME,
            owner,
            {"from": owner},
        )


def test_we_can_set_distributor(staker, distributor):
    staker.setDistributor(distributor.address)
    assert staker.distributor() == distributor.address


def test_set_distributor_emits_event(staker, distributor):
    tx = staker.setDistributor(distributor.address)
    assert "DistributorSet" in tx.events.keys()


def test_set_distributor_can_be_done_by_governor_only(accounts, staker, distributor):
    malicious_account = accounts[1]
    with brownie.reverts():
        staker.setDistributor(distributor.address, {"from": malicious_account})
