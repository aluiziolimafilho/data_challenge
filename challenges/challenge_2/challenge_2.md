
# Challenge 2

## Code step by step

### Define API infos

Here we define the URL from the API and API key which comes from environment variable for safety reasons.
```python
    API_URL = "https://api.freecurrencyapi.com/v1/latest?currencies=USD&base_currency=BRL"
    API_KEY = os.environ.get("API_KEY")
```

### Load the data

Then we load the CSV files of products and orders to transform them in pandas Dataframe.

```python
    products_df = pd.read_csv(PRODUCTS_FILENAME)
    orders_df = pd.read_csv(ORDERS_FILENAME)
```

### Join data from both dataframes

Now we join the data with a left join operation we the orders is the left resource, and therefore merge the information of products into the orders dataframe.

```python
    data_df = orders_df.join(products_df.set_index("id"), how="left", on="product_id")
```

### Get the current currency

In this step we get the current currency with an API request to convert from Brazil currency to USA currency and save the value in a variable called **usd_convert**. In the case of a fail in the request the script will dispatch an exception.

```python
    response = req.get(API_URL,headers={"apikey": API_KEY})
    response.raise_for_status()
    data = response.json()
    usd_convert = data["data"]["USD"]
```

### Calculate the total_price_br and total_price_us

To calculate the total price in BRL we just need to multiple the **quantity** column with the **price** column and then assign the result to a new column called **total_price_br**. And to calculate the total price USD we can get the result from column **total_price_br** and multiple by the variable **usd_convert** and save the result in the column **total_price_us**.

```python
    data_df["total_price_br"] = data_df["quantity"] * data_df["price"]
    data_df["total_price_us"] = data_df["total_price_br"] * usd_convert
```

### Rename columns

First we rename the columns as requested to identify the origins of them.

```python
    data_df = data_df.rename(columns={
        "created_date": "order_created_date",
        "id": "order_id", 
        "name": "product_name"
    })
```

### Select only the columns required and save the result data into a CSV file

Finally the result data can be save into CSV file with the **to_csv** function from pandas

```python
    data_df[[
        "order_created_date",
        "order_id",
        "product_name",
        "quantity",
        "total_price_br",
        "total_price_us"
    ]].to_csv(PERSISTED_DATA_FILENAME, index=None)
```

### Data analyzes

Firt calculate the date where we create the max amount of orders. To do so we need to get the data and group by the column **order_created_date** and count the number of orders in each date and then get date with the biggest number orders with max function and by filtering.

```python
    dmao = data_df[[
        "order_created_date",
        "order_id"
    ]].groupby("order_created_date").count()

    date_max_amount_orders = dmao[ dmao["order_id"] == dmao["order_id"].max()].index[0]
```

Now we need to calculate the most demanded product and the total sell price. In order to do so we need to get the data and group by the columns **product_id** and sum the values of the columns **quantity** and **total_price_br** in each group, then filter by the max value of quantity and so get the value of **product_id** which identify the product and the total price sum in the group.

```python
    mdp = data_df[["product_id","quantity","total_price_br"]].groupby("product_id").sum()
    mdp2 = mdp[mdp["quantity"] == mdp["quantity"].max()]
    most_demanded_product = mdp2.index[0]

    most_demanded_product_total_price = mdp2["total_price_br"].iloc[0]
```

The last analyzes is to get the top 3 most demanded categories. With the same strategy as before we need to group by the column **category** and sum the **quantity** in each group, then sort the result data by the sum quantity in descending way, finally we get the first 3 values of the categories.

```python
    mdc = data_df[["category","quantity"]].groupby("category").sum().sort_values("quantity", ascending=False)
    most_demanded_categories = mdc.index[:3].to_list()
```

### Save the result KPI analyzes

Now we create a dataframe based on the values calculated before, and save it into a CSV file.
```python
    kpi_df = pd.DataFrame({
        "date_max_amount_orders": [date_max_amount_orders],
        "most_demanded_product": [most_demanded_product],
        "most_demanded_product_total_price": [most_demanded_product_total_price],
        "most_demanded_categories": [";".join(most_demanded_categories)]
    })

    kpi_df.to_csv(KPI_FILENAME, index=None)
```

### Instructions to run the code

In this project the [uv tool](https://docs.astral.sh/uv/) is used to manage the python packages. Therefore to create the python virtal environment you can execute the following command.

```
    uv sync
```

With the python packages installed, you can execute the script python with the commands bellow and see the result in the file called **kpi_product_orders.csv** and the merged data in the file **fixed_order_full_information.csv**.

```
    export API_KEY=the_api_key_value
    uv run -- python challenges/challenge_2/challenge_2.py
```