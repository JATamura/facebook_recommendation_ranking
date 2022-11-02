import pandas as pd

class clean_tabular_data:

    def __init__(self):
        products = pd.read_csv("products.csv", lineterminator="\n")
        products["price"] = products["price"].str.strip("£")
        products["price"] = products["price"].str.replace(",", "")
        products["price"] = products["price"].astype("float64")

        print(products["price"])

if __name__ == "__main__":
    c = clean_tabular_data()