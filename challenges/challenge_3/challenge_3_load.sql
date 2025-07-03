
DROP table if exists public.products;


CREATE TABLE public.products (
	id int4 NOT NULL,
	"name" varchar(50) NULL,
	category varchar(50) NULL,
	price float4 NULL
);

CREATE INDEX products_id_idx ON public.products (id);


DROP table if exists public.orders;

CREATE TABLE public.orders (
	id int4 NOT NULL,
	product_id int4 NULL,
	quantity int4 NULL,
	created_date varchar(50) null
);

CREATE INDEX orders_product_id_idx ON public.orders (product_id);


-- https://www.postgresql.org/docs/current/sql-copy.html


COPY public.products 
FROM '/datasource/products.csv'
with ( delimiter ',' , header true );


COPY public.orders 
FROM '/datasource/orders.csv'
with ( delimiter ',' , header true );