def test_erc20_deployment(olympus_erc20_token):
    assert len(olympus_erc20_token.address) == 42


def test_treasury_deployment(olympus_treasury):
    assert len(olympus_treasury.address) == 42


def test_sohm_deployment(sOlympus_token):
    assert len(sOlympus_token.address) == 42
