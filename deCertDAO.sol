// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "./DeCertToken.sol";

contract DeCertGovernance is Ownable {
    DeCertToken public token;
    struct Proposal {
        string description;
        uint256 voteCount;
        bool executed;
    }
    Proposal[] public proposals;

    constructor(address _token) Ownable(msg.sender) {
        token = DeCertToken(_token);
    }

    function createProposal(string memory _desc) public onlyOwner {
        proposals.push(Proposal(_desc, 0, false));
    }

    function vote(uint256 _propId) public {
        require(token.balanceOf(msg.sender) > 0, "Requer tokens para votar");
        proposals[_propId].voteCount += token.balanceOf(msg.sender);
    }
}
