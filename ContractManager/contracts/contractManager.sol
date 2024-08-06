// SPDX-License-Identifier: MIT
pragma solidity 0.8.7;

contract ContractManager {

    //Adding Authorization level to add, edit and delete functions   
    enum AuthorizationLevel {BasicAuth,CanAdd,CanEdit,CanDelete }

    struct Authorizedusers{
        address useraddress;
        AuthorizationLevel authorizelevel;
    }

    // Storage for contract addresses and their descriptions
    mapping(address => string) private contractDescriptions;
    address[] private contractAddresses;

    mapping(address =>Authorizedusers)public authorizedusers;

    // Address of the contract owner
    address public owner;

    // Event declarations for logging actions
    event ContractAdded(address indexed contractAddress, string description);
    event ContractUpdated(address indexed contractAddress, string newDescription);
    event ContractRemoved(address indexed contractAddress);

    // Modifier to restrict access to only the owner 
    modifier onlyOwner() {
        require(msg.sender == owner, "Access denied: Only owner can perform this action");
        _;
    }

    // Modifier to restrict access to only the owner and Authorized user who can Add Contract addresses 
    modifier canAdd() {
        require(msg.sender == owner || authorizedusers[msg.sender].authorizelevel==AuthorizationLevel.CanAdd, "Access denied: Only Authorized user can perform this action");
        _;
    }

    // Modifier to restrict access to only the owner and Authorized user who can Update Contract description
    modifier canUpdate() {
        require(msg.sender == owner || authorizedusers[msg.sender].authorizelevel==AuthorizationLevel.CanEdit, "Access denied: Only Authorized user can perform this action");
        _;
    }

    // Modifier to restrict access to only the owner and Authorized user who can Delete
    modifier canDelete() {
        require(msg.sender == owner || authorizedusers[msg.sender].authorizelevel==AuthorizationLevel.CanDelete, "Access denied: Only Authorized user can perform this action");
        _;
    }

    constructor() {
        owner = msg.sender; // Set the contract creator as the owner
    }

    



    function adduserrole(address useraddress,AuthorizationLevel _authorizelevel) public onlyOwner{
             authorizedusers[useraddress].authorizelevel = _authorizelevel;

    }
    
    // Function to add a new contract address with a description
    function addContract(address _contractAddress, string memory _description) public canAdd {
        require(bytes(_description).length > 0, "Description cannot be empty");
        require(bytes(contractDescriptions[_contractAddress]).length == 0, "Contract address already exists");
        

        contractDescriptions[_contractAddress] = _description;
        contractAddresses.push(_contractAddress);

        emit ContractAdded(_contractAddress, _description);
    }

    // Function to update the description of an existing contract address
    function updateDescription(address _contractAddress, string memory _newDescription) public canUpdate {
        require(bytes(_newDescription).length > 0, "Description cannot be empty");
        require(bytes(contractDescriptions[_contractAddress]).length > 0, "Contract address does not exist");

        contractDescriptions[_contractAddress] = _newDescription;

        emit ContractUpdated(_contractAddress, _newDescription);
    }

    // Function to remove a contract address and its description
    function removeContract(address _contractAddress) public canDelete {
        require(bytes(contractDescriptions[_contractAddress]).length > 0, "Contract address does not exist");

        // Remove the contract address from the array
        for (uint i = 0; i < contractAddresses.length; i++) {
            if (contractAddresses[i] == _contractAddress) {
                contractAddresses[i] = contractAddresses[contractAddresses.length - 1];
                contractAddresses.pop();
                break;
            }
        }

        // Remove the description
        delete contractDescriptions[_contractAddress];

        emit ContractRemoved(_contractAddress);
    }

    // Function to get the description of a contract address
    function getDescription(address _contractAddress) public view returns (string memory) {
        return contractDescriptions[_contractAddress];
    }

    // Function to get all contract addresses
    function getAllContracts() public view returns (address[] memory) {
        return contractAddresses;
    }
}