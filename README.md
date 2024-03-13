# Dataset API

Test project for datasets.

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Clone the repository:

```sh
git clone https://github.com/zozulia-developer/test-dataset-api
cd test-dataset-api
```
2. Create a .env file in the project root and add the following environment variables:
```text
# Django settings
SECRET_KEY=your_secret_key
DEBUG=True
```
3. Run the following command to start the Docker containers:
```shell
docker-compose up --build
```
4. Access the application at http://localhost:8000/

## Additional Information
- The dataset.csv file should be placed in the project root directory.
- For production use, make sure to set DEBUG=False in the .env file.
- To stop the containers, run docker-compose down.
