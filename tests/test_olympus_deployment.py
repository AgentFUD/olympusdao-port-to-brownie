def test_erc20_deployment(OHM_token):
    assert len(OHM_token.address) == 42


def test_authority_deployment(authority_contract):
    assert len(authority_contract.address) == 42


def test_treasury_deployment(olympus_treasury):
    assert len(olympus_treasury.address) == 42


def test_sohm_deployment(sOHM_token):
    assert len(sOHM_token.address) == 42


def test_gohm_deployment(gOHM_token):
    assert len(gOHM_token.address) == 42


def test_staking_deployment(olympus_staking_contract):
    assert len(olympus_staking_contract.address) == 42


def test_distributor_deployment(distributor_contract):
    assert len(distributor_contract.address) == 42
