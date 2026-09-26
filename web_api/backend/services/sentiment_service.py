"""
Sentiment Analysis Service
===========================
Provides crypto sentiment analysis using Ollama LLM and real-time news.

Combines technical predictions with news sentiment for enhanced trading recommendations.
"""

import os
import json
import requests
from typing import Dict, Any, List
from datetime import datetime

class SentimentService:
    """Service for crypto sentiment analysis using Ollama"""
    
    def __init__(self, ollama_url: str = "http://localhost:11434/api/generate", 
                 ollama_model: str = "llama3.2"):
        """
        Initialize sentiment service
        
        Args:
            ollama_url: Ollama API endpoint
            ollama_model: Model name to use
        """
        self.ollama_url = ollama_url
        self.ollama_model = ollama_model
        self.news_cache = {}  # Cache news by crypto
        
    def _call_ollama(self, prompt: str, timeout: int = 60) -> str:
        """Call Ollama API"""
        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": self.ollama_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "num_predict": 2000
                    }
                },
                timeout=timeout
            )
            response.raise_for_status()
            return response.json().get("response", "")
        except Exception as e:
            raise Exception(f"Ollama API error: {str(e)}")
    
    def _fetch_news(self, crypto_name: str) -> List[Dict[str, str]]:
        """Fetch recent crypto news"""
        # Check cache first
        if crypto_name in self.news_cache:
            return self.news_cache[crypto_name]
        
        try:
            url = f"https://min-api.cryptocompare.com/data/v2/news/?lang=EN&categories={crypto_name}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            articles = []
            
            if 'Data' in data:
                for article in data['Data'][:10]:
                    articles.append({
                        'title': article.get('title', ''),
                        'body': article.get('body', '')[:500],
                        'source': article.get('source', ''),
                        'published': article.get('published_on', 0)
                    })
            
            # Cache the results
            self.news_cache[crypto_name] = articles
            return articles
            
        except Exception as e:
            print(f"News fetch error: {str(e)}")
            return []
    
    def _analyze_sentiment(self, crypto_name: str, articles: List[Dict[str, str]]) -> Dict[str, Any]:
        """Analyze sentiment using Ollama"""
        if not articles:
            return {
                'sentiment': 'NEUTRAL',
                'score': 0,
                'confidence': 0.5,
                'key_factors': [],
                'reasoning': 'No news articles available'
            }
        
        # Prepare news summary
        news_summary = "\n\n".join([
            f"Article {i+1}:\nTitle: {a['title']}\nSummary: {a['body'][:200]}"
            for i, a in enumerate(articles[:5])
        ])
        
        prompt = f"""You are a crypto market sentiment analyst. Analyze the following recent news about {crypto_name} and provide a sentiment assessment.

News Articles:
{news_summary}

Provide your analysis in the following JSON format:
{{
    "sentiment": "BULLISH" or "BEARISH" or "NEUTRAL",
    "score": <number between -100 (very bearish) and +100 (very bullish)>,
    "confidence": <number between 0 and 1>,
    "key_factors": ["factor1", "factor2", "factor3"],
    "reasoning": "Brief explanation of your sentiment assessment"
}}

Consider:
- Regulatory news
- Adoption/partnerships
- Technical developments
- Market trends
- Expert opinions

Return ONLY valid JSON, no additional text."""
        
        try:
            response_text = self._call_ollama(prompt)
            
            # Remove markdown code blocks if present
            response_text = response_text.strip()
            if '```json' in response_text:
                # Extract JSON from markdown code block
                start = response_text.find('```json') + 7
                end = response_text.find('```', start)
                response_text = response_text[start:end].strip()
            elif response_text.startswith('```'):
                # Remove any code block markers
                lines = response_text.split('\n')
                response_text = '\n'.join(lines[1:-1] if len(lines) > 2 else lines)
            
            # Try to find JSON object if there's extra text
            if not response_text.startswith('{'):
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}')
                if start_idx != -1 and end_idx != -1:
                    response_text = response_text[start_idx:end_idx+1]
            
            # Parse JSON
            sentiment_data = json.loads(response_text)
            
            # Ensure all required fields exist
            if 'sentiment' not in sentiment_data:
                sentiment_data['sentiment'] = 'NEUTRAL'
            if 'score' not in sentiment_data:
                sentiment_data['score'] = 0
            if 'confidence' not in sentiment_data:
                sentiment_data['confidence'] = 0.5
            if 'key_factors' not in sentiment_data:
                sentiment_data['key_factors'] = []
            if 'reasoning' not in sentiment_data:
                sentiment_data['reasoning'] = 'No reasoning provided'
                
            return sentiment_data
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {str(e)}")
            print(f"Response text: {response_text[:500]}")
            return {
                'sentiment': 'NEUTRAL',
                'score': 0,
                'confidence': 0.3,
                'key_factors': ['Unable to parse AI response'],
                'reasoning': 'AI response could not be parsed as valid JSON'
            }
        except Exception as e:
            print(f"Sentiment analysis error: {str(e)}")
            return {
                'sentiment': 'NEUTRAL',
                'score': 0,
                'confidence': 0.3,
                'key_factors': [],
                'reasoning': f'Error in analysis: {str(e)}'
            }
    
    def _combine_signals(self, technical_pred: Dict[str, Any], sentiment: Dict[str, Any]) -> Dict[str, Any]:
        """Combine technical and sentiment signals"""
        # Normalize technical signal to score
        tech_signal = technical_pred.get('signal', 'HOLD').upper()
        tech_pct = technical_pred.get('pct_change', 0)
        
        # Technical score: -100 to +100
        if tech_signal == 'STRONG BUY':
            tech_score = min(100, 80 + (tech_pct * 4))
        elif tech_signal == 'BUY':
            tech_score = min(80, 40 + (tech_pct * 4))
        elif tech_signal == 'SELL':
            tech_score = max(-80, -40 + (tech_pct * 4))
        elif tech_signal == 'STRONG SELL':
            tech_score = max(-100, -80 + (tech_pct * 4))
        else:  # HOLD
            tech_score = tech_pct * 4
        
        sentiment_score = sentiment.get('score', 0)
        
        # Weighted combination: 60% technical, 40% sentiment
        combined_score = (tech_score * 0.6) + (sentiment_score * 0.4)
        
        # Check signal alignment
        tech_direction = 1 if tech_score > 0 else -1 if tech_score < 0 else 0
        sentiment_direction = 1 if sentiment_score > 0 else -1 if sentiment_score < 0 else 0
        aligned = (tech_direction == sentiment_direction) or (tech_direction == 0) or (sentiment_direction == 0)
        
        return {
            'technical_score': tech_score,
            'sentiment_score': sentiment_score,
            'combined_score': combined_score,
            'signals_aligned': aligned,
            'tech_weight': 0.6,
            'sentiment_weight': 0.4
        }
    
    def _generate_recommendation(self, combined: Dict[str, Any], technical: Dict[str, Any], 
                                 sentiment: Dict[str, Any]) -> Dict[str, Any]:
        """Generate final trading recommendation"""
        score = combined['combined_score']
        aligned = combined['signals_aligned']
        
        # Determine action based on score and alignment
        if aligned:
            if score > 60:
                action = "STRONG BUY"
                confidence = 0.95
            elif score > 30:
                action = "BUY"
                confidence = 0.75
            elif score < -60:
                action = "STRONG SELL"
                confidence = 0.95
            elif score < -30:
                action = "SELL"
                confidence = 0.75
            else:
                action = "HOLD"
                confidence = 0.6
        else:
            # Conflicting signals - reduce confidence
            if abs(score) > 40:
                action = "BUY" if score > 0 else "SELL"
                confidence = 0.5
            else:
                action = "HOLD"
                confidence = 0.4
        
        # Generate reasoning using Ollama
        reasoning_prompt = f"""Provide a brief trading recommendation summary (2-3 sentences) based on:

Technical Analysis:
- Signal: {technical.get('signal')}
- Price Change: {technical.get('pct_change', 0):.2f}%
- RSI: {technical.get('rsi', 50):.1f}

Sentiment Analysis:
- Sentiment: {sentiment.get('sentiment')}
- Score: {sentiment.get('score', 0)}
- Key Factors: {sentiment.get('key_factors', [])}

Combined Decision: {action}
Signals Aligned: {aligned}

Provide clear, actionable reasoning for a trader."""
        
        try:
            reasoning = self._call_ollama(reasoning_prompt)
        except:
            reasoning = f"Combined analysis suggests {action} with {confidence:.0%} confidence."
        
        return {
            'action': action,
            'confidence': confidence,
            'aligned': aligned,
            'reasoning': reasoning.strip(),
            'timestamp': datetime.now().isoformat()
        }
    
    def analyze_crypto(self, crypto_name: str, technical_prediction: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run full sentiment analysis for a cryptocurrency
        
        Args:
            crypto_name: Name of cryptocurrency (e.g., 'Bitcoin', 'Ethereum')
            technical_prediction: Dict with technical analysis data
            
        Returns:
            Dict containing sentiment analysis and combined recommendation
        """
        # Fetch news
        articles = self._fetch_news(crypto_name)
        
        # Analyze sentiment
        sentiment = self._analyze_sentiment(crypto_name, articles)
        
        # Combine signals
        combined = self._combine_signals(technical_prediction, sentiment)
        
        # Generate recommendation
        recommendation = self._generate_recommendation(combined, technical_prediction, sentiment)
        
        return {
            'crypto': crypto_name,
            'technical': technical_prediction,
            'sentiment': sentiment,
            'combined_signal': combined,
            'recommendation': recommendation,
            'news_count': len(articles),
            'timestamp': datetime.now().isoformat()
        }
    
    def clear_cache(self):
        """Clear the news cache"""
        self.news_cache.clear()
