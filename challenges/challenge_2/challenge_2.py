import pandas as pd
import os
from decimal import Decimal
import requests as req

PRODUCTS_FILENAME = "data/products.csv"
ORDERS_FILENAME = "data/orders.csv"

PERSISTED_DATA_FILENAME = "fixed_order_full_information.csv"
KPI_FILENAME = "kpi_product_orders.csv"

## API infos
API_URL = "https://api.freecurrencyapi.com/v1/latest?currencies=USD&base_currency=BRL"
API_KEY = os.environ.get("API_KEY")

## load data source into dataframes
products_df = pd.read_csv(PRODUCTS_FILENAME)
orders_df = pd.read_csv(ORDERS_FILENAME)

## join data
data_df = orders_df.join(products_df.set_index("id"), how="left", on="product_id")

## get current currency
response = req.get(API_URL,headers={"apikey": API_KEY})
response.raise_for_status()
data = response.json()
usd_convert = data["data"]["USD"]

## calculate total_price

data_df["total_price_br"] = data_df["quantity"] * data_df["price"]
data_df["total_price_us"] = data_df["total_price_br"] * usd_convert

## rename columns
data_df = data_df.rename(columns={
    "created_date": "order_created_date",
    "id": "order_id", 
    "name": "product_name"
})

## select columns and persist the joined data
data_df[[
    "order_created_date",
    "order_id",
    "product_name",
    "quantity",
    "total_price_br",
    "total_price_us"
]].to_csv(PERSISTED_DATA_FILENAME, index=None)

## kpi analysis

### date_max_amount_orders
dmao = data_df[[
    "order_created_date",
    "order_id"
]].groupby("order_created_date").count()

date_max_amount_orders = dmao[ dmao["order_id"] == dmao["order_id"].max()].index[0]

### most_demanded_product and most_demanded_product_total_price
mdp = data_df[["product_id","quantity","total_price_br"]].groupby("product_id").sum()
mdp2 = mdp[mdp["quantity"] == mdp["quantity"].max()]
most_demanded_product = mdp2.index[0]

most_demanded_product_total_price = mdp2["total_price_br"].iloc[0]

### most_demanded_categories
mdc = data_df[["category","quantity"]].groupby("category").sum().sort_values("quantity", ascending=False)
most_demanded_categories = mdc.index[:3].to_list()


## result kpi dataframe
kpi_df = pd.DataFrame({
    "date_max_amount_orders": [date_max_amount_orders],
    "most_demanded_product": [most_demanded_product],
    "most_demanded_product_total_price": [most_demanded_product_total_price],
    "most_demanded_categories": [";".join(most_demanded_categories)]
})
print(kpi_df)

kpi_df.to_csv(KPI_FILENAME, index=None)


