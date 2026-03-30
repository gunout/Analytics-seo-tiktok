# utils/visualizations.py
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime

class TikTokVisualizations:
    """Génère les visualisations interactives"""
    
    @staticmethod
    def engagement_gauge(engagement_rate):
        """Jauge d'engagement"""
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=engagement_rate,
            title={'text': "Taux d'engagement (%)", 'font': {'size': 24}},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 20], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "#667eea", 'thickness': 0.3},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 2,
                'bordercolor': "#764ba2",
                'steps': [
                    {'range': [0, 5], 'color': "rgba(255, 99, 132, 0.3)"},
                    {'range': [5, 10], 'color': "rgba(255, 206, 86, 0.3)"},
                    {'range': [10, 20], 'color': "rgba(75, 192, 192, 0.3)"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': engagement_rate
                }
            }
        ))
        fig.update_layout(height=350, margin=dict(l=20, r=20, t=50, b=20))
        return fig
    
    @staticmethod
    def performance_over_time(videos_df):
        """Graphique des performances dans le temps"""
        if videos_df.empty:
            return None
        
        df_copy = videos_df.copy()
        df_copy['date'] = pd.to_datetime(df_copy['create_time'], unit='s')
        df_copy = df_copy.sort_values('date')
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(x=df_copy['date'], y=df_copy['play_count'], 
                      name="Vues", line=dict(color="#667eea", width=2),
                      mode='lines+markers'),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(x=df_copy['date'], y=df_copy['digg_count'], 
                      name="Likes", line=dict(color="#48bb78", width=2),
                      mode='lines+markers'),
            secondary_y=True
        )
        
        fig.update_xaxes(title_text="Date")
        fig.update_yaxes(title_text="Nombre de vues", secondary_y=False)
        fig.update_yaxes(title_text="Nombre de likes", secondary_y=True)
        fig.update_layout(
            title="Évolution des performances",
            height=400,
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        return fig
    
    @staticmethod
    def hashtag_bar_chart(top_hashtags):
        """Bar chart des top hashtags"""
        if not top_hashtags:
            return None
        
        hashtags, counts = zip(*top_hashtags[:8])
        
        fig = go.Figure(go.Bar(
            x=list(counts),
            y=list(hashtags),
            orientation='h',
            marker=dict(
                color=counts,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Fréquence")
            ),
            text=list(counts),
            textposition='outside'
        ))
        
        fig.update_layout(
            title="Top hashtags utilisés",
            xaxis_title="Nombre d'utilisations",
            yaxis_title="Hashtags",
            height=400,
            margin=dict(l=100)
        )
        
        return fig
    
    @staticmethod
    def sentiment_pie_chart(sentiment_distribution):
        """Camembert des sentiments"""
        if not sentiment_distribution:
            return None
        
        labels = ['Positif 😊', 'Neutre 😐', 'Négatif 😔']
        values = [
            sentiment_distribution.get('positive', 0),
            sentiment_distribution.get('neutral', 0),
            sentiment_distribution.get('negative', 0)
        ]
        colors = ['#48bb78', '#ecc94b', '#f56565']
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker=dict(colors=colors),
            textinfo='label+percent',
            textposition='auto'
        )])
        
        fig.update_layout(
            title="Distribution des sentiments",
            height=350,
            annotations=[dict(text="Sentiment", x=0.5, y=0.5, font_size=20, showarrow=False)]
        )
        
        return fig
    
    @staticmethod
    def posting_hours_chart(posting_times):
        """Graphique des meilleurs horaires"""
        if not posting_times:
            return None
        
        hours = [h['hour'] for h in posting_times]
        scores = [h['score'] for h in posting_times]
        
        fig = go.Figure(go.Bar(
            x=hours,
            y=scores,
            marker_color='#667eea',
            text=[f"{s}%" for s in scores],
            textposition='auto'
        ))
        
        fig.update_layout(
            title="Scores de performance par horaire",
            xaxis_title="Heure de la journée",
            yaxis_title="Score de performance (%)",
            height=350,
            xaxis=dict(tickmode='linear', tick0=0, dtick=2)
        )
        
        return fig
    
    @staticmethod
    def engagement_breakdown(metrics):
        """Breakdown des métriques d'engagement"""
        categories = ['Likes', 'Commentaires', 'Partages']
        values = [
            metrics.get('total_likes', 0),
            metrics.get('total_comments', 0),
            metrics.get('total_shares', 0)
        ]
        colors = ['#667eea', '#48bb78', '#fbbf24']
        
        fig = go.Figure(data=[go.Pie(
            labels=categories,
            values=values,
            marker=dict(colors=colors),
            textinfo='label+percent',
            textposition='auto'
        )])
        
        fig.update_layout(
            title="Répartition de l'engagement total",
            height=350
        )
        
        return fig
    
    @staticmethod
    def virality_gauge(virality_score):
        """Jauge de viralité"""
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=virality_score,
            title={'text': "Score de viralité", 'font': {'size': 20}},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#f59e0b"},
                'steps': [
                    {'range': [0, 30], 'color': "rgba(239, 68, 68, 0.3)"},
                    {'range': [30, 60], 'color': "rgba(245, 158, 11, 0.3)"},
                    {'range': [60, 100], 'color': "rgba(16, 185, 129, 0.3)"}
                ]
            }
        ))
        fig.update_layout(height=300)
        return fig

# Import pour make_subplots
from plotly.subplots import make_subplots