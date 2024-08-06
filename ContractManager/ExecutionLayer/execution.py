import json
from web3 import Web3
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


f = open("ExecutionLayer\contractConfig.json")
contractByteCodeAndABI = json.load(f)

# Initialize web3 instance 
web3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/f8706c9015f047ee9a4e63486bb1643e'))

# contract's ABI and address
contract = web3.eth.contract(address=contractByteCodeAndABI["ContractManager"]["address"], abi=contractByteCodeAndABI["ContractManager"]["abi"])

# account address and private key
account = '0x6404B135F5Fd54E11cb435c10075C6E6aEeB164C'
private_key = '4fc153ec7abb5b04b71d1eac1f97c2660ac74496ed318cc02caa728084c71b4f'


@app.route('/add_contract', methods=['POST'])
def add_contract():
    data = request.get_json()
    _contract_address = data['contract_address']
    _description = data['description']

    try:
        tx = contract.functions.addContract(_contract_address, _description)
        transaction = tx.build_transaction({
            'chainId': 11155111,  # Sepolia
            'gas': 8000000,
            'gasPrice': web3.to_wei('50', 'gwei'),
            'nonce': web3.eth.get_transaction_count(account),
        })
        
        signed_tx = web3.eth.account.sign_transaction(transaction, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        return jsonify({'status': 'success', 'transactionHash': tx_hash.hex()}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/update_description', methods=['POST'])
def update_description():
    data = request.get_json()
    _contract_address = data['contract_address']
    _new_description = data['new_description']

    try:
        tx = contract.functions.updateDescription(_contract_address, _new_description)
        nonce = web3.eth.get_transaction_count(account)
        
        transaction = tx.build_transaction({
            'chainId': 11155111,  # Sepolia
            'gas': 8000000,
            'gasPrice': web3.to_wei('50', 'gwei'),
            'nonce': nonce,
        })
        
        signed_tx = web3.eth.account.sign_transaction(transaction, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print(tx_hash)
        
        return jsonify({'status': 'success', 'transactionHash': tx_hash.hex()}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/remove_contract', methods=['POST'])
def remove_contract():
    data = request.get_json()
    _contract_address = data['contract_address']

    try:
        tx = contract.functions.removeContract(_contract_address)
        nonce = web3.eth.get_transaction_count(account)
        
        transaction = tx.build_transaction({
            'chainId': 11155111,  # Sepolia
            'gas': 8000000,
            'gasPrice': web3.to_wei('50', 'gwei'),
            'nonce': nonce,
        })
        
        signed_tx = web3.eth.account.sign_transaction(transaction, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        return jsonify({'status': 'success', 'transactionHash': tx_hash.hex()}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    

@app.route('/get_description', methods=['GET'])
def get_description():
    _contract_address = request.args.get('contract_address')

    try:
        description = contract.functions.getDescription(_contract_address).call()
        return jsonify({'status': 'success', 'description': description}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/get_all_contracts', methods=['GET'])
def get_all_contracts():

    try:
        addresses = contract.functions.getAllContracts().call()
        return jsonify({'status': 'success', 'addresses': addresses}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400
    

@app.route('/add_user_role', methods=['POST'])
def add_user_role():
    data = request.get_json()
    user_address = data['user_address']
    authorize_level = data['authorize_level']

    try:
        tx = contract.functions.adduserrole(user_address, authorize_level)
        nonce = web3.eth.get_transaction_count(account)
        
        transaction = tx.build_transaction({
            'chainId': 11155111,  # Sepolia
            'gas': 8000000,
            'gasPrice': web3.to_wei('50', 'gwei'),
            'nonce': nonce,
        })
        
        signed_tx = web3.eth.account.sign_transaction(transaction, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        
        return jsonify({'status': 'success', 'transactionHash': tx_hash.hex()}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
