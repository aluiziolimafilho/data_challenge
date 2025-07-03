import pandas as pd

## load data source into dataframes
PRODUCTS_FILENAME = "data/products.csv"
ORDERS_FILENAME = "data/orders.csv"
OUTPUT_FILENAME = "order_full_information.csv"

products_df = pd.read_csv(PRODUCTS_FILENAME)
orders_df = pd.read_csv(ORDERS_FILENAME)

## join data
data_df = orders_df.join(products_df.set_index("id"), how="left", on="product_id")

## calculate total_price
data_df["total_price"] = data_df["quantity"] * data_df["price"]

## rename and select columns
result_df = data_df.rename(columns={
    "created_date": "order_created_date",
    "id": "order_id", 
    "name": "product_name"
})
result_df = result_df[[
    "order_created_date",
    "order_id",
    "product_name",
    "quantity",
    "total_price"
]]

## save the output data
result_df.to_csv(OUTPUT_FILENAME, index=None)

