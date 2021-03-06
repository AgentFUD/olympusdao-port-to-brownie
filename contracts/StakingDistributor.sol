// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "@openzeppelin/contracts/utils/math/SafeMath.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/interfaces/IERC20.sol";

import "./interfaces/ITreasury.sol";
import "./interfaces/IDistributor.sol";
import "./types/OlympusAccessControlled.sol";

contract Distributor is IDistributor, OlympusAccessControlled {
    /* ========== DEPENDENCIES ========== */

    using SafeMath for uint256;
    using SafeERC20 for IERC20;

    /* ====== VARIABLES ====== */

    IERC20 private immutable ohm;
    ITreasury private immutable treasury;
    address private immutable staking;

    mapping(uint256 => Adjust) public adjustments;
    uint256 public override bounty;

    uint256 private immutable rateDenominator = 1_000_000;

    /* ====== STRUCTS ====== */

    struct Info {
        uint256 rate; // in ten-thousandths ( 5000 = 0.5% )
        address recipient;
    }
    Info[] public information;

    struct Adjust {
        bool add;
        uint256 rate;
        uint256 target;
    }

    /* ====== CONSTRUCTOR ====== */

    constructor(
        address _treasury,
        address _ohm,
        address _staking,
        address _authority
    ) OlympusAccessControlled(IOlympusAuthority(_authority)) {
        require(_treasury != address(0), "Zero address: Treasury");
        treasury = ITreasury(_treasury);
        require(_ohm != address(0), "Zero address: OHM");
        ohm = IERC20(_ohm);
        require(_staking != address(0), "Zero address: Staking");
        staking = _staking;
    }

    /* ====== PUBLIC FUNCTIONS ====== */

    /**
        @notice send epoch reward to staking contract
     */
    function distribute() external override {
        require(msg.sender == staking, "Only staking");
        // distribute rewards to each recipient
        for (uint256 i = 0; i < information.length; i++) {
            if (information[i].rate > 0) {
                treasury.mint(information[i].recipient, nextRewardAt(information[i].rate)); // mint and send tokens
                adjust(i); // check for adjustment
            }
        }
    }

    function retrieveBounty() external override returns (uint256) {
        require(msg.sender == staking, "Only staking");
        // If the distributor bounty is > 0, mint it for the staking contract.
        if (bounty > 0) {
            treasury.mint(address(staking), bounty);
        }

        return bounty;
    }

    /* ====== INTERNAL FUNCTIONS ====== */

    /**
        @notice increment reward rate for collector
     */
    function adjust(uint256 _index) internal {
        Adjust memory adjustment = adjustments[_index];
        if (adjustment.rate != 0) {
            if (adjustment.add) {
                // if rate should increase
                information[_index].rate = information[_index].rate.add(adjustment.rate); // raise rate
                if (information[_index].rate >= adjustment.target) {
                    // if target met
                    adjustments[_index].rate = 0; // turn off adjustment
                    information[_index].rate = adjustment.target; // set to target
                }
            } else {
                // if rate should decrease
                if (information[_index].rate > adjustment.rate) {
                    // protect from underflow
                    information[_index].rate = information[_index].rate.sub(adjustment.rate); // lower rate
                } else {
                    information[_index].rate = 0;
                }

                if (information[_index].rate <= adjustment.target) {
                    // if target met
                    adjustments[_index].rate = 0; // turn off adjustment
                    information[_index].rate = adjustment.target; // set to target
                }
            }
        }
    }

    /* ====== VIEW FUNCTIONS ====== */

    /**
        @notice view function for next reward at given rate
        @param _rate uint
        @return uint
     */
    function nextRewardAt(uint256 _rate) public view override returns (uint256) {
        return ohm.totalSupply().mul(_rate).div(rateDenominator);
    }

    /**
        @notice view function for next reward for specified address
        @param _recipient address
        @return uint
     */
    function nextRewardFor(address _recipient) public view override returns (uint256) {
        uint256 reward;
        for (uint256 i = 0; i < information.length; i++) {
            if (information[i].recipient == _recipient) {
                reward = reward.add(nextRewardAt(information[i].rate));
            }
        }
        return reward;
    }

    /* ====== POLICY FUNCTIONS ====== */

    /**
     * @notice set bounty to incentivize keepers
     * @param _bounty uint256
     */
    function setBounty(uint256 _bounty) external override onlyGovernor {
        require(_bounty <= 2e9, "Too much");
        bounty = _bounty;
    }

    /**
        @notice adds recipient for distributions
        @param _recipient address
        @param _rewardRate uint
     */
    function addRecipient(address _recipient, uint256 _rewardRate) external override onlyGovernor {
        require(_recipient != address(0), "Zero address: Recipient");
        require(_rewardRate <= rateDenominator, "Rate cannot exceed denominator");
        information.push(Info({recipient: _recipient, rate: _rewardRate}));
    }

    /**
        @notice removes recipient for distributions
        @param _index uint
     */
    function removeRecipient(uint256 _index) external override {
        require(
            msg.sender == authority.governor() || msg.sender == authority.guardian(),
            "Caller is not governor or guardian"
        );
        require(information[_index].recipient != address(0), "Recipient does not exist");
        information[_index].recipient = address(0);
        information[_index].rate = 0;
    }

    /**
        @notice set adjustment information for a collector's reward rate
        @param _index uint
        @param _add bool
        @param _rate uint
        @param _target uint
     */
    function setAdjustment(
        uint256 _index,
        bool _add,
        uint256 _rate,
        uint256 _target
    ) external override {
        require(
            msg.sender == authority.governor() || msg.sender == authority.guardian(),
            "Caller is not governor or guardian"
        );
        require(information[_index].recipient != address(0), "Recipient does not exist");

        if (msg.sender == authority.guardian()) {
            require(_rate <= information[_index].rate.mul(25).div(1000), "Limiter: cannot adjust by >2.5%");
        }

        if (!_add) {
            require(_rate <= information[_index].rate, "Cannot decrease rate by more than it already is");
        }

        adjustments[_index] = Adjust({add: _add, rate: _rate, target: _target});
    }
}
