# Challenge 3

## SQL load data step by step

First create a table for the products data and another for the orders data. Create also some index to improve the speed of some queries.

```sql
CREATE TABLE public.products (
	id int4 NOT NULL,
	"name" varchar(50) NULL,
	category varchar(50) NULL,
	price float4 NULL
);
CREATE INDEX products_id_idx ON public.products (id);

CREATE TABLE public.orders (
	id int4 NOT NULL,
	product_id int4 NULL,
	quantity int4 NULL,
	created_date varchar(50) null
);
CREATE INDEX orders_product_id_idx ON public.orders (product_id);
```

Then load the data into the tables with the follow script ([sql-copy](https://www.postgresql.org/docs/current/sql-copy.html)).
```sql
COPY public.products 
FROM '/datasource/products.csv'
with ( delimiter ',' , header true );

COPY public.orders 
FROM '/datasource/orders.csv'
with ( delimiter ',' , header true );
```

## SQL Analyzes

First we create a CTE called **join_orders_products** which joins the information of orders and products, then we group by **created_date** and count the number of orders and use another CTE (**group_dates**) to hold this info. Now we can calculate the date where there is the max amounnt of orders, by selecting the max value from previous count and filtering the group_dates with this value.

Next we get the **join_orders_products** group by **product_id** and sum the quantities in each group, then hold this info in a CTE called **group_products**. Now we can calculate the most demanded product by selecting the max value quantity and filtering group_products with this value.

Next we get the **join_orders_products** group by **category** and sum the quantities in each group, then sort the result by the summed quantities and get the first 3 elements, finally we join theses elements to become one and so we have the top 3 most demanded categories.

Finally we join the information from the result CTEs **max_amount_date**, **most_demanded_product** and **most_demanded_categories** to present the final result.

```sql
with join_orders_products as (
	select * from orders o
	left join products p
	on o.product_id = p.id 
),
group_dates as (
	select created_date, count(*) as amount 
	from join_orders_products j
	group by j.created_date
),
max_amount_date as (
	select gd.created_date 
	from group_dates gd
	where gd.amount in (select max(sb.amount) from group_dates sb)
	limit 1
),
group_products as (
	select j.product_id, sum(j.quantity) as demand 
	from join_orders_products j
	group by j.product_id
),
most_demanded_product as (
	select gp.product_id 
	from group_products gp
	where gp.demand in (select max(sp.demand) from group_products sp)
	limit 1
),
most_demanded_categories as (
	select string_agg(sq.category, ', ') as category from (
		select j.category
		from join_orders_products j
		group by j.category
		order by sum(j.quantity) desc
		limit 3
	) as sq
)
	select 
		r1.created_date as date_max_amount_orders, 
		r2.product_id as most_demanded_product,
		r3.category as most_demanded_categories
	from max_amount_date r1, most_demanded_product r2, most_demanded_categories r3;
```

## Run the scripts

Execute the command bellow to create a local postgres database with docker
```sh
    docker compose up -d
```

Then access this database with some database client like [dbeaver](https://dbeaver.com). The credentials to connect are inside the **compose.yaml** file.

Finally execute the first script (**challenge_3_load.sql**) to create the tables and load the data, then execute the second script (**challenge_3_analysis.sql**) to make the analyzes of the data.