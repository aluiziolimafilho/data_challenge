--set enable_seqscan = FALSE;
--set enable_seqscan = TRUE;

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
