# app.py - Version corrigée
import streamlit as st
import pandas as pd
from datetime import datetime
import json

from utils.data_simulator import TikTokDataSimulator
from utils.ia_insights import TikTokIAInsights
from utils.visualizations import TikTokVisualizations

# Configuration de la page
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
        color: white;
        box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1);
    }
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.95;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        padding: 1.2rem;
        border-radius: 1rem;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    .metric-card h4 {
        margin: 0 0 0.5rem 0;
        color: #667eea;
    }
    .metric-card .value {
        font-size: 1.8rem;
        font-weight: bold;
        margin: 0;
    }
    .badge-success {
        background: #48bb78;
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-block;
    }
    .badge-warning {
        background: #f6ad55;
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-block;
    }
    .badge-danger {
        background: #f56565;
        color: white;
        padding: 0.2rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        display: inline-block;
    }
    .footer {
        text-align: center;
        color: #888;
        font-size: 0.8rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🎯 Configuration")
    
    username = st.text_input(
        "Nom d'utilisateur TikTok",
        value="@khaby.lame",
        help="Entrez @username ou directement le nom d'utilisateur"
    )
    
    st.markdown("---")
    
    st.markdown("## 🤖 Fonctionnalités IA")
    st.markdown("""
    - ✅ Analyse de sentiment NLP
    - ✅ Prédiction des meilleurs horaires
    - ✅ Score de viralité IA
    - ✅ Recommandations personnalisées
    - ✅ Analyse des hashtags SEO
    - ✅ Visualisations interactives
    """)
    
    st.markdown("---")
    
    st.markdown("## 📊 Type de données")
    st.info("🔬 **Mode démonstration** : Données simulées réalistes")
    
    st.markdown("---")
    
    export_btn = st.button("📥 Exporter les résultats", use_container_width=True)

# Header principal
st.markdown("""
<div class="main-header">
    <h1>🎵 TikTok IA Analytics Pro</h1>
    <p>Analyses avancées, insights IA et recommandations personnalisées</p>
</div>
""", unsafe_allow_html=True)

# Bouton d'analyse
analyze_btn = st.button("🚀 LANCER L'ANALYSE IA", type="primary", use_container_width=True)

if analyze_btn and username:
    with st.spinner("🔄 Analyse IA en cours... Génération des données et calculs..."):
        
        # 1. Générer les données
        simulator = TikTokDataSimulator(username)
        data = simulator.get_all_data()
        
        profile = data['profile']
        videos_df = data['videos_df']
        
        # 2. Analyser avec IA
        ia = TikTokIAInsights(profile, videos_df)
        insights = ia.get_all_insights()
        
        # 3. Visualisations
        viz = TikTokVisualizations()
        
        # --- AFFICHAGE DU PROFIL ---
        st.markdown("## 📱 Profil TikTok")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            verified_badge = 'badge-success' if profile['verified'] else 'badge-warning'
            verified_text = '✓ Vérifié' if profile['verified'] else 'Non vérifié'
            st.markdown(f"""
            <div style="text-align: center;">
                <h2>{profile['nickname']}</h2>
                <p style="font-size: 1.2rem;">@{profile['username']}</p>
                <p>{profile['bio']}</p>
                <p>
                    <span class="{verified_badge}">{verified_text}</span>
                    <span style="margin-left: 0.5rem;">🎯 Niche : {profile['niche']}</span>
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # --- MÉTRIQUES PRINCIPALES ---
        st.markdown("## 📊 Métriques Globales")
        
        metrics = insights['metrics']
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("👥 Abonnés", f"{profile['followers']:,}")
        with col2:
            st.metric("❤️ Total likes", f"{profile['hearts']:,}")
        with col3:
            st.metric("🎬 Vidéos", profile['videos'])
        with col4:
            st.metric("🤖 Score IA", f"{insights['ia_score']}/100", delta=insights['ia_grade'])
        
        # --- DASHBOARD IA PRINCIPAL ---
        st.markdown("## 📈 Dashboard IA Avancé")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🎯 Engagement", "🧠 Sentiment IA", "🏷️ Hashtags SEO", 
            "⏰ Timing Optimal", "💡 Recommandations"
        ])
        
        # Tab 1 : Engagement
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                fig_gauge = viz.engagement_gauge(metrics['engagement_rate'])
                st.plotly_chart(fig_gauge, use_container_width=True)
                
                fig_virality = viz.virality_gauge(metrics['virality_score'])
                st.plotly_chart(fig_virality, use_container_width=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>📊 Métriques détaillées</h4>
                    <p><strong>Total vues :</strong> {metrics['total_views']:,}</p>
                    <p><strong>Total likes :</strong> {metrics['total_likes']:,}</p>
                    <p><strong>Total commentaires :</strong> {metrics['total_comments']:,}</p>
                    <p><strong>Total partages :</strong> {metrics['total_shares']:,}</p>
                    <hr>
                    <p><strong>Vues moyennes :</strong> {metrics['avg_views']:,}</p>
                    <p><strong>Likes moyens :</strong> {metrics['avg_likes']:,}</p>
                    <p><strong>Taux conversion vues → likes :</strong> {metrics['view_to_like_rate']}%</p>
                </div>
                """, unsafe_allow_html=True)
            
            fig_time = viz.performance_over_time(videos_df)
            if fig_time:
                st.plotly_chart(fig_time, use_container_width=True)
        
        # Tab 2 : Sentiment IA
        with tab2:
            sentiment = insights['sentiment']
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig_sentiment = viz.sentiment_pie_chart(sentiment['sentiment_distribution'])
                if fig_sentiment:
                    st.plotly_chart(fig_sentiment, use_container_width=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>🧠 Analyse NLP</h4>
                    <p><strong>Ton général :</strong> {sentiment['tone']}</p>
                    <p><strong>Polarité moyenne :</strong> {sentiment['avg_polarity']}</p>
                    <p><strong>Subjectivité :</strong> {sentiment['avg_subjectivity']}</p>
                    <p><strong>Écart-type polarité :</strong> {sentiment['polarity_std']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.info("""
                **🔍 Interprétation :**
                - **Polarité > 0** : contenu positif/apprécié
                - **Polarité < 0** : contenu négatif/critiqué
                - **Subjectivité élevée** : opinions personnelles fortes
                """)
        
        # Tab 3 : Hashtags SEO
        with tab3:
            hashtags = insights['hashtags']
            
            col1, col2 = st.columns(2)
            
            with col1:
                if hashtags['top_hashtags']:
                    fig_hashtags = viz.hashtag_bar_chart(hashtags['top_hashtags'])
                    if fig_hashtags:
                        st.plotly_chart(fig_hashtags, use_container_width=True)
                else:
                    st.info("Aucun hashtag détecté")
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>🏷️ Statistiques hashtags</h4>
                    <p><strong>Score SEO hashtags :</strong> {hashtags['seo_score']}/100</p>
                    <p><strong>Hashtags uniques :</strong> {hashtags['total_unique_hashtags']}</p>
                    <p><strong>Moyenne par vidéo :</strong> {hashtags['avg_hashtags_per_video']:.1f}</p>
                    <p><strong>Recommandation :</strong> {hashtags['recommendation']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            if hashtags['hashtag_performance']:
                st.markdown("### 📈 Performance par hashtag")
                perf_data = []
                for tag, perf in list(hashtags['hashtag_performance'].items())[:8]:
                    perf_data.append({
                        'Hashtag': f"#{tag}",
                        'Vues moyennes': f"{perf['avg_views']:,.0f}",
                        'Likes moyens': f"{perf['avg_likes']:,.0f}"
                    })
                st.dataframe(pd.DataFrame(perf_data), use_container_width=True)
        
        # Tab 4 : Timing Optimal
        with tab4:
            posting_times = insights['posting_times']
            
            if posting_times:
                fig_hours = viz.posting_hours_chart(posting_times)
                if fig_hours:
                    st.plotly_chart(fig_hours, use_container_width=True)
                
                st.markdown("### ⏰ Top 3 meilleurs horaires")
                cols = st.columns(3)
                for idx, time in enumerate(posting_times[:3]):
                    with cols[idx]:
                        st.metric(
                            f"🕐 {time['hour']}:00 - {time['hour']+1}:00",
                            f"Score {time['score']}%",
                            delta=f"{time['count']} vidéos analysées"
                        )
                
                st.info("💡 **Conseil IA** : Programmez vos publications dans ces créneaux pour maximiser l'engagement initial.")
            else:
                st.warning("Pas assez de données pour prédire les meilleurs horaires")
        
        # Tab 5 : Recommandations
        with tab5:
            recommendations = insights['recommendations']
            
            if recommendations:
                for rec in recommendations:
                    with st.expander(f"{rec['category']} - Priorité {rec['priority']}"):
                        st.markdown(f"""
                        **🔍 Insight IA :** {rec['insight']}  
                        
                        **🎯 Action recommandée :**  
                        {rec['action']}  
                        
                        **📈 Impact attendu :** {rec['expected_impact']}
                        """)
            else:
                st.success("🎉 Félicitations ! Pas de recommandations critiques. Votre stratégie est optimale.")
            
            st.markdown("---")
            st.markdown("### 📋 Résumé stratégique IA")
            
            summary = f"""
            **Score IA global :** {insights['ia_score']}/100 ({insights['ia_grade']})
            
            **Forces identifiées :**
            - Engagement rate : {metrics['engagement_rate']}%
            - Sentiment : {sentiment['tone']}
            - SEO hashtags : {hashtags['seo_score']}/100
            
            **Points d'attention :**
            - Score viralité : {metrics['virality_score']}/100
            - Moyenne hashtags/vidéo : {hashtags['avg_hashtags_per_video']:.1f}
            """
            st.info(summary)
        
        # --- ANALYSE DE L'ENGAGEMENT (section supplémentaire) ---
        st.markdown("## 🎯 Analyse de l'engagement")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_breakdown = viz.engagement_breakdown(metrics)
            if fig_breakdown:
                st.plotly_chart(fig_breakdown, use_container_width=True)
        
        with col2:
            # Calcul de l'engagement moyen si non présent
            avg_engagement = metrics.get('total_engagement', 0)
            if metrics.get('videos_count', 0) > 0:
                avg_engagement = metrics['total_engagement'] // metrics['videos_count']
            
            st.markdown(f"""
            <div class="metric-card">
                <h4>📊 Ratios de performance</h4>
                <p><strong>Likes / vues :</strong> {metrics['view_to_like_rate']}%</p>
                <p><strong>Commentaires / vues :</strong> {metrics['view_to_comment_rate']}%</p>
                <p><strong>Partages / vues :</strong> {metrics['view_to_share_rate']}%</p>
                <hr>
                <p><strong>Engagement moyen / vidéo :</strong> {avg_engagement:,}</p>
                <p><strong>Vidéos analysées :</strong> {metrics['videos_count']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # --- EXPORT DES DONNÉES ---
        if export_btn:
            export_data = {
                'profile': profile,
                'insights': {
                    'metrics': metrics,
                    'sentiment': sentiment,
                    'hashtags': {
                        'top_hashtags': hashtags['top_hashtags'],
                        'total_unique_hashtags': hashtags['total_unique_hashtags'],
                        'avg_hashtags_per_video': hashtags['avg_hashtags_per_video'],
                        'seo_score': hashtags['seo_score']
                    },
                    'posting_times': posting_times,
                    'recommendations': recommendations,
                    'ia_score': insights['ia_score'],
                    'ia_grade': insights['ia_grade']
                },
                'videos': videos_df.to_dict('records'),
                'export_date': datetime.now().isoformat()
            }
            
            json_str = json.dumps(export_data, indent=2, default=str)
            
            st.download_button(
                label="📥 Télécharger l'analyse complète (JSON)",
                data=json_str,
                file_name=f"tiktok_analysis_{profile['username']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        # --- FOOTER ---
        st.markdown("---")
        st.markdown(f"""
        <div class="footer">
            <p>🤖 Analyse IA réalisée le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}</p>
            <p>📊 Données simulées basées sur le nom d'utilisateur | Version 2.0</p>
        </div>
        """, unsafe_allow_html=True)

elif analyze_btn and not username:
    st.warning("⚠️ Veuillez entrer un nom d'utilisateur TikTok")

else:
    st.info("👈 **Bienvenue dans TikTok IA Analytics Pro !** Entrez un nom d'utilisateur dans la barre latérale et cliquez sur 'LANCER L'ANALYSE IA'")
    
    st.markdown("""
    ### ✨ Fonctionnalités incluses
    
    | Fonctionnalité | Description |
    |----------------|-------------|
    | 🎯 **Analyse d'engagement** | Taux d'engagement, scores de viralité, tendances |
    | 🧠 **NLP & Sentiment** | Analyse du ton, polarité, subjectivité |
    | 🏷️ **SEO Hashtags** | Performance des hashtags, recommandations |
    | ⏰ **Timing optimal** | Prédiction des meilleurs créneaux horaires |
    | 💡 **Recommandations IA** | Actions personnalisées avec impacts estimés |
    | 📊 **Visualisations** | Graphiques interactifs et dashboards |
    | 📥 **Export JSON** | Sauvegarde complète des analyses |
    
    ---
    
    ### 🚀 Comment ça marche ?
    
    1. Entrez n'importe quel nom d'utilisateur TikTok (ex: @khaby.lame)
    2. Cliquez sur "LANCER L'ANALYSE IA"
    3. Explorez les 5 onglets d'analyse
    4. Obtenez des recommandations personnalisées
    """)