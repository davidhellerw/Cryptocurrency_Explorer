import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from statsmodels.tsa.arima.model import ARIMA  
import matplotlib.pyplot as plt

# Cache the result of the API call to avoid repeated API requests and minimize hitting rate limits
@st.cache_data(ttl=300)  # Cache for 5 minutes (300 seconds)
def get_top_cryptos(per_page=100):
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page={per_page}&page=1"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch cryptocurrency data. Error: {e}")
        return None

# Cache historical price data for 10 minutes to reduce API calls
@st.cache_data(ttl=600)
def get_historical_prices(crypto_id, days):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart?vs_currency=usd&days={days}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch historical price data. Error: {e}")
        return None

# Helper function to convert historical data to a DataFrame
def format_historical_data(data):
    prices = data['prices']
    df = pd.DataFrame(prices, columns=['timestamp', 'price'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# Helper function to train ARIMA model and forecast future prices
def arima_forecast(df, forecast_days):
    df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)  # Clean and convert price to float
    model = ARIMA(df['price'], order=(5, 1, 0))  # ARIMA(p,d,q), d=1 for differencing
    model_fit = model.fit()

    # Forecast prices for the next 'forecast_days' days
    forecast = model_fit.get_forecast(steps=forecast_days)
    predicted_mean = forecast.predicted_mean
    conf_int = forecast.conf_int()

    return predicted_mean, conf_int

# Function to get top 10 by specific criteria (gainers, most expensive, etc.)
def sort_cryptos(crypto_list, sort_key, reverse=True):
    return sorted(crypto_list, key=lambda x: x.get(sort_key, 0), reverse=reverse)[:10]

# Convert the data to a pandas DataFrame
def convert_to_df(crypto_list, keys):
    df = pd.DataFrame(crypto_list)
    return df[keys]

# Tab 1: Real-Time Prices 🚀
def real_time_prices():
    st.header("🚀 Real-Time Cryptocurrency Prices")
    
    # Explanation of coin selection
    st.markdown("""
    **💡 Note**: Currently, the app fetches data for the top 100 cryptocurrencies by market capitalization. You can choose any cryptocurrency from this popular list to track real-time prices.
    """)
    
    # Fetch and cache the list of cryptocurrencies
    crypto_list = get_top_cryptos()
    if crypto_list is None:
        st.error("No valid cryptocurrency data available.")
        st.stop()

    crypto_names = {crypto['id']: crypto['name'] for crypto in crypto_list}

    # User selects which cryptocurrencies they want to track
    selected_cryptos = st.multiselect(
        "🪙 Select Cryptocurrencies", 
        options=list(crypto_names.keys()), 
        default=["bitcoin"],  # Default to Bitcoin
        format_func=lambda x: crypto_names[x].capitalize()  # Capitalize the names
    )

    # Display selected cryptocurrencies' real-time prices
    for crypto in selected_cryptos:
        for item in crypto_list:
            if item['id'] == crypto:
                price = item.get('current_price', 'N/A')
                price_change = item.get('price_change_percentage_24h', 'N/A')
                market_cap = item.get('market_cap', 'N/A')

                # Format the data properly
                if isinstance(price, (int, float)):
                    if price >= 1:
                        price_formatted = f"${price:,.2f}"  # Price above 1 USD: 2 decimal places
                    else:
                        price_formatted = f"${price:,.6f}"  # Price below 1 USD: 6 decimal places
                else:
                    price_formatted = 'N/A'
                
                price_change_formatted = f"{price_change:.2f}%" if isinstance(price_change, (int, float)) else 'N/A'
                market_cap_formatted = f"${market_cap:,.0f}" if isinstance(market_cap, (int, float)) else 'N/A'

                st.subheader(f"💹 {item['name']}")
                col1, col2, col3 = st.columns([1, 1, 1.75])  # Make the Market Cap column wider
                col1.metric(label="Price", value=price_formatted)
                col2.metric(label="24h Change", value=price_change_formatted)
                col3.metric(label="Market Cap", value=market_cap_formatted)

    # Explanation message specific to Tab 1
    st.markdown("""
    ---
    **📖 What do these metrics mean?**
    
    - **Price**: The current market value of the selected cryptocurrency in USD.
    - **24h Change**: The percentage change in the cryptocurrency’s price over the past 24 hours.
    - **Market Cap**: The total value of all circulating coins/tokens in the cryptocurrency's network, calculated as price multiplied by the total circulating supply.
    """)

# Tab 2: 📈 Crypto Statistics
def crypto_statistics():
    st.header("📈 Cryptocurrency Statistics")
    
    # Fetch top 100 cryptocurrencies by market cap
    crypto_list = get_top_cryptos(100)
    if crypto_list is None:
        st.error("Failed to retrieve cryptocurrency data.")
        return

    # Display the top 10 by Market Cap as a table
    st.subheader("🏆 Top 10 Cryptocurrencies by Market Cap")
    top_market_cap = sort_cryptos(crypto_list, "market_cap")
    df_market_cap = convert_to_df(top_market_cap, ['name', 'market_cap'])
    df_market_cap.columns = ['Cryptocurrency', 'Market Cap (USD)']
    st.dataframe(df_market_cap)

    # Add note below the table
    st.markdown("""
    **Note**: The following rankings are only considering the most popular coins (the top 100 cryptocurrencies by market cap).
    """)

    # Display the top 10 Gainers in the Last 24 Hours as a table
    st.subheader("📈 Top 10 Gainers in the Last 24 Hours")
    top_gainers = sort_cryptos(crypto_list, "price_change_percentage_24h")
    df_gainers = convert_to_df(top_gainers, ['name', 'price_change_percentage_24h'])
    df_gainers.columns = ['Cryptocurrency', '24h Change (%)']
    st.dataframe(df_gainers)

    # Display the top 10 Most Expensive Cryptocurrencies as a table
    st.subheader("💰 Top 10 Most Expensive Cryptocurrencies")
    top_expensive = sort_cryptos(crypto_list, "current_price")
    df_expensive = convert_to_df(top_expensive, ['name', 'current_price'])
    df_expensive.columns = ['Cryptocurrency', 'Price (USD)']
    st.dataframe(df_expensive)

# Tab 3: Historical Prices 📊
def historical_prices():
    st.header("📊 Historical Cryptocurrency Prices")
    
    # Explanation of coin selection
    st.markdown("""
    **💡 Note**: Currently, the app fetches data for the top 100 cryptocurrencies by market capitalization. You can select a popular cryptocurrency to view its historical prices.
    """)

    # Fetch and cache the list of cryptocurrencies
    crypto_list = get_top_cryptos()
    if crypto_list is None:
        st.error("No valid cryptocurrency data available.")
        st.stop()

    crypto_names = {crypto['id']: crypto['name'] for crypto in crypto_list}

    # Set Bitcoin as the default cryptocurrency and 365 days as the default date range
    default_crypto = "bitcoin"
    default_days = 365

    # User selects the cryptocurrency (default: Bitcoin)
    selected_crypto = st.selectbox("🪙 Select a Cryptocurrency", options=list(crypto_names.keys()), index=list(crypto_names.keys()).index(default_crypto), format_func=lambda x: crypto_names[x])

    # User selects the date range (default: 365 days)
    days = st.selectbox("🗓️ Select Date Range", options=[7, 14, 30, 90, 180, 365], index=[7, 14, 30, 90, 180, 365].index(default_days), format_func=lambda x: f"Last {x} days")

    # Fetch historical prices based on user selection
    if selected_crypto and days:
        st.subheader(f"📊 Historical Prices for {crypto_names[selected_crypto]} over the last {days} days")
        historical_data = get_historical_prices(selected_crypto, days)

        if historical_data:
            # Format the data into a DataFrame and display it as a table
            df = format_historical_data(historical_data)
            st.dataframe(df)

            # Display a line chart
            st.line_chart(df.set_index('timestamp')['price'])

# Tab 4: Price Prediction 🔮
def price_prediction():
    st.header("🔮 Cryptocurrency Price Prediction")

    # Fetch and cache the list of cryptocurrencies
    crypto_list = get_top_cryptos()
    if crypto_list is None:
        st.error("No valid cryptocurrency data available.")
        st.stop()

    crypto_names = {crypto['id']: crypto['name'] for crypto in crypto_list}

    # Set Bitcoin as the default cryptocurrency and 30 days as the default prediction range
    default_crypto = "bitcoin"
    default_days = 30

    # User selects the cryptocurrency (default: Bitcoin)
    selected_crypto = st.selectbox("Select a Cryptocurrency", options=list(crypto_names.keys()), index=list(crypto_names.keys()).index(default_crypto), format_func=lambda x: crypto_names[x].capitalize())

    # User selects the prediction horizon (e.g., next 1 day, 7 days, 30 days)
    days_to_predict = st.number_input("Days to predict in the future", min_value=1, max_value=365, value=7)

    # Fetch historical prices based on user selection
    st.subheader(f"Predicting future prices for {crypto_names[selected_crypto]} based on past data")
    historical_data = get_historical_prices(selected_crypto, 365)  # Fetch past 365 days of data to train the model

    if historical_data:
        # Format the data into a DataFrame
        df = format_historical_data(historical_data)

        # Train ARIMA model and forecast future prices
        predicted_mean, conf_int = arima_forecast(df, days_to_predict)

        # Prepare forecast results for display
        future_dates = pd.date_range(df['timestamp'].iloc[-1], periods=days_to_predict+1, freq='D')[1:]  # Next N days
        forecast_df = pd.DataFrame({
            'Date': future_dates,
            'Predicted Price (USD)': predicted_mean,
            'Lower Confidence Interval': conf_int.iloc[:, 0],
            'Upper Confidence Interval': conf_int.iloc[:, 1]
        })

        # Display the forecast results in a table (with better formatting)
        st.subheader(f"Predicted Prices for the next {days_to_predict} days")
        st.dataframe(forecast_df.style.format({
            'Predicted Price (USD)': '{:.2f}',
            'Lower Confidence Interval (USD)': '{:.2f}',
            'Upper Confidence Interval (USD)': '{:.2f}'
         }))

        # Plot the historical prices along with the forecast
        fig, ax = plt.subplots()
        ax.plot(df['timestamp'], df['price'], label='Historical Prices')
        ax.plot(forecast_df['Date'], forecast_df['Predicted Price (USD)'], label='Predicted Prices', color='orange')
        ax.fill_between(forecast_df['Date'], forecast_df['Lower Confidence Interval'], forecast_df['Upper Confidence Interval'], color='orange', alpha=0.3)
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (USD)")
        ax.legend()

        # Display the chart
        st.pyplot(fig)

    # Explanation of ARIMA and its limitations in simple terms
    st.markdown("""
    **How ARIMA Works for Price Prediction:**
    
    The ARIMA model (AutoRegressive Integrated Moving Average) is a popular time series forecasting method. It analyzes historical price patterns to predict future prices.
    
    - **Short-Term Predictions**: ARIMA is best suited for short-term price predictions because it captures recent trends and fluctuations.
    - **Long-Term Predictions**: As the number of days increases, ARIMA’s accuracy can decrease. Predictions beyond a certain point become less reliable due to the volatile and unpredictable nature of cryptocurrency markets.
    
    **Understanding Confidence Intervals:**
    
    The confidence intervals shown alongside the predicted prices provide a 95% range within which the actual price is expected to fall. A narrower interval indicates higher confidence in the prediction, while a wider interval shows more uncertainty. 
    """)

def overview_section():
    st.header("App Overview")
    
    # Picture and introduction
    st.write("""
    Welcome to the Cryptocurrency Explorer! This app offers multiple functionalities for cryptocurrency enthusiasts and data analysts, allowing you to explore real-time data, historical prices, and make price predictions for popular cryptocurrencies.
    
    ## Features:
    
    - **Real-Time Prices**: View up-to-date prices of selected cryptocurrencies, along with their 24-hour change and market cap.
    
    - **Cryptocurrency Statistics**: Explore the top 10 cryptocurrencies by market cap, the top gainers in the past 24 hours, and the most expensive cryptocurrencies.
    
    - **Historical Prices**: Track the historical price trends of your favorite cryptocurrencies for up to 365 days.
    
    - **Price Prediction**: Predict the future prices of cryptocurrencies using the ARIMA model. Note that predictions for shorter time frames tend to be more accurate than for longer ones.
    
    ## About the Author:
    
    My name is David Heller, and I'm a data scientist with a background in finance, passionate about cryptocurrencies and machine learning. I built this app to help others explore and analyze the world of crypto through interactive data tools.
    
    Feel free to connect with me on LinkedIn or explore my GitHub for more projects!
    
    - [LinkedIn](https://www.linkedin.com/in/david-heller-w)
    - [GitHub](https://github.com/davidhellerw)
    """)

    st.image("my_image.jpg", width=300)  


# Streamlit app config
st.set_page_config(
    page_title="Cryptocurrency Explorer",  # Custom page title for the browser tab
    page_icon="💹"
)

# Streamlit app
def navigation_buttons():

    tabs = ["App Overview", "Real-Time Prices", "Crypto Statistics", "Historical Prices", "Price Prediction"]
    selected_tab = st.sidebar.selectbox("Select a page", tabs)
    
    if selected_tab == "App Overview":
        overview_section()
    elif selected_tab == "Real-Time Prices":
        real_time_prices()
    elif selected_tab == "Crypto Statistics":
        crypto_statistics()
    elif selected_tab == "Historical Prices":
        historical_prices()
    elif selected_tab == "Price Prediction":
        price_prediction()

    # Image in sidebar
    st.sidebar.image('crypto_image.jpg', use_column_width=True)

# Main app
st.title("Cryptocurrency Explorer 🚀")
navigation_buttons()

