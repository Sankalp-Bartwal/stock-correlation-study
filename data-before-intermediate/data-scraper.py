# import yfinance as yf
import pandas as pd
# import time


def convertToList(data):
    new_data = data.split("\n")
    temp = []

    for index, value in enumerate(new_data):
        if index == 0:
            continue
        
        temp.append(float(value.split()[-1]))

    return temp

def getYearlyClosingPrice(tickers: list):
    start_date = '2024-02-01'
    end_date = '2025-02-28'

    closing_price = {}

    for index, ticker in enumerate(tickers):
        if(index == 1000):
            time.sleep(150)
        
        try:
            #data = yf.download("AMZN AAPL GOOG", start="2017-01-01", end="2017-04-30")
            # Download historical data for the ticker
            # stock_data = yf.download(ticker, start=start_date, end=end_date)
            stock = yf.Ticker(ticker)
            stock_data = stock.history(start=start_date, end=end_date, interval="1d")
            
            # Extract the 'Close' column and convert it to a dictionary
            # print(stock_data["Close"].column)
            
            #closing_price[ticker] = stock_data["Close"].to_string()
            temp = stock_data["Close"].to_string()
            if not stock_data.empty:
                closing_price[ticker] = convertToList(temp)
            
            # print(closing_price)
            # Append the ticker and its closing prices to the list
            # closing_price.append({ticker: close_price})
            
            print(f"Retrieved data for {ticker}")
        except Exception as e:
            print(f"Failed to retrieve data for {ticker}: {e}")
    # print(closing_price["NVDA"])

    return closing_price

def getTopCapTickers(size: int):
    csv_file_path = './companiesmarketcap.com - Largest American companies by market capitalization.csv'
    # csv_file_path = "./test.csv"
    tickers_df = pd.read_csv(csv_file_path)
    return tickers_df['Symbol'].head(size).tolist()

def calculateCorrelation(data):
    # Find the maximum length of the lists
    max_length = max(len(v) for v in data.values())

    # Pad shorter lists with NaN
    for key in data:
        data[key] = data[key] + [float('nan')] * (max_length - len(data[key]))

    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(data)

    # Calculate the correlation matrix
    correlation_matrix = df.corr()

    # Initialize a list to store pairwise correlations
    pairwise_correlations = []

    # Extract correlation coefficients for every pair of tickers
    tickers = df.columns
    for i in range(len(tickers)):
        for j in range(i + 1, len(tickers)):
            ticker1 = tickers[i]
            ticker2 = tickers[j]
            correlation = correlation_matrix.loc[ticker1, ticker2]
            pairwise_correlations.append([ticker1, ticker2, correlation])

    # Convert the list to a DataFrame
    correlation_df = pd.DataFrame(pairwise_correlations, columns=['Ticker 1', 'Ticker 2', 'Correlation'])

    # Save the DataFrame to a CSV file
    output_file = 'pairwise_correlations.csv'
    correlation_df.to_csv(output_file, index=False)

def filter_correlation(csv_file, output_file, threshold=0.6):
    """
    Load a CSV file, filter rows based on the absolute value of the correlation,
    and save the filtered data to a new CSV file.

    Parameters:
        csv_file (str): Path to the input CSV file.
        output_file (str): Path to save the filtered CSV file.
        threshold (float): Correlation threshold (default is 0.5).
    """
    # Load the CSV file
    df = pd.read_csv(csv_file)

    # Filter rows where the absolute value of correlation is >= threshold
    filtered_df = df[df['Correlation'].abs() >= threshold]

    # Save the filtered DataFrame to a new CSV file
    filtered_df.to_csv(output_file, index=False)
    print(f"Filtered data saved to {output_file}")

def main():
    # MAX_SIZE = 2000
    # # MAX_SIZE = 3
    # tickers = getTopCapTickers(MAX_SIZE)
    # # print(tickers)
    # #### Take the tickers use yfinance to get the correlation 
    # ## store it as dict <(comp1, comp2)> = correlation
    # #then create csv through that dict
    # closing_prices = getYearlyClosingPrice(tickers)
    # #print(closing_prices)

    # calculateCorrelation(closing_prices)

    input_csv = "pairwise_correlations.csv"  # Replace with your input CSV file
    output_csv = "filtered_correlations.csv"  # Replace with your desired output file
    filter_correlation(input_csv, output_csv)

if __name__ == "__main__":
    main()