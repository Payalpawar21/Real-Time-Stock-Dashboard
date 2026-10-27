
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from stock_data import get_stock_data


# ---------- Page Configuration ----------
st.set_page_config(
    page_title="MarketPulse | Stock Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------- Header ----------
st.title("📈 MarketPulse")
st.caption(
    "STOCK MARKET ANALYTICS • DAILY PRICE TRACKING • TECHNICAL INDICATORS"
)


# ---------- Sidebar ----------
with st.sidebar:
    st.title("MarketPulse")
    st.caption("Your stock market workspace")
    st.divider()

    st.subheader("Dashboard Settings")

    symbol = st.selectbox(
        "Select Stock",
        ["IBM", "AAPL", "MSFT", "TSLA"],
        index=0
    )

    period = st.selectbox(
        "Chart Period",
        [
            "1 Month",
            "3 Months",
            "6 Months",
            "Last 100 Trading Days"
        ],
        index=0
    )

    show_ma = st.toggle(
        "Show 7-day moving average",
        value=True
    )

    refresh = st.button(
        "🔄 Refresh Data",
        use_container_width=True
    )

    if refresh:
        get_stock_data.clear()

    st.divider()
    st.caption("Data source: Alpha Vantage")
    st.caption("Daily stock data; not a live intraday feed.")
    st.caption("Educational project — not investment advice.")


# ---------- Main Dashboard ----------
try:
    with st.spinner("Loading market data..."):
        df = get_stock_data(symbol)

    if df.empty:
        st.warning("No stock data is available for this symbol.")
        st.stop()

    required_columns = [
        "Open", "High", "Low", "Close", "Volume"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing stock data columns: {missing_columns}"
        )

    df = df.sort_index().copy()

    # ---------- Market Summary ----------
    latest = df.iloc[-1]
    previous = df.iloc[-2] if len(df) > 1 else latest

    price = float(latest["Close"])
    previous_close = float(previous["Close"])

    change = price - previous_close
    change_pct = (
        (change / previous_close) * 100
        if previous_close != 0 else 0
    )

    st.subheader(f"{symbol} Market Overview")

    st.caption(
        f"Latest available trading date: "
        f"{df.index[-1].strftime('%d %b %Y')}"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "Latest Close",
            f"${price:,.2f}",
            f"{change:+.2f} ({change_pct:+.2f}%)"
        )

    with c2:
        st.metric(
            "Day High",
            f"${float(latest['High']):,.2f}"
        )

    with c3:
        st.metric(
            "Day Low",
            f"${float(latest['Low']):,.2f}"
        )

    with c4:
        st.metric(
            "Trading Volume",
            f"{int(latest['Volume']):,}"
        )

    st.divider()

    # ---------- Calculate Indicators on Full Available History ----------
    # Calculate indicators before filtering the chart period.
    # This gives RSI and MACD more historical data to work with.

    # RSI: 14-period Relative Strength Index
    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(
        alpha=1 / 14,
        min_periods=14,
        adjust=False
    ).mean()

    avg_loss = loss.ewm(
        alpha=1 / 14,
        min_periods=14,
        adjust=False
    ).mean()

    rs = avg_gain / avg_loss

    df["RSI"] = 100 - (100 / (1 + rs))

    df.loc[
        (avg_loss == 0) & (avg_gain > 0),
        "RSI"
    ] = 100

    df.loc[
        (avg_loss == 0) & (avg_gain == 0),
        "RSI"
    ] = 50

    # MACD: 12-period EMA minus 26-period EMA
    ema_12 = df["Close"].ewm(
        span=12,
        adjust=False
    ).mean()

    ema_26 = df["Close"].ewm(
        span=26,
        adjust=False
    ).mean()

    df["MACD"] = ema_12 - ema_26

    df["Signal"] = df["MACD"].ewm(
        span=9,
        adjust=False
    ).mean()

    df["Histogram"] = df["MACD"] - df["Signal"]

    # ---------- Filter Chart Period ----------
    days = {
        "1 Month": 22,
        "3 Months": 66,
        "6 Months": 130,
        "Last 100 Trading Days": 100
    }[period]

    chart_df = df.tail(days).copy()

    # ---------- Candlestick Chart ----------
    st.subheader("Candlestick Analysis")
    st.caption(
        "Open • High • Low • Close • Trading Volume"
    )

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.06,
        row_heights=[0.72, 0.28],
        subplot_titles=(
            "Price Movement",
            "Trading Volume"
        )
    )

    fig.add_trace(
        go.Candlestick(
            x=chart_df.index,
            open=chart_df["Open"],
            high=chart_df["High"],
            low=chart_df["Low"],
            close=chart_df["Close"],
            name="OHLC",
            increasing_line_color="#22C55E",
            decreasing_line_color="#EF4444"
        ),
        row=1,
        col=1
    )

    # 7-day moving average
    if show_ma:
        ma7 = chart_df["Close"].rolling(
            window=7,
            min_periods=7
        ).mean()

        fig.add_trace(
            go.Scatter(
                x=chart_df.index,
                y=ma7,
                mode="lines",
                name="7-Day Average",
                line=dict(
                    color="#38BDF8",
                    width=2
                )
            ),
            row=1,
            col=1
        )

    # Volume bar colors
    volume_colors = [
        "#22C55E" if close >= open_price else "#EF4444"
        for open_price, close
        in zip(chart_df["Open"], chart_df["Close"])
    ]

    fig.add_trace(
        go.Bar(
            x=chart_df.index,
            y=chart_df["Volume"],
            name="Volume",
            marker_color=volume_colors
        ),
        row=2,
        col=1
    )

    fig.update_layout(
        height=650,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F1F5F9"),
        xaxis_rangeslider_visible=False,
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        ),
        margin=dict(
            l=10,
            r=10,
            t=60,
            b=10
        )
    )

    fig.update_yaxes(
        title_text="Price (USD)",
        row=1,
        col=1
    )

    fig.update_yaxes(
        title_text="Volume",
        row=2,
        col=1
    )

    with st.container(border=True):
        st.plotly_chart(
            fig,
            width="stretch",
            config={"displaylogo": False}
        )

    # ---------- RSI Indicator ----------
    st.subheader("RSI Indicator")
    st.caption("14-period Relative Strength Index")

    rsi_df = chart_df[["RSI"]].dropna()

    rsi_fig = go.Figure()

    rsi_fig.add_trace(
        go.Scatter(
            x=rsi_df.index,
            y=rsi_df["RSI"],
            mode="lines",
            name="RSI",
            line=dict(
                color="#38BDF8",
                width=2
            )
        )
    )

    rsi_fig.add_hline(
        y=70,
        line_dash="dash",
        line_color="#EF4444",
        annotation_text="Overbought (70)"
    )

    rsi_fig.add_hline(
        y=30,
        line_dash="dash",
        line_color="#22C55E",
        annotation_text="Oversold (30)"
    )

    rsi_fig.update_layout(
        template="plotly_dark",
        height=300,
        yaxis=dict(
            title="RSI",
            range=[0, 100]
        ),
        xaxis_title="Date",
        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20
        ),
        showlegend=False
    )

    with st.container(border=True):
        st.plotly_chart(
            rsi_fig,
            width="stretch",
            config={"displaylogo": False}
        )

    if not rsi_df.empty:
        latest_rsi = float(rsi_df["RSI"].iloc[-1])

        st.metric(
            "Latest RSI",
            f"{latest_rsi:.2f}"
        )

        if latest_rsi >= 70:
            st.warning(
                "RSI is in the overbought zone. "
                "This alone is not a sell signal."
            )
        elif latest_rsi <= 30:
            st.info(
                "RSI is in the oversold zone. "
                "This alone is not a buy signal."
            )
        else:
            st.success(
                "RSI is in the middle range."
            )
    else:
        st.info(
            "Not enough historical data is available to calculate RSI."
        )

    # ---------- MACD Indicator ----------
    st.subheader("MACD Indicator")
    st.caption("Trend and momentum analysis")

    macd_fig = go.Figure()

    macd_fig.add_trace(
        go.Scatter(
            x=chart_df.index,
            y=chart_df["MACD"],
            mode="lines",
            name="MACD",
            line=dict(
                color="#38BDF8",
                width=2
            )
        )
    )

    macd_fig.add_trace(
        go.Scatter(
            x=chart_df.index,
            y=chart_df["Signal"],
            mode="lines",
            name="Signal",
            line=dict(
                color="#F59E0B",
                width=2
            )
        )
    )

    histogram_colors = [
        "#22C55E" if value >= 0 else "#EF4444"
        for value in chart_df["Histogram"]
    ]

    macd_fig.add_trace(
        go.Bar(
            x=chart_df.index,
            y=chart_df["Histogram"],
            name="Histogram",
            marker_color=histogram_colors
        )
    )

    macd_fig.add_hline(
        y=0,
        line_dash="dash"
    )

    macd_fig.update_layout(
        template="plotly_dark",
        height=350,
        xaxis_title="Date",
        yaxis_title="MACD Value",
        margin=dict(
            l=20,
            r=20,
            t=40,
            b=20
        ),
        legend=dict(
            orientation="h",
            y=1.12
        )
    )

    with st.container(border=True):
        st.plotly_chart(
            macd_fig,
            width="stretch",
            config={"displaylogo": False}
        )

    latest_macd = float(chart_df["MACD"].iloc[-1])
    latest_signal = float(chart_df["Signal"].iloc[-1])

    macd_col1, macd_col2 = st.columns(2)

    with macd_col1:
        st.metric(
            "Latest MACD",
            f"{latest_macd:.3f}"
        )

    with macd_col2:
        st.metric(
            "Signal Line",
            f"{latest_signal:.3f}"
        )

    # ---------- Detailed Data ----------
    tab1, tab2 = st.tabs(
        ["📋 Historical Data", "📊 Statistics"]
    )

    with tab1:
        display_df = chart_df.sort_index(
            ascending=False
        ).copy()

        display_df.index = display_df.index.strftime(
            "%d %b %Y"
        )
        display_df.index.name = "Date"

        st.dataframe(
            display_df[
                [
                    "Open",
                    "High",
                    "Low",
                    "Close",
                    "Volume",
                    "RSI",
                    "MACD",
                    "Signal",
                    "Histogram"
                ]
            ].round(3),
            width="stretch"
        )

        csv = chart_df.to_csv().encode("utf-8")

        st.download_button(
            "⬇️ Download CSV",
            data=csv,
            file_name=f"{symbol}_stock_data.csv",
            mime="text/csv"
        )

    with tab2:
        s1, s2, s3 = st.columns(3)

        s1.metric(
            "Period High",
            f"${chart_df['High'].max():,.2f}"
        )

        s2.metric(
            "Period Low",
            f"${chart_df['Low'].min():,.2f}"
        )

        s3.metric(
            "Average Close",
            f"${chart_df['Close'].mean():,.2f}"
        )

    st.divider()

    st.caption(
        "MarketPulse • Built with Python, Pandas, "
        "Plotly and Streamlit."
    )

    st.caption(
        "Prices are shown in USD. Data availability and delays "
        "depend on the API provider. This is not financial advice."
    )

except Exception as error:
    st.error("Unable to load stock data.")
    st.info(
        "Check your API key, internet connection, "
        "stock symbol and API usage limits."
    )

    with st.expander("Technical details"):
        st.code(str(error))
