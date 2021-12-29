def test_erc20_deployment(ohm):
    assert len(ohm.address) == 42


def test_authority_deployment(authority):
    assert len(authority.address) == 42


def test_treasury_deployment(treasury):
    assert len(treasury.address) == 42


def test_sohm_deployment(sohm):
    assert len(sohm.address) == 42


def test_gohm_deployment(gohm):
    assert len(gohm.address) == 42


def test_staking_deployment(staker):
    assert len(staker.address) == 42


def test_distributor_deployment(distributor):
    assert len(distributor.address) == 42
