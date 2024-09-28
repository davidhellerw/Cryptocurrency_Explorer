<h1>Cryptocurrency Explorer 🚀</h1>

<p>
    <strong>Cryptocurrency Explorer</strong> is a comprehensive application built to provide real-time data tracking, historical analysis, and predictive modeling of cryptocurrency prices. It leverages cutting-edge technologies to deliver an intuitive, user-friendly experience for both casual enthusiasts and data professionals alike. This app allows users to explore cryptocurrency markets, gain insights into historical trends, and predict future prices using the ARIMA forecasting model.
</p>

<h2>🌟 Purpose of the App</h2>
<p>
    In the rapidly evolving world of cryptocurrency, staying informed is crucial. The Cryptocurrency Explorer app is designed to meet the needs of users who want a one-stop solution for tracking real-time prices, performing historical data analysis, and forecasting potential future trends. Whether you're an investor, a crypto enthusiast, or a data scientist looking to experiment with market data, this app provides the tools and data required to make well-informed decisions.
</p>

<h2>🚀 Live App</h2>
<p>
    You can explore the deployed app by visiting this link: <a href="https://cryptocurrencyexplorer.streamlit.app/">Cryptocurrency Explorer</a>.
</p>

<h2>🔧 Process of Building the App</h2>
<p>
    The development of Cryptocurrency Explorer followed a structured process, starting from data acquisition to implementing real-time analytics, visualizations, and predictive modeling. Here's an overview of the steps taken:
</p>

<ul>
    <li>
        <strong>Data Acquisition:</strong> The app uses the <a href="https://www.coingecko.com/en/api">CoinGecko API</a>, a highly reliable source of cryptocurrency data. Through this API, we fetch real-time price data, historical market trends, and detailed statistics for the top 100 cryptocurrencies. Due to the free version of the API, we chose to limit the app to the top 100 coins to be mindful of API request limits. This decision ensures that we can still provide rich data without exceeding the API’s rate limits.
    </li>
    <li>
        <strong>Data Caching:</strong> Since cryptocurrency data changes rapidly, we implemented caching using Streamlit's native caching mechanism. This ensures that frequent API calls are minimized, improving performance and reducing the risk of hitting API rate limits. By caching API results, we deliver near-instant responses to users for data that doesn't change frequently, like historical prices.
    </li>
    <li>
        <strong>Real-Time Data Tracking:</strong> Users can monitor the real-time prices of selected cryptocurrencies, including their market cap and 24-hour price change. This allows the app to serve as an excellent dashboard for users who want to keep track of the latest price movements.
    </li>
    <li>
        <strong>Historical Data Analysis:</strong> Users can analyze the historical performance of cryptocurrencies for various time periods (e.g., 7 days, 30 days, 365 days). The app transforms the raw historical data into easy-to-read charts and tables, helping users visualize price trends over time.
    </li>
    <li>
        <strong>Price Prediction:</strong> The ARIMA (AutoRegressive Integrated Moving Average) model is implemented to provide short-term price predictions based on historical data. ARIMA was chosen primarily because of its simplicity and effectiveness in short-term forecasting. Additionally, ARIMA does not require a large amount of parameter tuning compared to more complex models, making it an ideal choice for users who need quick predictions.
    </li>
    <li>
        <strong>User Interface:</strong> The app's interface is designed using Streamlit, with a focus on simplicity and ease of use. Key sections of the app are accessible via the sidebar, allowing users to easily switch between real-time prices, historical data analysis, statistics, and predictions. Visualization is achieved using libraries like Matplotlib and Streamlit’s built-in data display tools.
    </li>
</ul>

<h2>💾 Data Caching and API Usage</h2>
<p>
    Given the dynamic nature of cryptocurrency data, the app utilizes caching to reduce the number of API calls and provide a smoother user experience. Here’s how caching is implemented:
</p>

<ul>
    <li>
        <strong>Real-Time Data:</strong> Data for real-time prices is cached for 5 minutes using Streamlit’s <code>@st.cache_data</code> decorator. This ensures that API calls are minimized, while still delivering near real-time data to users. After 5 minutes, the cache expires, and new data is fetched from the API.
    </li>
    <li>
        <strong>Historical Data:</strong> Historical price data is cached for 10 minutes. Since historical data is not subject to rapid changes, a longer cache time is appropriate. This reduces the frequency of API calls for users performing multiple historical analyses in a single session.
    </li>
</ul>

<p>
    All data is fetched from the <a href="https://www.coingecko.com/en/api">CoinGecko API</a>, a well-established API that provides accurate and comprehensive data on a large number of cryptocurrencies. The API allows us to retrieve real-time prices, market capitalization, price changes, and historical price data, which are crucial for the various features of the app. We work with the top 100 cryptocurrencies due to the limitations of the free version of the API, ensuring that we stay within the rate limits and provide valuable insights without overwhelming the system.
</p>

<h2>📊 ARIMA Model and Why It’s Used</h2>
<p>
    The ARIMA model, short for AutoRegressive Integrated Moving Average, is a popular choice for time series forecasting. For this app, ARIMA was chosen primarily because of its <strong>simplicity</strong>. It provides a straightforward approach to short-term predictions and is capable of capturing important trends in the data without the need for extensive parameter tuning. This makes ARIMA an ideal model for rapid deployment and efficient predictions, especially for users who want quick insights without dealing with complex machine learning models.
</p>

<h3>How ARIMA Works</h3>
<ul>
    <li>
        <strong>AutoRegressive (AR):</strong> The model uses past values to predict future values. In this case, it looks at past cryptocurrency prices to predict future prices.
    </li>
    <li>
        <strong>Integrated (I):</strong> The data is differenced to make it stationary (i.e., remove trends or seasonality). This helps the model focus on the core price dynamics, eliminating long-term trends.
    </li>
    <li>
        <strong>Moving Average (MA):</strong> ARIMA models the relationship between a cryptocurrency’s past errors and the current price, allowing it to account for unexpected fluctuations.
    </li>
