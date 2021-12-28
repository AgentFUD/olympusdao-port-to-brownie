def test_erc20_deployment(accounts,olympus_erc20_token):
    assert len(olympus_erc20_token.address) == 42
