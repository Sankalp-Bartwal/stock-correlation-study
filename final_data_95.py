# Attempt to extract unique tickers and fetch sector data using yfinance (safely, without needing an API key)
import yfinance as yf
import pandas as pd

# Reuse the cleaned ticker list from the CSV
df_corr = pd.read_csv("filtered_correlations_095.csv")

# Get unique tickers
unique_tickers = pd.unique(df_corr[['Source_Ticker', 'Target_Ticker']].values.ravel('K'))

# Clean tickers to match Yahoo Finance format (e.g., 'BRK-B' -> 'BRK.B')
def clean_yahoo_ticker(ticker):
    return ticker.replace('-', '.')

# Fetch sector data using yfinance
sector_map_yf = {}
for ticker in unique_tickers:
    try:
        cleaned = clean_yahoo_ticker(ticker)
        info = yf.Ticker(cleaned).info
        sector = info.get('sector', None)
        sector_map_yf[ticker] = sector
    except Exception:
        sector_map_yf[ticker] = None

# Build dataframe for saving
df_sector_output = pd.DataFrame({
    'Symbol': list(sector_map_yf.keys()),
    'Sector': list(sector_map_yf.values())
})

# Add placeholder columns to match additional_data.csv structure
df_sector_output['Name'] = None
df_sector_output['Last Sale'] = None
df_sector_output['Net Change'] = None
df_sector_output['% Change'] = None
df_sector_output['Market Cap'] = None
df_sector_output['Country'] = None
df_sector_output['IPO Year'] = None
df_sector_output['Volume'] = None
df_sector_output['Industry'] = None

# Reorder columns
df_sector_output = df_sector_output[[
    'Symbol', 'Name', 'Last Sale', 'Net Change', '% Change', 'Market Cap',
    'Country', 'IPO Year', 'Volume', 'Sector', 'Industry'
]]

# Save to file
output_csv = "filled_sector_data_yfinance.csv"
df_sector_output.to_csv(output_csv, index=False)

output_csv
