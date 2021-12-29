import brownie


def test_erc20_properties(ohm):
    assert ohm.name() == "Olympus"
    assert ohm.symbol() == "OHM"
    assert ohm.decimals() == 9


def test_non_vault_cannot_mint(accounts, ohm):
    deployer = accounts[0]
    bob = accounts[1]
    with brownie.reverts("UNAUTHORIZED"):
        ohm.mint(bob, 100, {"from": bob})


def test_vault_can_mint(accounts, ohm):
    deployer = accounts[0]
    bob = accounts[1]
    ohm.mint(bob, 20, {"from": deployer})
    assert ohm.balanceOf(bob) == 20


def test_mint_increases_total_supply(accounts, ohm):
    deployer = accounts[0]
    bob = accounts[1]
    ohm.mint(bob, 20, {"from": deployer})
    total_supply_before = ohm.totalSupply()
    ohm.burn(10, {"from": bob})
    assert ohm.totalSupply() + 10 == total_supply_before


def test_burn_reduces_total_supply(accounts, ohm):
    bob = accounts[1]
    total_supply_before = ohm.totalSupply()
    ohm.burn(10, {"from": bob})
    assert ohm.totalSupply() == total_supply_before - 10


def test_burn_cannot_exceed_total_supply(accounts, ohm):
    bob = accounts[1]
    total_supply_before = ohm.totalSupply()
    with brownie.reverts("ERC20: burn amount exceeds balance"):
        ohm.burn(total_supply_before + 1, {"from": bob})


def test_burn_cannot_exceed_bobs_balance(accounts, ohm):
    bob = accounts[1]
    bob_balance = ohm.balanceOf(bob)
    with brownie.reverts("ERC20: burn amount exceeds balance"):
        ohm.burn(bob_balance + 1, {"from": bob})
