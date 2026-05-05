// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@chainlink/contracts/src/v0.8/shared/interfaces/AggregatorV3Interface.sol";

contract DeCertOracle {
    AggregatorV3Interface internal priceFeed;

    constructor() {
        // Feed ETH/USD na Sepolia
        priceFeed = AggregatorV3Interface(0x694AA1769357215DE4FAC081bf1f309aDC325306);
    }

    function getLatestPrice() public view returns (int) {
        ( , int price, , , ) = priceFeed.latestRoundData();
        return price; 
    }
}
