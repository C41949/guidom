automate:
	docker-compose up --build -d
setup:
	docker exec guidom-airflow airflow db init
	docker exec guidom-airflow airflow users create --username admin --password admin --role Admin --firstname admin --lastname admin --email admin@email.com
	docker exec guidom-airflow airflow scheduler -D 
