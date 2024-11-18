# My Currency API

Currency API based on [CurrencyBeacon](https://currencybeacon.com/api-documentation)

Based on [DRF](https://www.django-rest-framework.org/topics/documenting-your-api/) framework.

# Setup dev environment

Requirements:

- Python 3.11

Clone git repo then install python environment with command.

Enable virtual env
```bash
python -m venv env

>> env\Scripts\activate
>> pip install -r requirements.txt
```
Run development server with `python manage.py runserver` command then open http://localhost:8000 in your browser.

> Note: in this mode, Django database is stored in SQLite file `db.sqlite3`

Technical settings are defined through environment variables (see below). Create a `.env` file in root folder to customize these settings. Update `env.text` with `.env`
Example:

```sh
API_KEY=""
API_URL="https://api.currencybeacon.com/v1"
```

## Pre-commit hook

[Pre-commit](https://pre-commit.com/) is used for auto formatting python files. Its configuration is in `.pre-commit-config.yaml` file.

Run `pre-commit run -a` command to run these scripts.

To install them as git pre-commit hook, run `pre-commit install` command (once). After that, the scripts are run automatically on modified files at each git commit.

## Code linting

Several tools are used to help developers finding errors and ensure good code quality:

- **pylint**: static analysis of python code. Usage: https://pylint.readthedocs.io/en/stable/user_guide/usage/run.html

```
pylint <DIR OR FILE>
```

# Configuration

## Technical configuration

Technical configuration is loaded at startup by reading these environment variables (all of them are optional):

- **Currency Providers**: Integration with multiple providers (e.g., CurrencyBeacon, Mock).
- **REST API**: Exposes endpoints for:
  - Fetching exchange rates.
  - Converting between currencies.
  - Managing available currencies.
- **Back Office**:
  - Currency converter.
  - Admin tools for managing currencies and providers.
- **Adapter Design Pattern**: Flexible integration with multiple providers for scalability.
- **Asynchronous Data Loading**: Efficiently loads historical data for analysis.
- **Supported Currencies**: Currently supports EUR, CHF, USD, and GBP.


## Usage

### API Endpoints
#### Examples
- **Get Exchange Rates**:
`GET /api/exchange-rate/?source_currency=USD&exchanged_currency=EUR&valuation_date=2024-11-16`

- **Currency Rates**:
  `GET api/currency-rates/?source_currency=USD&date_from=2023-01-01&date_to=2023-01-10`
- **Convert Rates**:
  `/api/convert/?api/convert/?source_currency=USD&amount=10&exchanged_currency=EUR`
- **Historical data**
  `GET api/historical/?base=USD&date=2023-01-01&symbols=EUR,GBP,JPY`


- **List and Create Currencies**
  `GET /api/currencies/`
   Description: Retrieve all currencies.
- `POST /api/currencies/`
    Description: Create a new currency.
    Request Body:
     ```json
      {
        "name": "Swiss Franc",
        "code": "CHF",
        "symbol": "CHF"
      }
     ```
    Response:
    ```json
      {
        "id": 3,
        "name": "Swiss Franc",
        "code": "CHF",
        "symbol": "CHF"
      }
    ```

- **Retrieve, Update, or Delete a Currency**
    `GET /api/currencies/<int:pk>/`
    Description: Retrieve a specific currency by ID.

    `PUT /api/currencies/<int:pk>/` or `PATCH /api/currencies/<int:pk>/`
    Description: Update a currency by ID.

    `DELETE /api/currencies/<int:pk>/`
    Description**: Delete a currency by ID.

-  **Back-office**
    Login through admin section
    `/admin/currency-converter/`

    Pending Features: Add **Currency Converter** to the admin listing page for easier access.

- **Swagger endpoint**
  `/swagger/`

   Basic documentation to versioning
### Management Commands
To load historical data for the exchange rate between dates

```bash
python manage.py generate_mock_exchange_data
```

### POSTMAN Collection
API Collection file:

```
CurrencyAPI.postman_collection.json
```
