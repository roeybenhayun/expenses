import pandas as pd
import matplotlib.pyplot as plt
import re

def analyze_supermarket_spending(csv_filepath):
    """
    Analyzes supermarket spending from a CSV file and generates a monthly stacked bar chart with average spending line.

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

    # Calculate the average monthly spending across all supermarkets
    monthly_total_spending = monthly_spending.sum(axis=1)
    average_monthly_spending = monthly_total_spending.mean()

    # Plotting the stacked bar chart
    fig, ax1 = plt.subplots(figsize=(12, 7))
    monthly_spending.plot(kind='bar', stacked=True, ax=ax1)
    ax1.set_title('Monthly Groceries Spending by Supermarket with Average Spending Line')
    ax1.set_xlabel('Month and Year')
    ax1.set_ylabel('Total Amount Spent')
    ax1.set_xticks(range(len(monthly_spending.index)))
    ax1.set_xticklabels([month.strftime('%b-%Y') for month in monthly_spending.index], rotation=45)
    ax1.legend(title='Supermarket')

    # Add the average spending line
    ax1.axhline(average_monthly_spending, color='red', linestyle='--', linewidth=1, label=f'Average: {average_monthly_spending:.2f}')
    ax1.legend(loc='upper left') # Adjust legend location to avoid overlap

    plt.tight_layout()
    plt.show()

    ## Calculate the average monthly transaction counts across all supermarkets
    monthly_total_counts = monthly_counts.sum(axis=1)
    average_monthly_counts = monthly_total_counts.mean()

    # Plotting the bar chart for transaction counts
    fig, ax2 = plt.subplots(figsize=(12, 7))
    monthly_counts.plot(kind='bar', ax=ax2)
    ax2.set_title('Monthly Number of Transactions per Supermarket with Average Transaction Count Line')
    ax2.set_xlabel('Month and Year')
    ax2.set_ylabel('Number of Transactions')
    ax2.set_xticks(range(len(monthly_counts.index)))
    ax2.set_xticklabels([month.strftime('%b-%Y') for month in monthly_counts.index], rotation=45)
    ax2.legend(title='Supermarket')

    # Add the average transaction count line
    ax2.axhline(average_monthly_counts, color='red', linestyle='--', linewidth=1, label=f'Average: {average_monthly_counts:.2f}')
    ax2.legend(loc='upper left')  # Adjust legend location to avoid overlap

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    csv_file = input("Enter the path to your CSV file: ")
    analyze_supermarket_spending(csv_file)