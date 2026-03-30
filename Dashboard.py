import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import asyncio
from TikTokApi import TikTokApi
from datetime import datetime, timedelta
import hashlib
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page Streamlit
st.set_page_config(
    page_title="TikTok IA Analytics Pro",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styles CSS personnalisés
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea20 0%, #764ba220 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #667eea;
    }
    .insight-box {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Cache pour éviter de re-scraper trop souvent
@st.cache_data(ttl=3600)  # Cache de 1 heure
def get_tiktok_data(username):
    """Récupère les données TikTok réelles"""
    try:
        # Nettoyer le username
        username = username.strip().replace('@', '')
        
        # Exécuter l'async
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def fetch_data():
            async with TikTokApi() as api:
                # Note: Ajoutez votre ms_token ici si nécessaire
                # await api.create_sessions(ms_tokens=[ms_token], num_sessions=1)
                await api.create_sessions(num_sessions=1, headless=True)
                
                user = api.user(username)
                user_info = await user.info()
                user_stats = user_info.get('stats', {})
                user_detail = user_info.get('user', {})
                
                # Récupérer les vidéos
                videos = []
                async for video in user.videos(count=30):
                    video_data = {
                        'id': video.id,
                        'desc': video.description,
                        'create_time': video.create_time,
                        'play_count': video.stats['play_count'],
                        'digg_count': video.stats['digg_count'],
                        'comment_count': video.stats['comment_count'],
                        'share_count': video.stats['share_count'],
                        'hashtags': video.hashtags if hasattr(video, 'hashtags') else []
                    }
                    videos.append(video_data)
                
                return {
                    'profile': {
                        'username': username,
                        'nickname': user_detail.get('nickname', ''),
                        'bio': user_detail.get('bio', ''),
                        'avatar': user_detail.get('avatarThumb', ''),
                        'verified': user_detail.get('verified', False),
                        'followers': user_stats.get('followerCount', 0),
                        'following': user_stats.get('followingCount', 0),
                        'hearts': user_stats.get('heartCount', 0),
                        'videos': user_stats.get('videoCount', 0)
                    },
                    'videos': videos
                }
        
        data = loop.run_until_complete(fetch_data())
        loop.close()
        return data
        
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données: {str(e)}")
        return None

# Fonctions d'analyse IA
class TikTokIAInsights:
    def __init__(self, profile_data, videos_data):
        self.profile = profile_data
        self.videos = videos_data
        self.df = pd.DataFrame(videos_data)
        
    def calculate_engagement_metrics(self):
        """Calcule les métriques d'engagement avancées"""
        if self.df.empty:
            return {}
        
        total_engagement = (self.df['digg_count'] + self.df['comment_count'] + self.df['share_count']).sum()
        avg_engagement = total_engagement / len(self.df)
        
        engagement_rate = 0
        if self.profile['followers'] > 0:
            engagement_rate = (avg_engagement / self.profile['followers']) * 100
        
        # Calculer le taux de conversion vues → likes
        view_to_like = (self.df['digg_count'].sum() / self.df['play_count'].sum() * 100) if self.df['play_count'].sum() > 0 else 0
        
        # Score de viralité
        viral_scores = []
        for _, video in self.df.iterrows():
            if video['play_count'] > 0:
                viral_score = (video['digg_count'] + video['comment_count']*2 + video['share_count']*3) / video['play_count']
                viral_scores.append(viral_score)
        
        return {
            'total_engagement': int(total_engagement),
            'avg_engagement': int(avg_engagement),
            'engagement_rate': round(engagement_rate, 2),
            'view_to_like_rate': round(view_to_like, 2),
            'virality_score': round(np.mean(viral_scores) * 100, 2) if viral_scores else 0,
            'best_performing_video': self.df.loc[self.df['play_count'].idxmax()] if not self.df.empty else None
        }
    
    def analyze_content_sentiment(self):
        """Analyse de sentiment IA sur les descriptions"""
        if self.df.empty:
            return {}
        
        sentiments = []
        for desc in self.df['desc']:
            if desc and desc.strip():
                blob = TextBlob(desc)
                sentiments.append({
                    'polarity': blob.sentiment.polarity,
                    'subjectivity': blob.sentiment.subjectivity
                })
            else:
                sentiments.append({'polarity': 0, 'subjectivity': 0})
        
        avg_polarity = np.mean([s['polarity'] for s in sentiments])
        avg_subjectivity = np.mean([s['subjectivity'] for s in sentiments])
        
        # Classification du ton
        if avg_polarity > 0.3:
            tone = "Très positif 😊"
        elif avg_polarity > 0:
            tone = "Légèrement positif 🙂"
        elif avg_polarity > -0.3:
            tone = "Neutre 😐"
        else:
            tone = "Négatif 😔"
        
        return {
            'avg_polarity': round(avg_polarity, 3),
            'avg_subjectivity': round(avg_subjectivity, 3),
            'tone': tone,
            'sentiments': sentiments
        }
    
    def extract_hashtag_insights(self):
        """Analyse avancée des hashtags"""
        all_hashtags = []
        hashtag_performance = {}
        
        for _, video in self.df.iterrows():
            for tag in video['hashtags']:
                all_hashtags.append(tag.lower())
                if tag not in hashtag_performance:
                    hashtag_performance[tag] = {'count': 0, 'total_views': 0, 'total_likes': 0}
                hashtag_performance[tag]['count'] += 1
                hashtag_performance[tag]['total_views'] += video['play_count']
                hashtag_performance[tag]['total_likes'] += video['digg_count']
        
        # Fréquence des hashtags
        hashtag_counts = Counter(all_hashtags)
        top_hashtags = hashtag_counts.most_common(10)
        
        # Performance moyenne par hashtag
        hashtag_avg_perf = {}
        for tag, perf in hashtag_performance.items():
            if perf['count'] > 0:
                hashtag_avg_perf[tag] = {
                    'avg_views': perf['total_views'] / perf['count'],
                    'avg_likes': perf['total_likes'] / perf['count']
                }
        
        return {
            'top_hashtags': top_hashtags,
            'total_unique_hashtags': len(hashtag_counts),
            'avg_hashtags_per_video': len(all_hashtags) / len(self.df) if not self.df.empty else 0,
            'hashtag_performance': hashtag_avg_perf
        }
    
    def predict_best_posting_time(self):
        """Prédit les meilleurs horaires de publication avec IA"""
        if self.df.empty:
            return []
        
        # Convertir les timestamps
        posting_hours = []
        performance_by_hour = {}
        
        for _, video in self.df.iterrows():
            if video['create_time']:
                dt = datetime.fromtimestamp(video['create_time'])
                hour = dt.hour
                posting_hours.append(hour)
                
                if hour not in performance_by_hour:
                    performance_by_hour[hour] = {'views': [], 'engagement': []}
                
                performance_by_hour[hour]['views'].append(video['play_count'])
                performance_by_hour[hour]['engagement'].append(
                    video['digg_count'] + video['comment_count'] + video['share_count']
                )
        
        # Calculer les scores moyens par heure
        hour_scores = []
        for hour in range(24):
            if hour in performance_by_hour:
                avg_views = np.mean(performance_by_hour[hour]['views'])
                avg_engagement = np.mean(performance_by_hour[hour]['engagement'])
                # Score normalisé
                score = (avg_views / (max(performance_by_hour[hour]['views']) + 1)) * 0.6 + \
                        (avg_engagement / (max(performance_by_hour[hour]['engagement']) + 1)) * 0.4
                hour_scores.append((hour, score))
            else:
                hour_scores.append((hour, 0))
        
        # Top 3 meilleures heures
        best_hours = sorted(hour_scores, key=lambda x: x[1], reverse=True)[:3]
        
        return [{'hour': h, 'score': round(s*100, 1)} for h, s in best_hours if s > 0]
    
    def generate_ai_recommendations(self, metrics, sentiment, hashtags, posting_times):
        """Génère des recommandations IA personnalisées"""
        recommendations = []
        
        # Recommandations basées sur l'engagement
        if metrics['engagement_rate'] < 3:
            recommendations.append({
                'priority': 'Haute',
                'category': 'Engagement',
                'insight': '⚠️ Taux d\'engagement faible',
                'action': 'Ajoutez des calls-to-action dans vos vidéos et répondez aux commentaires dans l\'heure suivant la publication',
                'expected_impact': '+150% d\'engagement en 2 semaines'
            })
        elif metrics['engagement_rate'] > 10:
            recommendations.append({
                'priority': 'Moyenne',
                'category': 'Engagement',
                'insight': '✅ Excellent engagement !',
                'action': 'Capitalisez sur ce momentum en publiant plus fréquemment et en faisant des duos avec des créateurs similaires',
                'expected_impact': 'Accélération de la croissance'
            })
        
        # Recommandations basées sur le sentiment
        if sentiment['avg_polarity'] < 0:
            recommendations.append({
                'priority': 'Moyenne',
                'category': 'Sentiment',
                'insight': '📊 Contenu perçu négativement',
                'action': 'Essayez un ton plus positif et éducatif. Évitez les controverses inutiles',
                'expected_impact': 'Amélioration de l\'image de marque'
            })
        
        # Recommandations hashtags
        if hashtags['avg_hashtags_per_video'] < 3:
            recommendations.append({
                'priority': 'Haute',
                'category': 'SEO',
                'insight': '🏷️ Utilisation insuffisante de hashtags',
                'action': 'Utilisez 3-5 hashtags spécifiques + 2-3 hashtags tendance par vidéo',
                'expected_impact': '+200% de visibilité sur les recherches'
            })
        
        # Recommandations timing
        if posting_times:
            best_hour = posting_times[0]['hour']
            recommendations.append({
                'priority': 'Moyenne',
                'category': 'Timing',
                'insight': f'⏰ Meilleur horaire: {best_hour}h',
                'action': f'Programmez vos publications entre {best_hour-1}h et {best_hour+1}h pour maximiser la portée',
                'expected_impact': '+50% de vues initiales'
            })
        
        # Recommandation générale IA
        recommendations.append({
            'priority': 'Basse',
            'category': 'Stratégie',
            'insight': '🎯 Analyse des tendances',
            'action': 'Utilisez les sons tendance du moment et créez des séries éducatives pour booster l\'algorithme',
            'expected_impact': 'Croissance organique accélérée'
        })
        
        return recommendations
    
    def create_advanced_analytics(self):
        """Crée des analyses avancées avec visualisations"""
        metrics = self.calculate_engagement_metrics()
        sentiment = self.analyze_content_sentiment()
        hashtags = self.extract_hashtag_insights()
        posting_times = self.predict_best_posting_time()
        recommendations = self.generate_ai_recommendations(metrics, sentiment, hashtags, posting_times)
        
        # Score IA global
        ia_score = 0
        if metrics['engagement_rate'] > 5:
            ia_score += 30
        if sentiment['avg_polarity'] > 0.2:
            ia_score += 25
        if hashtags['avg_hashtags_per_video'] >= 5:
            ia_score += 25
        if posting_times:
            ia_score += 20
        
        return {
            'metrics': metrics,
            'sentiment': sentiment,
            'hashtags': hashtags,
            'posting_times': posting_times,
            'recommendations': recommendations,
            'ia_score': ia_score,
            'ia_grade': 'A+' if ia_score > 80 else 'A' if ia_score > 70 else 'B+' if ia_score > 60 else 'B' if ia_score > 50 else 'C'
        }

# Interface Streamlit
def main():
    # En-tête
    st.markdown("""
    <div class="main-header">
        <h1>🎵 TikTok IA Analytics Pro</h1>
        <p style="font-size: 1.2rem;">Analyses avancées & Insights IA pour optimiser votre présence TikTok</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100?text=TikTok+IA", use_container_width=False)
        st.markdown("## 🎯 Configuration")
        
        username = st.text_input("Nom d'utilisateur TikTok", value="@khaby.lame", help="Entrez @username ou lien TikTok")
        
        st.markdown("---")
        st.markdown("### 🤖 Fonctionnalités IA")
        st.markdown("""
        - ✅ Analyse de sentiment NLP
        - ✅ Prédiction des meilleurs horaires
        - ✅ Score de viralité IA
        - ✅ Recommandations personnalisées
        - ✅ Analyse des hashtags intelligente
        """)
        
        st.markdown("---")
        st.markdown("### 📊 Données")
        st.markdown("Données **réelles** TikTok via API")
        
        analyze_btn = st.button("🚀 Lancer l'analyse IA", type="primary", use_container_width=True)
    
    # Zone principale
    if analyze_btn and username:
        with st.spinner("🔄 Analyse IA en cours... Récupération des données réelles TikTok"):
            # Récupérer les données
            data = get_tiktok_data(username)
            
            if data and data['videos']:
                # Initialiser l'analyse IA
                ia = TikTokIAInsights(data['profile'], data['videos'])
                insights = ia.create_advanced_analytics()
                
                # Afficher le profil
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <h2>{data['profile']['nickname'] or data['profile']['username']}</h2>
                        <p>@{data['profile']['username']}</p>
                        <p>{data['profile']['bio'][:150]}...</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Métriques principales
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("👥 Abonnés", f"{data['profile']['followers']:,}", delta=None)
                with col2:
                    st.metric("❤️ Total likes", f"{data['profile']['hearts']:,}", delta=None)
                with col3:
                    st.metric("🎬 Vidéos", data['profile']['videos'])
                with col4:
                    st.metric("🤖 Score IA", f"{insights['ia_score']}/100", delta=insights['ia_grade'])
                
                st.markdown("---")
                
                # Graphiques avancés
                st.markdown("## 📈 Analyses IA Avancées")
                
                tab1, tab2, tab3, tab4 = st.tabs(["🎯 Engagement IA", "🧠 Analyse Sentiment", "🏷️ Hashtags SEO", "💡 Recommandations"])
                
                with tab1:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Métriques d'engagement
                        fig = go.Figure(go.Indicator(
                            mode = "gauge+number+delta",
                            value = insights['metrics']['engagement_rate'],
                            title = {'text': "Taux d'engagement (%)"},
                            domain = {'x': [0, 1], 'y': [0, 1]},
                            gauge = {
                                'axis': {'range': [None, 20]},
                                'bar': {'color': "#667eea"},
                                'steps': [
                                    {'range': [0, 5], 'color': "lightgray"},
                                    {'range': [5, 10], 'color': "gray"}
                                ],
                                'threshold': {
                                    'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75,
                                    'value': 90
                                }
                            }
                        ))
                        fig.update_layout(height=300)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h4>📊 Métriques IA</h4>
                            <p><strong>Score de viralité:</strong> {insights['metrics']['virality_score']}/100</p>
                            <p><strong>Taux vues → likes:</strong> {insights['metrics']['view_to_like_rate']}%</p>
                            <p><strong>Engagement total:</strong> {insights['metrics']['total_engagement']:,}</p>
                            <p><strong>Meilleure vidéo:</strong> {insights['metrics']['best_performing_video']['play_count']:,} vues</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                with tab2:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Analyse de sentiment
                        fig = go.Figure(data=[
                            go.Bar(name='Polarité', x=['Score'], y=[insights['sentiment']['avg_polarity']], marker_color='#667eea'),
                            go.Bar(name='Subjectivité', x=['Score'], y=[insights['sentiment']['avg_subjectivity']], marker_color='#764ba2')
                        ])
                        fig.update_layout(title="Analyse NLP du contenu", height=400)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h4>🧠 Insights Sentiment</h4>
                            <p><strong>Ton général:</strong> {insights['sentiment']['tone']}</p>
                            <p><strong>Polarité moyenne:</strong> {insights['sentiment']['avg_polarity']}</p>
                            <p><strong>Subjectivité:</strong> {insights['sentiment']['avg_subjectivity']}</p>
                            <p><em>La polarité positive indique un contenu apprécié, la subjectivité montre l'opinion personnelle</em></p>
                        </div>
                        """, unsafe_allow_html=True)
                
                with tab3:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Top hashtags
                        if insights['hashtags']['top_hashtags']:
                            top_hashtags_df = pd.DataFrame(
                                insights['hashtags']['top_hashtags'][:8],
                                columns=['Hashtag', 'Fréquence']
                            )
                            fig = px.bar(top_hashtags_df, x='Fréquence', y='Hashtag', orientation='h', title="Top Hashtags Utilisés")
                            fig.update_layout(height=400)
                            st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h4>🏷️ Statistiques Hashtags</h4>
                            <p><strong>Hashtags uniques:</strong> {insights['hashtags']['total_unique_hashtags']}</p>
                            <p><strong>Moyenne par vidéo:</strong> {insights['hashtags']['avg_hashtags_per_video']:.1f}</p>
                            <p><strong>Recommandation:</strong> {'✅ Bonne utilisation' if insights['hashtags']['avg_hashtags_per_video'] >= 3 else '⚠️ Ajoutez plus de hashtags'}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Heatmap des performances hashtags
                    if insights['hashtags']['hashtag_performance']:
                        perf_data = []
                        for tag, perf in list(insights['hashtags']['hashtag_performance'].items())[:10]:
                            perf_data.append({
                                'Hashtag': tag,
                                'Vues moyennes': perf['avg_views'],
                                'Likes moyens': perf['avg_likes']
                            })
                        perf_df = pd.DataFrame(perf_data)
                        st.dataframe(perf_df, use_container_width=True)
                
                with tab4:
                    st.markdown("## 💡 Recommandations IA Personnalisées")
                    
                    for rec in insights['recommendations']:
                        with st.expander(f"{rec['category']} - Priorité {rec['priority']}"):
                            st.markdown(f"""
                            **🔍 Insight:** {rec['insight']}  
                            **🎯 Action recommandée:** {rec['action']}  
                            **📈 Impact attendu:** {rec['expected_impact']}
                            """)
                
                # Meilleurs horaires
                if insights['posting_times']:
                    st.markdown("## ⏰ Prédiction des Meilleurs Horaires")
                    cols = st.columns(len(insights['posting_times']))
                    for idx, time in enumerate(insights['posting_times']):
                        with cols[idx]:
                            st.metric(f"🕐 {time['hour']}h", f"Score {time['score']}%", delta="Optimal" if idx == 0 else None)
                
                # Footer
                st.markdown("---")
                st.markdown("""
                <div style="text-align: center; color: gray;">
                    <p>🤖 Analyse IA basée sur les données réelles TikTok | Modèles NLP & Machine Learning</p>
                    <p>Dernière mise à jour: {}</p>
                </div>
                """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)
                
            else:
                st.error("❌ Impossible de récupérer les données. Vérifiez le nom d'utilisateur ou réessayez plus tard.")
    
    elif analyze_btn and not username:
        st.warning("⚠️ Veuillez entrer un nom d'utilisateur TikTok")

if __name__ == "__main__":
    main()