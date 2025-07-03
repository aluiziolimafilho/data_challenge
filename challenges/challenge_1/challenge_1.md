
# Challenge 1

## Code step by step

### Load the data

First we load the CSV files of products and orders to transform them in pandas Dataframe.

```python
    products_df = pd.read_csv(PRODUCTS_FILENAME)
    orders_df = pd.read_csv(ORDERS_FILENAME)
```

### Join data from both dataframes

Now we join the data with a left join operation we the orders is the left resource, and therefore merge the information of products into the orders dataframe.

```python
    data_df = orders_df.join(products_df.set_index("id"), how="left", on="product_id")
```

### Calculate the total_price

To calculate the total price we just need to multiple the **quantity** column with the **price** column and then assign the result to a new column called **total_price**
```python
    data_df["total_price"] = data_df["quantity"] * data_df["price"]
```

### Rename columns and select only the columns required

First we rename the columns as requested to identify the origins of them. In the sequence we select only the required columns.

```python
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
```

### Save the result data into a CSV file

Finally the result data can be save into CSV file with the **to_csv** function from pandas

```python
    result_df.to_csv(OUTPUT_FILENAME, index=None)
```

### Instructions to run the code

In this project the [uv tool](https://docs.astral.sh/uv/) is used to manage the python packages. Therefore to create the python virtal environment you can execute the following command.

```
    uv sync
```

With the python packages installed, you can execute the script python with the command bellow and see the result in the file called **order_full_information.csv** .
```
    uv run -- python challenges/challenge_1/challenge_1.py
```