</ul>

<p>
    In this app, ARIMA is configured with the parameters <code>order=(5, 1, 0)</code>. These numbers represent:
</p>
<ul>
    <li><strong>p = 5:</strong> The number of lag observations included in the model (AutoRegressive component).</li>
    <li><strong>d = 1:</strong> The number of times that the raw observations are differenced to make the series stationary (Integrated component).</li>
    <li><strong>q = 0:</strong> The size of the moving average window (Moving Average component).</li>
</ul>

<h3>Limitations of ARIMA</h3>
<p>
    While ARIMA is well-suited for short-term forecasting, it has some limitations:
</p>
<ul>
    <li>
        <strong>Short-Term Focus:</strong> ARIMA is designed to provide accurate predictions in the short term. As the prediction horizon extends (e.g., 100 days into the future), the model’s accuracy diminishes, and the confidence intervals widen. The model struggles with long-term forecasts because it doesn't account for structural breaks or external factors that could impact cryptocurrency markets.
    </li>
    <li>
        <strong>Volatility:</strong> Cryptocurrency markets are highly volatile, and ARIMA cannot capture sudden market shocks or events such as new regulations, technological advancements, or large-scale transactions.
    </li>
</ul>

<h2>📊 Understanding Confidence Intervals</h2>
<p>
    The confidence intervals displayed alongside the ARIMA predictions represent the range within which the actual price is expected to fall, with a 95% confidence level. This means that there is a 95% probability that the actual cryptocurrency price will fall between the lower and upper bounds of the confidence interval.
</p>
<p>
    In the app, the confidence intervals are labeled as <strong>Lower Confidence Interval (USD)</strong> and <strong>Upper Confidence Interval (USD)</strong> to reflect the currency. As the prediction window expands (e.g., predicting 100 days into the future), these intervals widen, indicating growing uncertainty in the predictions.
</p>

<h2>🚀 Features</h2>
<p>
    The app comes packed with several features designed for cryptocurrency enthusiasts and data professionals:
</p>
<ul>
    <li><strong>Real-Time Prices:</strong> Get live price data for the top 100 cryptocurrencies, along with market cap, 24-hour price change, and detailed metrics.</li>
    <li><strong>Cryptocurrency Statistics:</strong> Analyze top cryptocurrencies by market cap, view top gainers, and explore the most expensive coins in the market.</li>
    <li><strong>Historical Prices:</strong> Visualize historical prices for different time frames (7, 14, 30, 90, 180, and 365 days). Historical trends help you understand the price movements over time.</li>
    <li><strong>Price Prediction:</strong> Use ARIMA forecasting to predict cryptocurrency prices for the next few days or weeks. Ideal for users who want short-term forecasts to make data-driven decisions.</li>
</ul>

<h2>📂 Project Structure</h2>
<pre><code>
Cryptocurrency_Explorer/
│
├── .streamlit/                    # Contains theme settings for the app
│   └── config.toml                # Dark theme configuration file
├── Cryptocurrency_Explorer_App.py  # Main app script
├── README.md                      # Documentation for the app
├── crypto_image.jpg               # Background image for the app
├── my_image.jpg                   # Author's image for the "About" section
├── requirements.txt               # List of dependencies for the project
└── LICENSE                        # License file (MIT)
</code></pre>

<h2>🛠 How to Run the App Locally</h2>
<ol>
    <li><strong>Clone the Repository:</strong></li>
    <pre><code>git clone https://github.com/davidhellerw/Cryptocurrency_Explorer.git
cd Cryptocurrency_Explorer
</code></pre>
    <li><strong>Install Dependencies:</strong> Run the following command to install all necessary Python packages:
    <pre><code>pip install -r requirements.txt</code></pre>
    </li>
    <li><strong>Run the App:</strong> Once the dependencies are installed, start the Streamlit app using:
    <pre><code>streamlit run Cryptocurrency_Explorer_App.py</code></pre>
    </li>
    <li><strong>Access the App:</strong> After running the command, you can access the app locally at:
    <pre><code>http://localhost:8501</code></pre>
    </li>
</ol>

<h2>🚀 Deployment</h2>
<p>
    The app is designed to be deployed using platforms like <strong>Streamlit Cloud</strong>, <strong>Heroku</strong>, or any cloud service supporting Python applications. To deploy:
</p>
<ol>
    <li>Ensure your code is pushed to a GitHub repository.</li>
    <li>Configure deployment settings on your chosen platform.</li>
    <li>Ensure the <code>requirements.txt</code> file is present to install dependencies.</li>
    <li>Deploy and monitor performance using the platform's dashboard.</li>
</ol>

<h2>👤 About the Author</h2>
<p>
    I’m <strong>David Heller</strong>, a passionate data scientist with a strong background in finance and machine learning. I built this app to combine my interests in data science and cryptocurrency, making it easier for others to gain insights into the rapidly changing crypto market.
</p>
<p>
    Feel free to connect with me on LinkedIn or check out more of my projects on GitHub:
</p>
<ul>
    <li><a href="https://www.linkedin.com/in/david-heller-w">LinkedIn</a></li>
    <li><a href="https://github.com/davidhellerw">GitHub</a></li>
</ul>

<h2>🖼 Screenshots</h2>
<p>
    Add relevant screenshots here to showcase the app’s different sections and features in action.
</p>

<h2>📜 License</h2>
<p>
    This project is licensed under the MIT License - see the <a href="LICENSE">LICENSE</a> file for more details.
</p>
