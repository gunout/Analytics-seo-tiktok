// server.js - Backend pour récupérer les VRAIES données TikTok
const express = require('express');
const axios = require('axios');
const cors = require('cors');
const cheerio = require('cheerio');

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());
app.use(express.static('.')); // Servir les fichiers statiques

// Fonction pour extraire les données réelles de TikTok
async function getRealTikTokData(username) {
    username = username.replace('@', '').trim().toLowerCase();
    
    try {
        // Méthode 1: API TikTok Oembed (publique)
        const oembedUrl = `https://www.tiktok.com/oembed?url=https://www.tiktok.com/@${username}`;
        const oembedResponse = await axios.get(oembedUrl, {
            headers: {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            },
            timeout: 10000
        });
        
        if (oembedResponse.data && oembedResponse.data.author_name) {
            // Méthode 2: Scraper la page pour les stats
            const pageUrl = `https://www.tiktok.com/@${username}`;
            const pageResponse = await axios.get(pageUrl, {
                headers: {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'fr,fr-FR;q=0.8,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1'
                },
                timeout: 15000
            });
            
            // Extraire les données du JSON intégré
            const html = pageResponse.data;
            const jsonMatch = html.match(/<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>([\s\S]*?)<\/script>/);
            
            let userStats = {
                followers: 0,
                following: 0,
                hearts: 0,
                videos: 0,
                bio: '',
                verified: false,
                nickname: oembedResponse.data.author_name || username
            };
            
            if (jsonMatch && jsonMatch[1]) {
                try {
                    const jsonData = JSON.parse(jsonMatch[1]);
                    const userInfo = jsonData?.__DEFAULT_SCOPE__?.['webapp.user-detail']?.userInfo;
                    
                    if (userInfo) {
                        const stats = userInfo.stats || {};
                        const user = userInfo.user || {};
                        
                        userStats = {
                            followers: stats.followerCount || 0,
                            following: stats.followingCount || 0,
                            hearts: stats.heartCount || 0,
                            videos: stats.videoCount || 0,
                            bio: user.signature || '',
                            verified: user.verified || false,
                            nickname: user.nickname || oembedResponse.data.author_name || username,
                            avatar: user.avatarThumb || '',
                            joinDate: user.createTime ? new Date(user.createTime * 1000).toISOString() : null
                        };
                    }
                } catch (e) {
                    console.log('Erreur parsing JSON:', e.message);
                }
            }
            
            // Calculer le taux d'engagement réel
            let engagementRate = 0;
            if (userStats.followers > 0) {
                // Estimation basée sur les dernières vidéos (si disponibles)
                engagementRate = (userStats.hearts / userStats.followers) * 100;
                engagementRate = Math.min(20, Math.max(0.1, engagementRate));
            }
            
            // Score SEO basé sur la bio et le nombre de vidéos
            let seoScore = 40;
            if (userStats.bio && userStats.bio.length > 50) seoScore += 20;
            else if (userStats.bio && userStats.bio.length > 20) seoScore += 10;
            if (userStats.videos > 50) seoScore += 20;
            else if (userStats.videos > 20) seoScore += 10;
            if (userStats.verified) seoScore += 15;
            seoScore = Math.min(98, seoScore);
            
            return {
                success: true,
                username: username,
                nickname: userStats.nickname,
                bio: userStats.bio || 'Aucune bio',
                verified: userStats.verified,
                followers: userStats.followers,
                following: userStats.following,
                hearts: userStats.hearts,
                videos: userStats.videos,
                engagementRate: engagementRate.toFixed(1),
                seoScore: seoScore,
                bioOptimization: Math.min(95, 30 + (userStats.bio?.length || 0) / 3),
                accountStrength: seoScore > 70 ? "Très fort" : (seoScore > 45 ? "Moyen" : "À optimiser"),
                avatar: userStats.avatar,
                joinDate: userStats.joinDate,
                source: 'real_tiktok_api'
            };
        }
        
        return { success: false, error: "Utilisateur non trouvé" };
        
    } catch (error) {
        console.error('Erreur:', error.message);
        return { 
            success: false, 
            error: "Impossible de récupérer les données. Vérifiez le nom d'utilisateur.",
            details: error.message 
        };
    }
}

// Endpoint API
app.get('/api/tiktok/:username', async (req, res) => {
    const username = req.params.username;
    console.log(`📊 Récupération des données réelles pour @${username}...`);
    
    const data = await getRealTikTokData(username);
    res.json(data);
});

// Endpoint de santé
app.get('/api/health', (req, res) => {
    res.json({ status: 'ok', message: 'TikTok Real Analytics API is running' });
});

// Démarrer le serveur
app.listen(PORT, () => {
    console.log(`
    ╔══════════════════════════════════════════════════╗
    ║     🎵 TikTok Real Analytics API - Démarrée      ║
    ╠══════════════════════════════════════════════════╣
    ║  🌐 Serveur: http://localhost:${PORT}              ║
    ║  📊 API: http://localhost:${PORT}/api/tiktok/@user ║
    ║  🧪 Test: http://localhost:${PORT}/api/health      ║
    ╚══════════════════════════════════════════════════╝
    `);
});