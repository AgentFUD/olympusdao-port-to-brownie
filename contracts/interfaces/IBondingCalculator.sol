// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

interface IBondingCalculator {
    function markdown( address _LP ) external view returns ( uint );

    function valuation( address pair_, uint amount_ ) external view returns ( uint _value );
}