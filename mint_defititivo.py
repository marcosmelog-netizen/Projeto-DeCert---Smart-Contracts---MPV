import os
import json
import sys
from dotenv import load_dotenv
from web3 import Web3

# 1. Carregamento do Ambiente
load_dotenv(override=True)

def get_env_var(name):
    value = os.getenv(name, '').strip()
    if not value:
        print(f"❌ ERRO: A variável {name} está vazia no .env")
        sys.exit(1)
    return value

rpc_url = get_env_var('SEPOLIA_URL')
private_key = get_env_var('PRIVATE_KEY')
nft_address = get_env_var('NFT_ADDRESS')

# 2. Conexão com a Rede Sepolia
web3 = Web3(Web3.HTTPProvider(rpc_url))
if not web3.is_connected():
    print("❌ Falha crítica: Não foi possível conectar à rede Sepolia.")
    sys.exit(1)

print(f"✅ Conectado à Sepolia. Bloco: {web3.eth.block_number}")

# 3. Carregamento do ABI
abi_path = 'abis/DeCertNFT.json'
try:
    with open(abi_path, 'r') as f:
        contract_abi = json.load(f)
    print(f"✅ ABI carregado com sucesso de {abi_path}")
except Exception as e:
    print(f"❌ Erro ao ler o arquivo ABI: {e}")
    sys.exit(1)

# 4. Configuração do Contrato e Conta
account = web3.eth.account.from_key(private_key)
contract = web3.eth.contract(address=nft_address, abi=contract_abi)

def executar_mint(uri_metadata):
    print(f"\n🚀 Iniciando transação via função 'certify'...")
    try:
        # Pega o nonce atual da sua carteira
        nonce = web3.eth.get_transaction_count(account.address)
        
        # Constrói a transação chamando a função 'certify' do seu contrato
        # Note que passamos apenas a URI, conforme definido no seu Solidity
        txn = contract.functions.certify(uri_metadata).build_transaction({
            'from': account.address,
            'gas': 500000,
            'gasPrice': web3.eth.gas_price,
            'nonce': nonce,
            'chainId': 11155111
        })

        # Assina a transação com sua chave privada
        signed_txn = web3.eth.account.sign_transaction(txn, private_key)
        
        # Envia para a blockchain
        txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        
        print(f"📡 Transação enviada! Hash: {web3.to_hex(txn_hash)}")
        print("⏳ Aguardando confirmação (15-30 segundos)...")
        
        # Espera o recibo da mineração
        receipt = web3.eth.wait_for_transaction_receipt(txn_hash)
        print(f"✨ SUCESSO! NFT mintado no bloco: {receipt.blockNumber}")
        print(f"🔗 Veja no Etherscan: https://sepolia.etherscan.io/tx/{web3.to_hex(txn_hash)}")

    except Exception as e:
        print(f"❌ Falha durante o Mint: {e}")

if __name__ == "__main__":
    # COLOQUE AQUI O LINK DO SEU METADATA JSON NO PINATA/IPFS
    LINK_IPFS = "ipfs://SEU_CID_AQUI" 
    
    executar_mint(LINK_IPFS)
