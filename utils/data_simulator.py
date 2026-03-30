# utils/data_simulator.py
import hashlib
import random
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

class TikTokDataSimulator:
    """Générateur de données TikTok réalistes basé sur le nom d'utilisateur"""
    
    def __init__(self, username):
        self.username = username.replace('@', '').strip()
        self.seed = self._generate_seed()
        random.seed(self.seed)
        np.random.seed(self.seed)
        
    def _generate_seed(self):
        """Génère un seed unique basé sur le nom d'utilisateur"""
        return int(hashlib.md5(self.username.encode()).hexdigest()[:8], 16)
    
    def _get_niche(self):
        """Détermine la niche basée sur le username"""
        niches = [
            "Divertissement", "Éducation", "Beauté & Mode", 
            "Sport & Fitness", "Tech & Dev", "Business", 
            "Voyages", "Musique & Danse", "Cuisine", "Animaux"
        ]
        idx = self.seed % len(niches)
        return niches[idx]
    
    def get_profile(self):
        """Génère les données du profil"""
        base_followers = 1000 + (self.seed % 500000)
        
        # Variation réaliste
        followers = base_followers + int(base_followers * (random.random() - 0.5) * 0.3)
        
        return {
            'username': self.username,
            'nickname': f"Creator_{self.username[:10]}",
            'bio': self._generate_bio(),
            'avatar_url': f"https://picsum.photos/id/{self.seed % 100}/200/200",
            'verified': self.seed > 9000,
            'private': False,
            'followers': followers,
            'following': int(followers * (0.1 + random.random() * 0.3)),
            'hearts': int(followers * (5 + random.random() * 15)),
            'videos': 15 + (self.seed % 150),
            'niche': self._get_niche(),
            'join_date': datetime.now() - timedelta(days=180 + (self.seed % 1000))
        }
    
    def _generate_bio(self):
        """Génère une bio réaliste"""
        bios = [
            f"Créateur {self._get_niche().lower()} 🚀 | {self.seed % 1000}K+ 🎯",
            f"📸 {self._get_niche()} • Business: {self.username}@pro.com",
            f"✨ {self._get_niche()} content creator | Follow for more 🫶",
            f"🎵 {self._get_niche()} enthusiast | Tiktok marketing expert",
            f"💡 Astuces {self._get_niche().lower()} | Formation dispo 📚"
        ]
        return random.choice(bios)
    
    def get_videos(self, count=30):
        """Génère les données des vidéos"""
        videos = []
        base_views = 5000 + (self.seed % 200000)
        
        for i in range(min(count, self.get_profile()['videos'])):
            # Plus la vidéo est récente, plus elle a de vues (tendance naturelle)
            recency = 1 - (i / count)
            views = int(base_views * (0.3 + recency * 1.5) * (0.7 + random.random() * 0.6))
            
            engagement_rate = 0.02 + random.random() * 0.08
            likes = int(views * engagement_rate * random.uniform(0.7, 1.3))
            comments = int(likes * (0.05 + random.random() * 0.1))
            shares = int(likes * (0.03 + random.random() * 0.08))
            
            # Hashtags pertinents selon la niche
            hashtags = self._generate_hashtags(i)
            
            videos.append({
                'id': f"video_{i}_{self.seed}",
                'desc': self._generate_description(i),
                'create_time': (datetime.now() - timedelta(days=i * random.randint(1, 5))).timestamp(),
                'play_count': views,
                'digg_count': likes,
                'comment_count': comments,
                'share_count': shares,
                'hashtags': hashtags,
                'duration': random.randint(15, 60),
                'music': self._generate_music(),
                'is_ad': random.random() < 0.05
            })
        
        return videos
    
    def _generate_description(self, index):
        """Génère une description de vidéo"""
        descriptions = [
            f"✨ Nouvelle vidéo sur {self._get_niche()} ! Like et partage 🔥",
            f"📢 {self._get_niche()} tips que vous devez connaître 💡",
            f"🎯 Comment réussir dans {self._get_niche()} ? 🚀",
            f"🤯 Incroyable mais vrai ! #pourtoi #fyp",
            f"💪 Le secret des pros de {self._get_niche()}",
            f"🎬 C'est parti pour cette nouvelle aventure !",
            f"📚 Apprenez-en plus sur {self._get_niche()} aujourd'hui",
            f"🔥 La tendance du moment dans {self._get_niche()}"
        ]
        return random.choice(descriptions) + f" #{index+1}"
    
    def _generate_hashtags(self, index):
        """Génère des hashtags pertinents"""
        niche = self._get_niche().lower().replace(' & ', '').replace('é', 'e')
        
        base_tags = ['fyp', 'foryou', 'viral', 'tiktok', 'trending', 'pourtoi']
        niche_tags = {
            'divertissement': ['humour', 'funny', 'comedy', 'meme'],
            'education': ['learn', 'education', 'astuces', 'tutorial', 'apprendre'],
            'beaute mode': ['beauty', 'fashion', 'style', 'makeup', 'mode'],
            'sport fitness': ['fitness', 'workout', 'sport', 'gym', 'training'],
            'tech dev': ['tech', 'coding', 'dev', 'programming', 'ai'],
            'business': ['business', 'marketing', 'entrepreneur', 'money'],
            'voyages': ['travel', 'voyage', 'adventure', 'wanderlust'],
            'musique danse': ['music', 'dance', 'challenge', 'song'],
            'cuisine': ['food', 'cooking', 'recipe', 'cuisine'],
            'animaux': ['animals', 'pets', 'dog', 'cat', 'cute']
        }
        
        # Tags spécifiques à la niche
        specific_tags = []
        for key, tags in niche_tags.items():
            if key in niche:
                specific_tags = tags[:3]
                break
        
        if not specific_tags:
            specific_tags = ['content', 'creator', 'viral']
        
        # Mélanger et sélectionner
        all_tags = base_tags + specific_tags
        random.seed(self.seed + index)
        selected = random.sample(all_tags, min(5, len(all_tags)))
        
        return [f"#{tag}" for tag in selected]
    
    def _generate_music(self):
        """Génère un nom de musique aléatoire"""
        musics = [
            "Original Sound", "TikTok Trend Beat", "Viral Song 2024",
            "Popular Audio", "Trending Track", "Remix Version"
        ]
        return random.choice(musics)
    
    def get_all_data(self):
        """Retourne toutes les données"""
        profile = self.get_profile()
        videos = self.get_videos(profile['videos'])
        
        return {
            'profile': profile,
            'videos': videos,
            'videos_df': pd.DataFrame(videos),
            'analysis_date': datetime.now().isoformat()
        }