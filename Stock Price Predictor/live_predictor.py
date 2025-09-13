"""
Live Stock Price Predictor with Real-time Updates
Features live data streaming, real-time predictions, and interactive dashboards
"""

import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import time
import threading
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

from stock_predictor import StockPredictor
import config

class LiveStockPredictor(StockPredictor):
    """Enhanced Stock Predictor with live data capabilities"""
    
    def __init__(self, symbol='AAPL', period='2y', update_interval=30):
        super().__init__(symbol, period)
        self.update_interval = update_interval  # seconds
        self.live_data = None
        self.is_live = False
        self.last_update = None
        
    def get_live_data(self):
        """Get the most recent stock data"""
        try:
            ticker = yf.Ticker(self.symbol)
            # Get data for the last 5 days to ensure we have recent data
            live_data = ticker.history(period="5d", interval="1m")
            if len(live_data) > 0:
                self.live_data = live_data
                self.last_update = datetime.now()
                return True
        except Exception as e:
            print(f"Error fetching live data: {e}")
        return False
    
    def get_current_price(self):
        """Get current stock price"""
        if self.live_data is not None and len(self.live_data) > 0:
            return self.live_data['Close'].iloc[-1]
        return None
    
    def get_price_change(self):
        """Get current price change from previous close"""
        if self.live_data is not None and len(self.live_data) > 0:
            current = self.live_data['Close'].iloc[-1]
            previous = self.live_data['Close'].iloc[-2] if len(self.live_data) > 1 else current
            return ((current - previous) / previous) * 100
        return None
    
    def create_live_chart(self):
        """Create interactive live chart using Plotly"""
        if self.data is None:
            return go.Figure()
        
        # Create subplots
        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=(f'{self.symbol} Price Chart', 'Volume', 'RSI'),
            row_heights=[0.6, 0.2, 0.2]
        )
        
        # Price chart with moving averages
        fig.add_trace(
            go.Scatter(
                x=self.data.index,
                y=self.data['Close'],
                mode='lines',
                name='Close Price',
                line=dict(color='#1f77b4', width=2)
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=self.data.index,
                y=self.data['MA_5'],
                mode='lines',
                name='MA 5',
                line=dict(color='#ff7f0e', width=1),
                opacity=0.7
            ),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=self.data.index,
                y=self.data['MA_20'],
                mode='lines',
                name='MA 20',
                line=dict(color='#2ca02c', width=1),
                opacity=0.7
            ),
            row=1, col=1
        )
        
        # Volume chart
        colors = ['green' if close >= open else 'red' 
                 for close, open in zip(self.data['Close'], self.data['Open'])]
        
        fig.add_trace(
            go.Bar(
                x=self.data.index,
                y=self.data['Volume'],
                name='Volume',
                marker_color=colors,
                opacity=0.7
            ),
            row=2, col=1
        )
        
        # RSI chart
        fig.add_trace(
            go.Scatter(
                x=self.data.index,
                y=self.data['RSI'],
                mode='lines',
                name='RSI',
                line=dict(color='#9467bd', width=2)
            ),
            row=3, col=1
        )
        
        # Add RSI reference lines
        fig.add_hline(y=70, line_dash="dash", line_color="red", 
                     annotation_text="Overbought", row=3, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green", 
                     annotation_text="Oversold", row=3, col=1)
        
        # Update layout
        fig.update_layout(
            title=f'{self.symbol} Live Stock Analysis',
            height=800,
            showlegend=True,
            hovermode='x unified',
            template='plotly_white'
        )
        
        fig.update_xaxes(title_text="Date", row=3, col=1)
        fig.update_yaxes(title_text="Price ($)", row=1, col=1)
        fig.update_yaxes(title_text="Volume", row=2, col=1)
        fig.update_yaxes(title_text="RSI", row=3, col=1)
        
        return fig
    
    def get_live_prediction(self):
        """Get live prediction with current data"""
        if self.model is None:
            return None
        
        # Update with latest data
        self.get_live_data()
        
        if self.live_data is not None and len(self.live_data) > 0:
            # Use the latest features for prediction
            latest_features = self.features.iloc[-1:].values
            prediction = self.model.predict(latest_features)[0]
            prediction_proba = self.model.predict_proba(latest_features)[0]
            
            direction = "UP" if prediction == 1 else "DOWN"
            confidence = max(prediction_proba) * 100
            
            return {
                'direction': direction,
                'confidence': confidence,
                'prediction': prediction,
                'probabilities': prediction_proba,
                'current_price': self.get_current_price(),
                'price_change': self.get_price_change(),
                'last_update': self.last_update
            }
        return None

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Live Stock Price Predictor"

