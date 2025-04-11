docker build . -f Dockerfile.postgress -t my-postgres-image
docker run -it --user root --name my-postgres-container my-postgres-image
docker rm -f my-postgres-container & docker rmi my-postgres-image
