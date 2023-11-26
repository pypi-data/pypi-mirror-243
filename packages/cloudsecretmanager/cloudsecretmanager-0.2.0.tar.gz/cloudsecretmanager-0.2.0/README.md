# Cloud Secret Manager

Cloud Secret Manager is a Python package providing a unified interface for managing secrets across multiple cloud providers. With concrete implementations for Azure Key Vault and Google Cloud Secret Manager, this package offers a consistent and simplified API for the creation, retrieval, and management of secrets, tailored for secure and efficient handling in cloud-based applications.

## Project Structure

The project is organized as follows:

```
.
├── README.md
├── cloudsecretmanager
│   ├── __init__.py
│   ├── azure.py         # Azure Key Vault implementation
│   ├── gcp.py           # Google Cloud Secret Manager implementation
│   └── secret_manager.py # Abstract base class for secret managers
├── poetry.lock
├── pyproject.toml
└── tests
    ├── __init__.py
    ├── test_az_mock.py          # Mock tests for Azure implementation
    └── test_az_real_connection.py # Real connection tests for Azure implementation
```



## Features

- **Unified API**: A single, standardized interface for interacting with different cloud secret management services.
- **Cloud Provider Support**: Concrete implementations for both Azure Key Vault and Google Cloud Secret Manager.
- **Secure Handling**: Designed to promote best practices in secret management for cloud applications.
- **Easy Integration**: Simplifies the process of integrating secret management into cloud-based Python applications.

## Installation

This package can be installed using pip:

```bash
pip install cloudsecretmanager
```

## Usage

To use the Cloud Secret Manager, first import the appropriate class for your cloud provider:

```python
from cloudsecretmanager.azure import AzureKeyVaultManager
from cloudsecretmanager.gcp import GCPSecretManager
```

### Azure Key Vault Example
```python
# Create an instance of AzureKeyVaultManager
azure_manager = AzureKeyVaultManager(vault_url="https://your-vault-url.vault.azure.net/")

# Create or update a secret
azure_manager.create(secret_id="your-secret-id", payload="your-secret-value")

# Retrieve a secret
secret_value = azure_manager.get(secret_id="your-secret-id")

```
### Google Cloud Secret Manager Example
```python
# Create an instance of GCPSecretManager
gcp_manager = GCPSecretManager(project_id="your-gcp-project-id")

# Create or update a secret
gcp_manager.create(secret_id="your-secret-id", payload="your-secret-value")

# Retrieve a secret
secret_value = gcp_manager.get(secret_id="your-secret-id")
```

## Testing

The package includes unit tests for both Azure and GCP implementations. These tests are designed to ensure the integrity and correctness of the package functionalities.

To run the tests, you'll need to have Python and the necessary dependencies installed. You can run the tests directly using the Python `unittest` module from the root directory of the project.

Follow these steps to execute the tests:

1. Navigate to the root directory of the project.

2. Run the tests using the following command:

```bash
python -m unittest discover -s tests
```

## Contributing
Contributions to the Cloud Secret Manager are welcome! Please refer to the contributing guidelines for more information.

## License
This project is licensed under the MIT License - see the LICENSE file for details.