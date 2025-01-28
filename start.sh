if ! docker network ls | grep -q "elt_network"; then
  echo "Create elt_network"
  docker network create elt_network
else
  echo "elt_network found"
fi

docker compose up init-airflow

sleep 5

docker compose up -d
