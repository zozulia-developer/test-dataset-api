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
2. Create a `.env` file in the project root and add the following environment variables from `.env.example`
3. Run the following command to start the Docker containers:
```shell
docker-compose up --build
```
4. Access the application at http://localhost:8000/
5. Access the admin panel at http://localhost:8000/admin/
6. Access the swagger at http://localhost:8000/swagger/

## Additional Information
- The dataset.csv file should be placed in the project root directory.
- For production use, make sure to set DEBUG=False in the .env file.
- To stop the containers, run docker-compose down.
