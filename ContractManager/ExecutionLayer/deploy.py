from solcx import compile_standard, install_solc
from web3 import Web3, contract
from web3.middleware import geth_poa_middleware
import json
from dotenv import load_dotenv


contractSources = dict()
solidityFiles=["ContractManager"]
solidityContracts=[["ContractManager"]]
for fileName in solidityFiles:
  with open("./contracts/{0}.sol".format(fileName), "r") as file:
      contractSources["{0}.sol".format(fileName)] = {"content": file.read()}

install_solc("0.8.7")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": contractSources,
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.7"
)

contractByteCodeAndABI = dict()
for i,fileName in enumerate(solidityFiles):
    for contractName in solidityContracts[i]:
        contractByteCodeAndABI[contractName] ={ "bytecode": compiled_sol["contracts"]["{0}.sol".format(fileName)][contractName]["evm"]["bytecode"]["object"],
                                              "abi": json.loads(compiled_sol["contracts"]["{0}.sol".format(fileName)][contractName]["metadata"])["output"]["abi"]
                                             }
load_dotenv()
#Added Polygon integrated webAddress details if chainId= 80002
webObject=Web3(Web3.HTTPProvider("https://sepolia.infura.io/v3/f8706c9015f047ee9a4e63486bb1643e"))
webObject.middleware_onion.inject(geth_poa_middleware,layer=0)

contractByteCodeAndABI["chain_id"] = 11155111
contractByteCodeAndABI["ContractOwnerAddress"] = "0x6404B135F5Fd54E11cb435c10075C6E6aEeB164C"
private_key = "4fc153ec7abb5b04b71d1eac1f97c2660ac74496ed318cc02caa728084c71b4f"



# Please add a file inside Dapp folder with the name ".env" and add "Contract_Owner_private_key = "Your Account corsponding private_key" " insde ".env" file



contractManager = webObject.eth.contract(abi=contractByteCodeAndABI["ContractManager"]["abi"],bytecode=contractByteCodeAndABI["ContractManager"]["bytecode"])

transaction = contractManager.constructor().build_transaction(
    {
        "chainId": contractByteCodeAndABI["chain_id"] ,
        #"gasPrice": webObject.eth.gas_price,
        "from":contractByteCodeAndABI["ContractOwnerAddress"],
        "nonce": webObject.eth.get_transaction_count(contractByteCodeAndABI["ContractOwnerAddress"])
    }
)
signed_txn= webObject.eth.account.sign_transaction(transaction, private_key)

# #send  signed transaction
tx_hash=webObject.eth.send_raw_transaction(signed_txn.rawTransaction)

# #waiting for transaction rcipt
tx_recept=webObject.eth.wait_for_transaction_receipt(tx_hash)
print("contractManager Contract is deployed.")
contractByteCodeAndABI["ContractManager"]["address"] = tx_recept.contractAddress

json_object = json.dumps(contractByteCodeAndABI, indent=4)

# Writing to sample.json
with open("./ExecutionLayer/contractConfig.json", "w") as outfile:
    outfile.write(json_object)
