import requests
import json

BASE_URL = 'http://127.0.0.1:5000'

# Utility function to send POST requests
def send_post_request(endpoint, data):
    url = f"{BASE_URL}{endpoint}"
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response

# Utility function to send GET requests
def send_get_request(endpoint, params=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers, params=params)
    return response

# Test adding a contract (positive scenario)
def test_add_contract():
    data = {
        'contract_address': '0x24dB6e3b3A156c97a88438664a27c5e00f16E7db',
        'description': 'Test3 Contract Description'
    }
    response = send_post_request('/add_contract', data)
    print(response.json())

# Test adding a contract with missing description (negative scenario)
def test_add_contract_missing_description():
    data = {
        'contract_address': '0x8d8bbc1118725845C978138EcD0A64ddeFe9E37B',
        'description': ''
    }
    response = send_post_request('/add_contract', data)
    print(response.json())

# Test updating a contract description (positive scenario)
def test_update_description():
    data = {
        'contract_address': '0x24dB6e3b3A156c97a88438664a27c5e00f16E7db',
        'new_description': 'Updated3 Contract Description'
    }
    response = send_post_request('/update_description', data)
    print(response.json())

# Test updating a contract description for a non-existent contract (negative scenario)
def test_update_description_non_existent():
    data = {
        'contract_address': '0x8d8bbc1118725845C978138EcD0A64ddeFe9E37B',
        'new_description': 'Updated3 Contract Description'
    }
    response = send_post_request('/update_description', data)
    print(response.json())

# Test removing a contract (positive scenario)
def test_remove_contract():
    data = {
        'contract_address': '0x24dB6e3b3A156c97a88438664a27c5e00f16E7db'
    }
    response = send_post_request('/remove_contract', data)
    print(response.json())

# Test removing a non-existent contract (negative scenario)
def test_remove_contract_non_existent():
    data = {
        'contract_address': '0x8d8bbc1118725845C978138EcD0A64ddeFe9E37B'
    }
    response = send_post_request('/remove_contract', data)
    print(response.json())

# Test getting a contract description (positive scenario)
def test_get_description():
    params = {
        'contract_address': '0x24dB6e3b3A156c97a88438664a27c5e00f16E7db'
    }
    response = send_get_request('/get_description', params)
    print(response.json())

# Test getting a contract description for a non-existent contract (negative scenario)
def test_get_description_non_existent():
    params = {
        'contract_address': '0x8d8bbc1118725845C978138EcD0A64ddeFe9E37B'
    }
    response = send_get_request('/get_description', params)
    print(response.json())

# Test getting all contracts (positive scenario)
def test_get_all_contracts():
    response = send_get_request('/get_all_contracts')
    print(response.json())

# Test adding a user role (positive scenario)
def test_add_user_role():
    data = {
        'user_address': '0x24dB6e3b3A156c97a88438664a27c5e00f16E7db',
        'authorize_level': 1
    }
    response = send_post_request('/add_user_role', data)
    print(response.json())

# Test adding a user role with invalid authorization level (negative scenario)
def test_add_user_role_invalid_level():
    data = {
        'user_address': '0x8d8bbc1118725845C978138EcD0A64ddeFe9E37B',
        'authorize_level': 5  # Invalid authorization level
    }
    response = send_post_request('/add_user_role', data)
    print(response.json())

# Running the tests
if __name__ == "__main__":
    test_add_contract()
    test_add_contract_missing_description()
    test_update_description()
    test_update_description_non_existent()
    test_remove_contract()
    test_remove_contract_non_existent()
    test_get_description()
    test_get_description_non_existent()
    test_get_all_contracts()
    test_add_user_role()
    test_add_user_role_invalid_level()
