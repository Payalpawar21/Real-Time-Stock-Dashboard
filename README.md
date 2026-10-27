# 📈 MarketPulse — Stock Market Dashboard

A Python-based stock market analytics dashboard built with **Streamlit, Pandas, Plotly, and Alpha Vantage API**. MarketPulse allows users to explore daily stock prices, visualize price movements, and analyze market trends using technical indicators.

## ✨ Features

- **Multiple Stock Selection:** Analyze IBM, Apple (AAPL), Microsoft (MSFT), and Tesla (TSLA).
- **Interactive Candlestick Chart:** Visualize daily Open, High, Low, and Close prices.
- **Trading Volume:** Explore historical trading volume.
- **Moving Average:** Option to display a 7-day moving average.
- **RSI Indicator:** Analyze Relative Strength Index with 70 and 30 reference levels.
- **MACD Indicator:** View MACD, signal line, and histogram.
- **Historical Data:** View daily stock market data in a table.
- **CSV Export:** Download historical data for further analysis.
- **Data Caching:** Cache API responses to reduce unnecessary requests.
- **Interactive Dashboard:** Select stocks and chart periods using the sidebar.

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- Requests
- python-dotenv
- Alpha Vantage API

## 📂 Project Structure


Real-Time-Stock-Dashboard/
1. app.py
2. stock_data.py
3. requirements.txt
4. .gitignore
5. .streamlit/
  config.toml


## ⚙️ Installation and Setup

### 1. Clone the repository

git clone https://github.com/Payalpawar21/Real-Time-Stock-Dashboard.git
cd Real-Time-Stock-Dashboard


### 2. Create a virtual environment

python -m venv venv


Activate it on Windows PowerShell:

powershell
.\venv\Scripts\Activate.ps1

### 3. Install dependencies

pip install -r requirements.txt


### 4. Configure the API key

Get an API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key).

Create a `.env` file in the project root:

ALPHA_VANTAGE_API_KEY=your_actual_api_key


Replace `your_actual_api_key` with your own key.

**Security:** Never commit your `.env` file or API key to GitHub. The `.env` file should be excluded using `.gitignore`.

### 5. Run the application

streamlit run app.py


The application will open in your browser, usually at `http://localhost:8501`.

## 📊 Technical Indicators

### Relative Strength Index (RSI)

RSI is a momentum indicator used to study the strength of recent price movements. This dashboard displays reference levels at 70 and 30.

### Moving Average Convergence Divergence (MACD)

MACD compares exponential moving averages to help visualize changes in price momentum. The dashboard displays the MACD line, signal line, and histogram.

### Moving Average

The 7-day moving average helps visualize the general direction of recent closing prices.

## 📡 Data Source

MarketPulse retrieves daily stock market data from the Alpha Vantage API.

- Prices are displayed in USD.
- Data availability and update frequency depend on the API provider.
- The dashboard uses daily data and is not a live intraday trading feed.

## 🔐 Security

- API keys are stored in environment variables or Streamlit Secrets.
- Sensitive configuration files should not be committed to the repository.
- The `.gitignore` file excludes local environment and secret files.

## 🚀 Deployment

The application can be deployed using [Streamlit Community Cloud](https://share.streamlit.io/).

Configure `ALPHA_VANTAGE_API_KEY` in the app's Streamlit Secrets settings before running the deployed application.

## 🎯 Project Objective

The objective of MarketPulse is to demonstrate Python programming, API integration, data processing, interactive visualization, and basic technical analysis in a practical dashboard application.

## ⚠️ Disclaimer

MarketPulse is an educational project intended for data visualization and learning purposes only. It does not provide financial advice or guarantee investment outcomes.

## 👩‍💻 Author

**Payal Pawar**

GitHub: [Payalpawar21](https://github.com/Payalpawar21)

---

Built with Python, Pandas, Plotly, and Streamlit. 
