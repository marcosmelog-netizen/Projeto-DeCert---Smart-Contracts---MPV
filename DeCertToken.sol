// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract DeCertToken is ERC20, Ownable {
    constructor() ERC20("DeCert Token", "DCRT") Ownable(msg.sender) {
        _mint(msg.sender, 1000000 * 10 ** decimals());
    }
}
