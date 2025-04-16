import pandas as pd
import matplotlib.pyplot as plt
import re

def analyze_supermarket_spending(csv_filepath):
    """
    Analyzes supermarket spending from a CSV file and generates a monthly stacked bar chart.

    Args:
        csv_filepath (str): The path to the CSV file.
    """
    try:
        df = pd.read_csv(csv_filepath)
    except FileNotFoundError:
        print(f"Error: File not found at {csv_filepath}")
        return

    # Ensure correct column names are used
    if not all(col in df.columns for col in ["description", "amount", "transactiondate"]):
        print("Error: The CSV file must contain columns named 'description', 'amount', and 'transactiondate'.")
        return

    # Convert amount to positive float
    df['amount'] = df['amount'].abs().astype(float)

    # Convert transaction date to datetime objects
    df['transactiondate'] = pd.to_datetime(df['transactiondate'], format='%Y%m%d')

    # Filter for the specified supermarkets
    supermarkets = ['ALBERT HEIJN', 'Makro', 'Jumbo',"darya"]
    supermarket_df = df[df['description'].str.contains('|'.join(supermarkets), case=False, regex=True)].copy()

    if supermarket_df.empty:
        print("No transactions found for the specified supermarkets.")
        return

    # Extract supermarket name (handling potential variations)
    def extract_supermarket(description):
        for name in supermarkets:
            if re.search(r'\b' + re.escape(name) + r'\b', description, re.IGNORECASE):
                return name
        return None

    supermarket_df['supermarket'] = supermarket_df['description'].apply(extract_supermarket)
    supermarket_df.dropna(subset=['supermarket'], inplace=True)

    # Monthly Analysis for Stacked Bar Chart
    monthly_spending = supermarket_df.groupby([pd.Grouper(key='transactiondate', freq='M'), 'supermarket'])['amount'].sum().unstack(fill_value=0)
    monthly_counts = supermarket_df.groupby([pd.Grouper(key='transactiondate', freq='M'), 'supermarket']).size().unstack(fill_value=0)


    # Plotting the stacked bar chart
    monthly_spending.plot(kind='bar', stacked=True, figsize=(12, 7))
    plt.title('Monthly Groceries Spending by Supermarket')
    plt.xlabel('Month and Year')
    plt.ylabel('Total Amount Spent')
    plt.xticks(rotation=45)

    # Format x-axis labels to show only Month and Year
    months = monthly_spending.index
    month_year_labels = [month.strftime('%b-%Y') for month in months]
    plt.gca().set_xticklabels(month_year_labels)

    plt.legend(title='Supermarket')
    plt.tight_layout()
    plt.show()

    # Plotting the bar chart for transaction counts
    monthly_counts.plot(kind='bar', figsize=(12, 7))
    plt.title('Monthly Number of Transactions per Supermarket')
    plt.xlabel('Month and Year')
    plt.ylabel('Number of Transactions')
    plt.xticks(rotation=45)
    plt.gca().set_xticklabels([month.strftime('%b-%Y') for month in monthly_counts.index])
    plt.legend(title='Supermarket')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    csv_file = input("Enter the path to your CSV file: ")
    analyze_supermarket_spending(csv_file)