from brownie import (
    accounts,
    OlympusERC20Token,
    OlympusTreasury,
    sOlympus,
    OlympusStaking,
    OlympusAuthority,
    gOHM,
    OlympusBondingCalculator,
    Distributor,
)

import scripts.constants as c


def main():
    # deploy authority
    deployer = accounts[0]
    authority = OlympusAuthority.deploy(
        deployer, deployer, deployer, deployer, {"from": deployer}
    )
    # print(authority.address)

    # deploy sOHM
    sohm = sOlympus.deploy({"from": deployer})
    # print(sohm.address)

    # deploy gOHM
    # first parameter we'll ignore as it is the migrator address and we need no migrations at all.
    gohm = gOHM.deploy(deployer, sohm.address, {"from": deployer})
    # print(gohm.address)

    # deploy OHM
    ohm = OlympusERC20Token.deploy(authority.address, {"from": deployer})

    # deploy Treasury
    treasury = OlympusTreasury.deploy(
        ohm.address, c.TREASURY_TIMELOCK, authority.address, {"from": deployer}
    )

    # deploy Bonding Calculator
    bondingCalculator = OlympusBondingCalculator.deploy(ohm.address, {"from": deployer})

    # deploy Staking
    staking = OlympusStaking.deploy(
        ohm.address,
        sohm.address,
        gohm.address,
        c.EPOCH_LENGTH_IN_BLOCKS,
        c.FIRST_EPOCH_NUMBER,
        c.FIRST_EPOCH_TIME,
        authority.address,
        {"from": deployer},
    )

    # deploy distributor
    distributor = Distributor.deploy(
        treasury.address,
        ohm.address,
        staking.address,
        authority.address,
        {"from": deployer},
    )

    # post deployment

    # Step 1: Set treasury as vault on authority
    print("Step 1: Set treasury as vault on authority")
    authority.pushVault(treasury.address, True)

    # Step 2: Set distributor as minter on treasury
    print("Step 2: Set distributor as minter on treasury")
    treasury.enable(8, distributor.address, c.ZERO_ADDRESS)

    # Step 3: Set distributor on staking
    print("Step 3: Set distributor on staking")
    staking.setDistributor(distributor.address)

    # Step 4: Initialize sOHM and set the index
    print("Step 4: Initialize sOHM and set the index")
    if sohm.gOHM() == c.ZERO_ADDRESS:
        sohm.setIndex(c.INITIAL_INDEX)
        sohm.setgOHM(gohm.address)
        sohm.initialize(staking.address, treasury.address)

    # Step 5: Set up distributor with bounty and recipient
    print("Step 5: Set up distributor with bounty and recipient")
    distributor.setBounty(c.BOUNTY_AMOUNT)
    distributor.addRecipient(staking.address, c.INITIAL_REWARD_RATE)
