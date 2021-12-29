import pytest
import brownie


def test_erc20_properties(OHM_token):
    assert OHM_token.name() == "Olympus"
    assert OHM_token.symbol() == "OHM"
    assert OHM_token.decimals() == 9


def test_non_vault_cannot_mint(accounts, OHM_token):
    deployer = accounts[0]
    bob = accounts[1]
    with brownie.reverts("UNAUTHORIZED"):
        OHM_token.mint(bob, 100, {"from": bob})


def test_vault_can_mint(accounts, OHM_token):
    deployer = accounts[0]
    bob = accounts[1]
    OHM_token.mint(bob, 20, {"from": deployer})
    assert OHM_token.balanceOf(bob) == 20


def test_mint_increases_total_supply(accounts, OHM_token):
    deployer = accounts[0]
    bob = accounts[1]
    OHM_token.mint(bob, 20, {"from": deployer})
    total_supply_before = OHM_token.totalSupply()
    OHM_token.burn(10, {"from": bob})
    assert OHM_token.totalSupply() + 10 == total_supply_before


def test_burn_reduces_total_supply(accounts, OHM_token):
    bob = accounts[1]
    total_supply_before = OHM_token.totalSupply()
    OHM_token.burn(10, {'from': bob})
    assert OHM_token.totalSupply() == total_supply_before - 10    


def test_burn_cannot_exceed_total_supply(accounts, OHM_token):
    bob = accounts[1]
    total_supply_before = OHM_token.totalSupply()
    with brownie.reverts("ERC20: burn amount exceeds balance"):
        OHM_token.burn(total_supply_before + 1, {'from': bob})


def test_burn_cannot_exceed_bobs_balance(accounts, OHM_token):
    bob = accounts[1]
    bob_balance = OHM_token.balanceOf(bob)
    with brownie.reverts("ERC20: burn amount exceeds balance"):
        OHM_token.burn(bob_balance + 1, {'from': bob})