# App layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("📈 Live Stock Price Predictor", 
                   className="text-center mb-4", 
                   style={'color': '#2c3e50'}),
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Controls", className="card-title"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Stock Symbol:"),
                            dcc.Dropdown(
                                id='symbol-dropdown',
                                options=[{'label': stock, 'value': stock} 
                                        for stock in config.POPULAR_STOCKS],
                                value='AAPL',
                                clearable=False
                            )
                        ], width=6),
                        dbc.Col([
                            dbc.Label("Time Period:"),
                            dcc.Dropdown(
                                id='period-dropdown',
                                options=[{'label': desc, 'value': period} 
                                        for period, desc in config.TIME_PERIODS.items()],
                                value='2y',
                                clearable=False
                            )
                        ], width=6)
                    ], className="mb-3"),
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("🔄 Update Data", 
                                      id="update-button", 
                                      color="primary", 
                                      className="me-2"),
                            dbc.Button("🎯 Train Model", 
                                      id="train-button", 
                                      color="success", 
                                      className="me-2"),
                        ], width=12)
                    ])
                ])
            ])
        ], width=12)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Live Prediction", className="card-title"),
                    html.Div(id="prediction-display")
                ])
            ])
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Current Price", className="card-title"),
                    html.Div(id="price-display")
                ])
            ])
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Model Status", className="card-title"),
                    html.Div(id="model-status")
                ])
            ])
        ], width=4)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="live-chart")
        ], width=12)
    ]),
    
    # Auto-refresh component
    dcc.Interval(
        id='interval-component',
        interval=30*1000,  # Update every 30 seconds
        n_intervals=0
    ),
    
    # Store for predictor instance
    dcc.Store(id='predictor-store')
    
], fluid=True)

# Global predictor instance
predictor = None

@app.callback(
    Output('predictor-store', 'data'),
    [Input('symbol-dropdown', 'value'),
     Input('period-dropdown', 'value')]
)
def update_predictor(symbol, period):
    """Update predictor when symbol or period changes"""
    global predictor
    predictor = LiveStockPredictor(symbol=symbol, period=period)
    return {'symbol': symbol, 'period': period}

@app.callback(
    [Output('prediction-display', 'children'),
     Output('price-display', 'children'),
     Output('model-status', 'children'),
     Output('live-chart', 'figure')],
    [Input('update-button', 'n_clicks'),
     Input('train-button', 'n_clicks'),
     Input('interval-component', 'n_intervals')],
    [dash.dependencies.State('predictor-store', 'data')]
)
def update_dashboard(update_clicks, train_clicks, n_intervals, predictor_data):
    """Update dashboard components"""
    global predictor
    
    if predictor is None:
        return "No predictor", "No data", "Not initialized", go.Figure()
    
    # Update data if update button was clicked
    ctx = dash.callback_context
    if ctx.triggered:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if trigger_id == 'update-button':
            predictor.fetch_data()
            predictor.create_features()
        elif trigger_id == 'train-button':
            predictor.train_model()
    
    # Get live prediction
    prediction = predictor.get_live_prediction()
    
    # Prediction display
    if prediction:
        direction_color = "success" if prediction['direction'] == "UP" else "danger"
        prediction_display = dbc.Alert([
            html.H3(f"{prediction['direction']}", className="mb-0"),
            html.P(f"Confidence: {prediction['confidence']:.1f}%", className="mb-0")
        ], color=direction_color, className="text-center")
    else:
        prediction_display = dbc.Alert("No prediction available", color="warning")
    
    # Price display
    current_price = predictor.get_current_price()
    price_change = predictor.get_price_change()
    
    if current_price:
        change_color = "success" if price_change and price_change >= 0 else "danger"
        change_symbol = "📈" if price_change and price_change >= 0 else "📉"
        price_display = [
            html.H3(f"${current_price:.2f}", className="mb-1"),
            html.P(f"{change_symbol} {price_change:.2f}%" if price_change else "No change", 
                   className=f"text-{change_color} mb-0")
        ]
    else:
        price_display = dbc.Alert("No price data", color="warning")
    
    # Model status
    if predictor.model is not None:
        model_status = dbc.Alert("✅ Model Trained", color="success")
    else:
        model_status = dbc.Alert("❌ Model Not Trained", color="danger")
    
    # Chart
    chart_figure = predictor.create_live_chart()
    
    return prediction_display, price_display, model_status, chart_figure

def run_live_dashboard(host='127.0.0.1', port=8050, debug=True):
    """Run the live dashboard"""
    print("🚀 Starting Live Stock Price Predictor Dashboard...")
    print(f"📊 Dashboard will be available at: http://{host}:{port}")
    print("🔄 Auto-refresh every 30 seconds")
    print("⏹️  Press Ctrl+C to stop")
    
    app.run_server(host=host, port=port, debug=debug)

if __name__ == "__main__":
    run_live_dashboard()

