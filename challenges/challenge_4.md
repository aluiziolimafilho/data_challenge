# Challange 4

## Question 1

What other insights do you think would add value to the business that can be extracted using at least one of these tables?
Pick up to three, and explain why they might be useful and how we can get them. (If more tables are needed, list them.)

- We have two tables one related to product identification and the other related to events of orders requests by some client, so maybe we can collect some info related to clients, or base in the location of the deliveries, also try some optimization of inventory based on the total ordered.

- - we can analyze the quantity of products ordered based on the destination of the request, and this can help to adjust the price base on the location. In this case, it is needed a table which contains the information related to the location of the destiny.

- - we can analyza the quantity of products ordered based on the origin of the request. This can help to optimize the inventory, it is needed a table which contains the information related to the location of the warehouse/store.

- - we can use the indentification of client to identify recurrent clients by store and use this information to evaluation the effectiveness of each store, in this case we need a table to identify the clients and other table to determine the store location.

## Question 2
What ETL/ELT tool would you use to extract this data and insert it into BigQuery? Explain the steps of creating this type of pipeline.

- We can use a service offer by GCP called Dataproc and with it create a Spark cluster which it will be responsible to extract the information from the source and send it to the BigQuery, we also need the composer from GCP which runs the Airflow service, this tool will allows to control how and when to execute this pipeline. The pipeline will get the location of datasource, then start a job spark with the information from previous step and wait until it is done, finaly send some message of success of fail to some monitoring system or an alert to some service. So basicaly the pipeline will read the datasources, join the information, transform them to the structure expected and them write the result on the BigQuery. 

## Question 3
What AI-based pipeline could you add to this pipeline? Describe it. 

- As the previous described pipeline is one to extract features which can be used in machine learning models, therefore we can create a tranning pipeline to train machine learning models and attach to the previous pipeline. The tranning pipeline will load a dataset of preprocessed features, then create a machine learning model and start to train accordingly the algorithm confitured, finally the output can be a trained model and/or the performance metrics. 
Also there is the inference pipeline which it makes inferece with the machine learning models and the output of the previous pipeline can be used as input to the inference pipeline. This pipeline will load the features dataset, load the machine learning model, apply the inference on each row and write the result of the inference in a defined destination.