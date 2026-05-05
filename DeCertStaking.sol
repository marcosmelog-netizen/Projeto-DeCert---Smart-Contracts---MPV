// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "./DeCertToken.sol";

contract DeCertStaking is Ownable {
    DeCertToken public token;
    mapping(address => uint256) public stakes;

    constructor(address _token) Ownable(msg.sender) {
        token = DeCertToken(_token);
    }

    function stake(uint256 _amount) public {
        token.transferFrom(msg.sender, address(this), _amount);
        stakes[msg.sender] += _amount;
    }
}
