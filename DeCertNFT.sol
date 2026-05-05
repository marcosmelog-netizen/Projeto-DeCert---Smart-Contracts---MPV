// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

interface IDeCertOracle {
    function getLatestPrice() external view returns (int);
}

contract DeCertNFT is ERC721URIStorage, Ownable, ReentrancyGuard {
    address public oracleAddress;
    uint256 public nextTokenId;

    constructor(address _oracle) ERC721("DeCert NFT", "DCNFT") Ownable(msg.sender) {
        oracleAddress = _oracle;
    }

    // Para a obtenção do certificado
    function certify(string memory _uri) public nonReentrant {
        int ethPrice = IDeCertOracle(oracleAddress).getLatestPrice();
        require(ethPrice > 0, "Erro no Oraculo");
        
        uint256 tokenId = nextTokenId;
        nextTokenId++;

        _safeMint(msg.sender, tokenId);
        _setTokenURI(tokenId, _uri); // Agora a linha 20 usa a variavel _uri!
    }
}
