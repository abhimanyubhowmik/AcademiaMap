import asyncio
import time
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import logging

from scholarly import scholarly, ProxyGenerator
import requests
from bs4 import BeautifulSoup
import re

from ..core.config import settings
from ..utils.helpers import extract_location_from_affiliation, calculate_rank_score

logger = logging.getLogger(__name__)


class ScholarScraper:
    def __init__(self):
        self.rate_limit_delay = 60 / settings.SCHOLAR_RATE_LIMIT  # seconds between requests
        self.last_request_time = 0
        self.setup_proxy()
    
    def setup_proxy(self):
        """Setup proxy for scholarly to avoid rate limiting"""
        try:
            pg = ProxyGenerator()
            success = pg.FreeProxies()
            if success:
                scholarly.use_proxy(pg)
                logger.info("Proxy setup successful")
        except Exception as e:
            logger.warning(f"Proxy setup failed: {e}. Continuing without proxy.")
    
    async def rate_limit(self):
        """Implement rate limiting between requests"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.rate_limit_delay:
            await asyncio.sleep(self.rate_limit_delay - time_since_last)
        self.last_request_time = time.time()
    
    async def search_researchers_by_keywords(self, keywords: List[str], max_results: int = 100) -> List[Dict]:
        """Search for researchers based on keywords"""
        all_researchers = []
        
        for keyword in keywords:
            try:
                await self.rate_limit()
                logger.info(f"Searching for keyword: {keyword}")
                
                search_query = scholarly.search_author(keyword)
                count = 0
                
                for author in search_query:
                    if count >= max_results:
                        break
                    
                    try:
                        await self.rate_limit()
                        
                        # Fill author details
                        filled_author = scholarly.fill(author)
                        researcher_data = await self.extract_researcher_data(filled_author, [keyword])
                        
                        if researcher_data and researcher_data['citations'] >= settings.MIN_CITATIONS_THRESHOLD:
                            all_researchers.append(researcher_data)
                            count += 1
                            logger.info(f"Added researcher: {researcher_data['name']} (Citations: {researcher_data['citations']})")
                    
                    except Exception as e:
                        logger.error(f"Error processing author: {e}")
                        continue
                
            except Exception as e:
                logger.error(f"Error searching for keyword '{keyword}': {e}")
                continue
        
        return self.deduplicate_researchers(all_researchers)
    
    async def extract_researcher_data(self, author_data: Dict, keywords: List[str]) -> Optional[Dict]:
        """Extract relevant data from scholarly author object"""
        try:
            # Basic information
            name = author_data.get('name', '')
            if not name:
                return None
            
            scholar_id = author_data.get('scholar_id', '')
            affiliation = author_data.get('affiliation', '')
            email = author_data.get('email', '')
            homepage = author_data.get('homepage', '')
            
            # Citations and indices
            citations = author_data.get('citedby', 0)
            h_index = author_data.get('hindex', 0)
            i10_index = author_data.get('i10index', 0)
            
            # Interests
            interests = author_data.get('interests', [])
            
            # Photo URL
            photo_url = None
            if 'url_picture' in author_data:
                photo_url = author_data['url_picture']
            
            # Extract location information
            university, country = extract_location_from_affiliation(affiliation)
            region = self.determine_region(country)
            
            # Calculate rank score
            rank_score = calculate_rank_score(citations, h_index, i10_index)
            
            # Research categories based on interests and keywords
            research_categories = self.categorize_research_interests(interests, keywords)
            
            return {
                'scholar_id': scholar_id,
                'name': name,
                'affiliation': affiliation,
                'email': email,
                'university': university,
                'country': country,
                'region': region,
                'citations': citations,
                'h_index': h_index,
                'i10_index': i10_index,
                'rank_score': rank_score,
                'interests': interests,
                'photo_url': photo_url,
                'homepage': homepage,
                'research_categories': research_categories
            }
        
        except Exception as e:
            logger.error(f"Error extracting researcher data: {e}")
            return None
    
    def determine_region(self, country: str) -> str:
        """Determine the geographic region based on country"""
        if not country:
            return "Unknown"
        
        country = country.strip().title()
        
        # Check North America
        if country in settings.REGIONS["North America"]:
            return "North America"
        
        # Check Europe
        if country in settings.REGIONS["Europe"]:
            return "Europe"
        
        # Check Asia-Pacific regions
        asia_pacific = settings.REGIONS["Asia-Pacific"]
        for region, countries in asia_pacific.items():
            if country in countries:
                return region
        
        return "Other"
    
    def categorize_research_interests(self, interests: List[str], keywords: List[str]) -> List[str]:
        """Categorize research interests into predefined categories"""
        categories = []
        all_text = ' '.join(interests + keywords).lower()
        
        for category, category_keywords in settings.RESEARCH_CATEGORIES.items():
            for keyword in category_keywords:
                if keyword.lower() in all_text:
                    if category not in categories:
                        categories.append(category)
                    break
        
        return categories
    
    def deduplicate_researchers(self, researchers: List[Dict]) -> List[Dict]:
        """Remove duplicate researchers based on scholar_id and name"""
        seen_ids = set()
        seen_names = set()
        unique_researchers = []
        
        for researcher in researchers:
            scholar_id = researcher.get('scholar_id', '')
            name = researcher.get('name', '').lower().strip()
            
            # Skip if we've seen this scholar_id or very similar name
            if scholar_id and scholar_id in seen_ids:
                continue
            if name in seen_names:
                continue
            
            if scholar_id:
                seen_ids.add(scholar_id)
            seen_names.add(name)
            unique_researchers.append(researcher)
        
        return unique_researchers
    
    async def get_collaborators(self, researcher_data: Dict) -> List[Dict]:
        """Get collaborators for a specific researcher"""
        collaborators = []
        
        try:
            if not researcher_data.get('scholar_id'):
                return []
            
            await self.rate_limit()
            
            # Search for publications of this researcher
            publications = scholarly.search_pubs(f"author:{researcher_data['name']}")
            
            collaboration_counts = {}
            
            for pub in publications:
                try:
                    await self.rate_limit()
                    filled_pub = scholarly.fill(pub)
                    
                    if 'bib' in filled_pub and 'author' in filled_pub['bib']:
                        authors = filled_pub['bib']['author']
                        
                        for author in authors:
                            if author.lower() != researcher_data['name'].lower():
                                collaboration_counts[author] = collaboration_counts.get(author, 0) + 1
                
                except Exception as e:
                    logger.error(f"Error processing publication: {e}")
                    continue
            
            # Convert to collaborator format
            for collaborator_name, count in collaboration_counts.items():
                if count >= 2:  # Minimum 2 collaborations to be considered
                    collaborators.append({
                        'name': collaborator_name,
                        'collaboration_count': count
                    })
        
        except Exception as e:
            logger.error(f"Error getting collaborators for {researcher_data['name']}: {e}")
        
        return collaborators
    
    async def search_researchers_by_categories(self, categories: List[str]) -> List[Dict]:
        """Search researchers by research categories"""
        all_researchers = []
        
        for category in categories:
            if category in settings.RESEARCH_CATEGORIES:
                keywords = settings.RESEARCH_CATEGORIES[category]
                researchers = await self.search_researchers_by_keywords(keywords, 
                                                                      settings.MAX_RESULTS_PER_SEARCH)
                
                # Add category information
                for researcher in researchers:
                    if category not in researcher.get('research_categories', []):
                        researcher['research_categories'].append(category)
                
                all_researchers.extend(researchers)
        
        return self.deduplicate_researchers(all_researchers)