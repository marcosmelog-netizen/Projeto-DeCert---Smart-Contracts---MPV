import os
import json
import sys
from dotenv import load_dotenv
from web3 import Web3

load_dotenv(override=True)

# Configurações iniciais (mesma lógica do seu mint)
rpc_url = os.getenv('SEPOLIA_URL')
private_key = os.getenv('PRIVATE_KEY')
token_address = os.getenv('TOKEN_ADDRESS')
staking_address = os.getenv('STAKING_ADDRESS')

web3 = Web3(Web3.HTTPProvider(rpc_url))
account = web3.eth.account.from_key(private_key)

# Carregamento dos ABIs
with open('abis/DeCertToken.json', 'r') as f: token_abi = json.load(f)
with open('abis/DeCertStaking.json', 'r') as f: staking_abi = json.load(f)

token_contract = web3.eth.contract(address=token_address, abi=token_abi)
staking_contract = web3.eth.contract(address=staking_address, abi=staking_abi)

def realizar_stake(quantidade_tokens):
    # Quantidade convertida para Wei (18 casas decimais do padrão ERC20)
    valor_wei = web3.to_wei(quantidade_tokens, 'ether')
    
    print(f"⚙️ Passo 1: Autorizando o contrato de Staking a gastar {quantidade_tokens} tokens...")
    # Chama 'approve' no contrato do TOKEN
    nonce = web3.eth.get_transaction_count(account.address)
    tx_approve = token_contract.functions.approve(staking_address, valor_wei).build_transaction({
        'from': account.address, 'nonce': nonce, 'gas': 100000, 'gasPrice': web3.eth.gas_price, 'chainId': 11155111
    })
    
    signed_approve = web3.eth.account.sign_transaction(tx_approve, private_key)
    hash_approve = web3.eth.send_raw_transaction(signed_approve.raw_transaction)
    web3.eth.wait_for_transaction_receipt(hash_approve)
    print("✅ Autorização confirmada!")

    print(f"🚀 Passo 2: Realizando o Stake no contrato...")
    # Chama 'stake' no contrato de STAKING
    nonce = web3.eth.get_transaction_count(account.address)
    tx_stake = staking_contract.functions.stake(valor_wei).build_transaction({
        'from': account.address, 'nonce': nonce, 'gas': 150000, 'gasPrice': web3.eth.gas_price, 'chainId': 11155111
    })
    
    signed_stake = web3.eth.account.sign_transaction(tx_stake, private_key)
    hash_stake = web3.eth.send_raw_transaction(signed_stake.raw_transaction)
    
    print(f"⏳ Aguardando confirmação do Stake...")
    receipt = web3.eth.wait_for_transaction_receipt(hash_stake)
    print(f"✨ SUCESSO! Stake realizado no bloco: {receipt.blockNumber}")

if __name__ == "__main__":
    realizar_stake(10) # Altere aqui a quantidade de tokens que deseja travar
