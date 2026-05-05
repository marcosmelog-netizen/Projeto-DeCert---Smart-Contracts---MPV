import os
import json
from dotenv import load_dotenv
from web3 import Web3

load_dotenv(override=True)

# Configurações de ambiente
rpc_url = os.getenv('SEPOLIA_URL')
private_key = os.getenv('PRIVATE_KEY')
dao_address = os.getenv('DAO_ADDRESS')

web3 = Web3(Web3.HTTPProvider(rpc_url))
account = web3.eth.account.from_key(private_key)

# Carregamento do ABI (Certifique-se de que o nome do arquivo na pasta abis está correto)
try:
    with open('abis/DeCertDAO.json', 'r') as f:
        dao_abi = json.load(f)
except FileNotFoundError:
    print("❌ Erro: Arquivo abis/DeCertDAO.json não encontrado!")
    exit()

dao_contract = web3.eth.contract(address=dao_address, abi=dao_abi)

def realizar_votacao(proposta_id):
    print(f"🗳️ Iniciando processo de votação para a proposta #{proposta_id}...")
    
    try:
        # Verifica se você tem tokens para votar (requisito da linha 24 do seu Solidity)
        # Como você já fez o Stake, o contrato Governance checa o balanceOf no contrato do Token
        
        nonce = web3.eth.get_transaction_count(account.address)
        
        # Chama a função 'vote' do seu contrato DeCertGovernance
        txn = dao_contract.functions.vote(proposta_id).build_transaction({
            'from': account.address,
            'gas': 150000,
            'gasPrice': web3.eth.gas_price,
            'nonce': nonce,
            'chainId': 11155111
        })

        # Assina e envia
        signed_txn = web3.eth.account.sign_transaction(txn, private_key)
        txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        
        print(f"📡 Transação de voto enviada! Hash: {web3.to_hex(txn_hash)}")
        print("⏳ Aguardando confirmação na rede Sepolia...")
        
        receipt = web3.eth.wait_for_transaction_receipt(txn_hash)
        print(f"✨ SUCESSO! Voto computado no bloco: {receipt.blockNumber}")

    except Exception as e:
        print(f"❌ Falha ao votar: {e}")

if __name__ == "__main__":
    # IMPORTANTE: Você deve ter criado uma proposta no Remix antes (ID 0)
    realizar_votacao(0)
