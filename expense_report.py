import os
import pandas as pd
import matplotlib.pyplot as plt


def load_and_clean(file):
    if not os.path.exists(file):
        raise FileNotFoundError(f"{file} not found")
    df = pd.read_csv(file)
    df = df.dropna(subset=["category", "amount"])
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["amount"])
    df = df.reset_index(drop=True)
    return df


def add_columns(df):
    df["tax"] = df["amount"]*0.05
    df["total amount"] = df["amount"]+df["tax"]
    df["expenses type"] = df["total amount"].apply(
        lambda x: "High" if x > 100 else "Normal")
    return df


def summary(df):
    category_total = df.groupby("category")["amount"].sum()
    grand_total = df["total amount"].sum()
    highest = category_total.idxmax()
    print("\nCategory Total\n", category_total)
    print("\nGrand Total\n", grand_total)
    print(f"\nHighest Category{highest}={category_total[highest]:.2f}")
    return df, category_total


def visualize(category_total, df):
    category_total.plot(kind="bar", color="skyblue", title="Total by category")
    plt.ylabel("Amount")
    plt.show()

    df.reset_index().plot(
        kind="scatter",
        x="index",
        y="amount",
        color="red",
        grid=True,
        title="Expenses Overview"
    )
    plt.show()


def main():
    df = load_and_clean("expenses_cleaned.csv")
    df = add_columns(df)
    df, category_total = summary(df)
    visualize(category_total, df)


if __name__ == "__main__":
    main()
