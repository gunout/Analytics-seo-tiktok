# utils/ia_insights.py
import numpy as np
import pandas as pd
from textblob import TextBlob
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class TikTokIAInsights:
    """Analyses IA avancées pour TikTok"""
    
    def __init__(self, profile, videos_df):
        self.profile = profile
        self.df = videos_df if not videos_df.empty else pd.DataFrame()
        
    def calculate_engagement_metrics(self):
        """Calcule les métriques d'engagement avancées"""
        if self.df.empty:
            return self._empty_metrics()
        
        total_views = self.df['play_count'].sum()
        total_likes = self.df['digg_count'].sum()
        total_comments = self.df['comment_count'].sum()
        total_shares = self.df['share_count'].sum()
        total_engagement = total_likes + total_comments + total_shares
        
        # Engagement rate
        if self.profile['followers'] > 0:
            avg_engagement_per_video = total_engagement / len(self.df)
            engagement_rate = (avg_engagement_per_video / self.profile['followers']) * 100
        else:
            engagement_rate = 0
        
        # Taux de conversion
        view_to_like = (total_likes / total_views * 100) if total_views > 0 else 0
        view_to_comment = (total_comments / total_views * 100) if total_views > 0 else 0
        view_to_share = (total_shares / total_views * 100) if total_views > 0 else 0
        
        # Score de viralité
        viral_scores = []
        for _, video in self.df.iterrows():
            if video['play_count'] > 0:
                score = (video['digg_count'] + video['comment_count']*2 + video['share_count']*3) / video['play_count']
                viral_scores.append(score)
        virality_score = np.mean(viral_scores) * 100 if viral_scores else 0
        
        # Meilleure vidéo
        best_video = self.df.loc[self.df['play_count'].idxmax()] if not self.df.empty else None
        
        return {
            'total_views': int(total_views),
            'total_likes': int(total_likes),
            'total_comments': int(total_comments),
            'total_shares': int(total_shares),
            'total_engagement': int(total_engagement),
            'avg_views': int(self.df['play_count'].mean()),
            'avg_likes': int(self.df['digg_count'].mean()),
            'avg_comments': int(self.df['comment_count'].mean()),
            'avg_shares': int(self.df['share_count'].mean()),
            'engagement_rate': round(engagement_rate, 2),
            'view_to_like_rate': round(view_to_like, 2),
            'view_to_comment_rate': round(view_to_comment, 2),
            'view_to_share_rate': round(view_to_share, 2),
            'virality_score': round(virality_score, 2),
            'best_video': best_video.to_dict() if best_video is not None else None,
            'videos_count': len(self.df)
        }
    
    def _empty_metrics(self):
        return {
            'total_views': 0, 'total_likes': 0, 'total_comments': 0,
            'total_shares': 0, 'total_engagement': 0, 'avg_views': 0,
            'avg_likes': 0, 'avg_comments': 0, 'avg_shares': 0,
            'engagement_rate': 0, 'view_to_like_rate': 0,
            'view_to_comment_rate': 0, 'view_to_share_rate': 0,
            'virality_score': 0, 'best_video': None, 'videos_count': 0
        }
    
    def analyze_sentiment(self):
        """Analyse de sentiment NLP sur les descriptions"""
        if self.df.empty or self.df['desc'].isna().all():
            return self._empty_sentiment()
        
        sentiments = []
        for desc in self.df['desc'].fillna(''):
            if desc:
                blob = TextBlob(desc)
                sentiments.append({
                    'polarity': blob.sentiment.polarity,
                    'subjectivity': blob.sentiment.subjectivity
                })
            else:
                sentiments.append({'polarity': 0, 'subjectivity': 0})
        
        polarities = [s['polarity'] for s in sentiments]
        subjectivities = [s['subjectivity'] for s in sentiments]
        
        avg_polarity = np.mean(polarities)
        avg_subjectivity = np.mean(subjectivities)
        
        # Classification
        if avg_polarity > 0.3:
            tone = "Très positif 😊"
            tone_emoji = "😊"
        elif avg_polarity > 0:
            tone = "Légèrement positif 🙂"
            tone_emoji = "🙂"
        elif avg_polarity > -0.3:
            tone = "Neutre 😐"
            tone_emoji = "😐"
        else:
            tone = "Négatif 😔"
            tone_emoji = "😔"
        
        return {
            'avg_polarity': round(avg_polarity, 3),
            'avg_subjectivity': round(avg_subjectivity, 3),
            'tone': tone,
            'tone_emoji': tone_emoji,
            'polarity_std': round(np.std(polarities), 3),
            'sentiment_distribution': {
                'positive': sum(1 for p in polarities if p > 0.1),
                'neutral': sum(1 for p in polarities if -0.1 <= p <= 0.1),
                'negative': sum(1 for p in polarities if p < -0.1)
            }
        }
    
    def _empty_sentiment(self):
        return {
            'avg_polarity': 0, 'avg_subjectivity': 0, 'tone': "Inconnu",
            'tone_emoji': "❓", 'polarity_std': 0,
            'sentiment_distribution': {'positive': 0, 'neutral': 0, 'negative': 0}
        }
    
    def analyze_hashtags(self):
        """Analyse avancée des hashtags"""
        if self.df.empty:
            return self._empty_hashtags()
        
        all_hashtags = []
        hashtag_performance = {}
        
        for _, video in self.df.iterrows():
            for tag in video.get('hashtags', []):
                tag_clean = tag.lower().replace('#', '')
                all_hashtags.append(tag_clean)
                
                if tag_clean not in hashtag_performance:
                    hashtag_performance[tag_clean] = {
                        'count': 0, 'total_views': 0, 'total_likes': 0,
                        'total_comments': 0, 'total_shares': 0
                    }
                
                hashtag_performance[tag_clean]['count'] += 1
                hashtag_performance[tag_clean]['total_views'] += video['play_count']
                hashtag_performance[tag_clean]['total_likes'] += video['digg_count']
                hashtag_performance[tag_clean]['total_comments'] += video['comment_count']
                hashtag_performance[tag_clean]['total_shares'] += video['share_count']
        
        # Fréquence
        hashtag_counts = Counter(all_hashtags)
        top_hashtags = hashtag_counts.most_common(10)
        
        # Performance moyenne par hashtag
        hashtag_avg_perf = {}
        for tag, perf in hashtag_performance.items():
            if perf['count'] > 0:
                hashtag_avg_perf[tag] = {
                    'avg_views': perf['total_views'] / perf['count'],
                    'avg_likes': perf['total_likes'] / perf['count'],
                    'avg_comments': perf['total_comments'] / perf['count'],
                    'avg_shares': perf['total_shares'] / perf['count']
                }
        
        # Score SEO hashtags
        optimal_count = 3 <= len(all_hashtags) / len(self.df) <= 5
        has_viral_tags = any(tag in ['fyp', 'foryou', 'viral', 'trending'] for tag in all_hashtags)
        
        seo_score = 0
        if optimal_count:
            seo_score += 40
        if has_viral_tags:
            seo_score += 30
        if len(hashtag_counts) > 10:
            seo_score += 30
        
        return {
            'top_hashtags': top_hashtags,
            'total_unique_hashtags': len(hashtag_counts),
            'avg_hashtags_per_video': len(all_hashtags) / len(self.df) if len(self.df) > 0 else 0,
            'hashtag_performance': hashtag_avg_perf,
            'seo_score': min(100, seo_score),
            'recommendation': self._hashtag_recommendation(optimal_count, has_viral_tags, len(hashtag_counts))
        }
    
    def _empty_hashtags(self):
        return {
            'top_hashtags': [], 'total_unique_hashtags': 0,
            'avg_hashtags_per_video': 0, 'hashtag_performance': {},
            'seo_score': 0, 'recommendation': "Aucune donnée"
        }
    
    def _hashtag_recommendation(self, optimal_count, has_viral_tags, unique_count):
        if not optimal_count:
            return "⚠️ Utilisez 3 à 5 hashtags par vidéo pour un SEO optimal"
        elif not has_viral_tags:
            return "📈 Ajoutez des hashtags viraux comme #fyp ou #foryou"
        elif unique_count < 10:
            return "💡 Diversifiez vos hashtags pour toucher plus de communautés"
        else:
            return "✅ Bonne stratégie de hashtags !"
    
    def predict_best_posting_times(self):
        """Prédit les meilleurs horaires avec IA"""
        if self.df.empty or 'create_time' not in self.df.columns:
            return []
        
        performance_by_hour = {h: {'views': [], 'engagement': []} for h in range(24)}
        
        for _, video in self.df.iterrows():
            if video['create_time']:
                dt = datetime.fromtimestamp(video['create_time'])
                hour = dt.hour
                
                performance_by_hour[hour]['views'].append(video['play_count'])
                performance_by_hour[hour]['engagement'].append(
                    video['digg_count'] + video['comment_count'] + video['share_count']
                )
        
        # Calculer les scores
        hour_scores = []
        max_views = max([max(v['views']) for v in performance_by_hour.values() if v['views']] or [1])
        max_engagement = max([max(v['engagement']) for v in performance_by_hour.values() if v['engagement']] or [1])
        
        for hour in range(24):
            views = performance_by_hour[hour]['views']
            engagement = performance_by_hour[hour]['engagement']
            
            if views:
                avg_views = np.mean(views)
                avg_engagement = np.mean(engagement)
                
                views_score = (avg_views / max_views) * 0.6 if max_views > 0 else 0
                engagement_score = (avg_engagement / max_engagement) * 0.4 if max_engagement > 0 else 0
                score = views_score + engagement_score
            else:
                score = 0
            
            hour_scores.append({'hour': hour, 'score': round(score * 100, 1), 'count': len(views)})
        
        # Top 3 meilleures heures
        best_hours = sorted(hour_scores, key=lambda x: x['score'], reverse=True)[:3]
        
        return [h for h in best_hours if h['score'] > 0]
    
    def generate_ai_recommendations(self, metrics, sentiment, hashtags, posting_times):
        """Génère des recommandations IA personnalisées"""
        recommendations = []
        
        # Recommandations engagement
        if metrics['engagement_rate'] < 3:
            recommendations.append({
                'priority': 'Haute',
                'category': '🎯 Engagement',
                'insight': f"Taux d'engagement de {metrics['engagement_rate']}% (faible)",
                'action': 'Répondez aux commentaires dans l\'heure, posez des questions dans vos vidéos',
                'expected_impact': '+150% d\'engagement en 2 semaines'
            })
        elif metrics['engagement_rate'] > 8:
            recommendations.append({
                'priority': 'Moyenne',
                'category': '🎯 Engagement',
                'insight': f"Excellent engagement ({metrics['engagement_rate']}%) !",
                'action': 'Capitalisez avec plus de contenu similaire et des duos avec d\'autres créateurs',
                'expected_impact': 'Accélération de la croissance'
            })
        
        # Recommandations sentiment
        if sentiment['avg_polarity'] < -0.1:
            recommendations.append({
                'priority': 'Haute',
                'category': '💬 Sentiment',
                'insight': 'Contenu perçu négativement par l\'audience',
                'action': 'Adoptez un ton plus positif et évitez les controverses',
                'expected_impact': 'Amélioration de l\'image de marque'
            })
        
        # Recommandations hashtags
        if hashtags['avg_hashtags_per_video'] < 3:
            recommendations.append({
                'priority': 'Haute',
                'category': '🏷️ SEO',
                'insight': 'Utilisation insuffisante de hashtags',
                'action': 'Ajoutez 3-5 hashtags spécifiques + 2-3 hashtags tendance par vidéo',
                'expected_impact': '+200% de visibilité organique'
            })
        
        # Recommandations timing
        if posting_times and posting_times[0]['score'] > 0:
            best_hour = posting_times[0]['hour']
            recommendations.append({
                'priority': 'Moyenne',
                'category': '⏰ Timing',
                'insight': f'Meilleur créneau détecté : {best_hour}h',
                'action': f'Programmez vos vidéos entre {best_hour-1}h et {best_hour+1}h',
                'expected_impact': '+50% de vues initiales'
            })
        
        # Recommandation générale IA
        if metrics['virality_score'] < 20:
            recommendations.append({
                'priority': 'Basse',
                'category': '🚀 Viralité',
                'insight': 'Score de viralité à améliorer',
                'action': 'Utilisez les sons tendance, créez des hooks accrocheurs (3 premières secondes)',
                'expected_impact': 'Potentiel viral x2'
            })
        
        # Ajouter une recommandation sur la fréquence
        if metrics['videos_count'] < 20:
            recommendations.append({
                'priority': 'Moyenne',
                'category': '📅 Fréquence',
                'insight': 'Peu de vidéos analysées',
                'action': 'Publiez au moins 3-4 fois par semaine pour nourrir l\'algorithme',
                'expected_impact': 'Meilleure reconnaissance'
            })
        
        return recommendations
    
    def calculate_ia_score(self, metrics, sentiment, hashtags):
        """Calcule un score IA global /100"""
        score = 0
        
        # Engagement (max 35 points)
        if metrics['engagement_rate'] >= 8:
            score += 35
        elif metrics['engagement_rate'] >= 5:
            score += 25
        elif metrics['engagement_rate'] >= 3:
            score += 15
        else:
            score += 5
        
        # Viralité (max 25 points)
        if metrics['virality_score'] >= 50:
            score += 25
        elif metrics['virality_score'] >= 30:
            score += 18
        elif metrics['virality_score'] >= 15:
            score += 10
        else:
            score += 5
        
        # Sentiment (max 20 points)
        if sentiment['avg_polarity'] > 0.3:
            score += 20
        elif sentiment['avg_polarity'] > 0:
            score += 12
        elif sentiment['avg_polarity'] > -0.2:
            score += 6
        else:
            score += 2
        
        # SEO hashtags (max 20 points)
        score += hashtags['seo_score'] * 0.2
        
        return min(100, round(score))
    
    def get_all_insights(self):
        """Retourne tous les insights IA"""
        metrics = self.calculate_engagement_metrics()
        sentiment = self.analyze_sentiment()
        hashtags = self.analyze_hashtags()
        posting_times = self.predict_best_posting_times()
        recommendations = self.generate_ai_recommendations(metrics, sentiment, hashtags, posting_times)
        ia_score = self.calculate_ia_score(metrics, sentiment, hashtags)
        
        # Grade
        if ia_score >= 85:
            grade = "A+ 🏆"
        elif ia_score >= 75:
            grade = "A 🌟"
        elif ia_score >= 65:
            grade = "B+ 📈"
        elif ia_score >= 55:
            grade = "B 👍"
        elif ia_score >= 45:
            grade = "C+ ⚠️"
        else:
            grade = "D 🚨"
        
        return {
            'metrics': metrics,
            'sentiment': sentiment,
            'hashtags': hashtags,
            'posting_times': posting_times,
            'recommendations': recommendations,
            'ia_score': ia_score,
            'ia_grade': grade,
            'profile': self.profile
        }