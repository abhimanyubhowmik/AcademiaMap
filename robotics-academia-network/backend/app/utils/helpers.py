import re
import math
from typing import Tuple, Optional
import pycountry
from geopy.geocoders import Nominatim
import logging

logger = logging.getLogger(__name__)


def extract_location_from_affiliation(affiliation: str) -> Tuple[Optional[str], Optional[str]]:
    """Extract university/institution and country from affiliation string"""
    if not affiliation:
        return None, None
    
    # Common patterns for extracting university and country
    university = None
    country = None
    
    try:
        # Split by comma and take parts
        parts = [part.strip() for part in affiliation.split(',')]
        
        if len(parts) >= 2:
            # Usually university is first, country is last
            university = parts[0]
            
            # Look for country in the last few parts
            for part in reversed(parts[-3:]):  # Check last 3 parts
                potential_country = clean_country_name(part)
                if is_valid_country(potential_country):
                    country = potential_country
                    break
        
        elif len(parts) == 1:
            # Try to extract from single string
            university = parts[0]
            
            # Look for country patterns
            country_patterns = [
                r'\b(USA|United States|US)\b',
                r'\b(UK|United Kingdom|Britain)\b',
                r'\b(Germany|Deutschland)\b',
                r'\b(China|PRC)\b',
                r'\b(Japan|日本)\b',
                r'\b(India|भारत)\b',
                r'\b(Canada)\b',
                r'\b(Australia)\b',
                r'\b(Singapore)\b',
                r'\b(South Korea|Korea)\b',
                r'\b(France|Francia)\b',
                r'\b(Italy|Italia)\b',
                r'\b(Spain|España)\b',
                r'\b(Netherlands|Holland)\b',
                r'\b(Switzerland|Schweiz)\b',
                r'\b(Sweden|Sverige)\b',
                r'\b(Norway|Norge)\b',
                r'\b(Denmark|Danmark)\b',
                r'\b(Finland|Suomi)\b',
                r'\b(Taiwan|ROC)\b',
                r'\b(Hong Kong|HK)\b',
                r'\b(New Zealand|NZ)\b',
            ]
            
            for pattern in country_patterns:
                match = re.search(pattern, affiliation, re.IGNORECASE)
                if match:
                    country = normalize_country_name(match.group(1))
                    break
    
    except Exception as e:
        logger.warning(f"Error extracting location from '{affiliation}': {e}")
    
    return university, country


def clean_country_name(name: str) -> str:
    """Clean and normalize country name"""
    if not name:
        return ""
    
    # Remove common suffixes and prefixes
    cleaned = re.sub(r'\b(University|Institute|College|School|Department|Dept)\b', '', name, flags=re.IGNORECASE)
    cleaned = re.sub(r'\b(of|the|and|&)\b', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'[^\w\s]', '', cleaned)  # Remove punctuation
    cleaned = cleaned.strip()
    
    return cleaned


def normalize_country_name(name: str) -> str:
    """Normalize country names to standard format"""
    name = name.strip()
    
    # Common mappings
    mappings = {
        'USA': 'United States',
        'US': 'United States',
        'UK': 'United Kingdom',
        'Britain': 'United Kingdom',
        'PRC': 'China',
        'ROC': 'Taiwan',
        'HK': 'Hong Kong',
        'NZ': 'New Zealand',
        'Korea': 'South Korea',
    }
    
    return mappings.get(name, name)


def is_valid_country(name: str) -> bool:
    """Check if a string represents a valid country"""
    if not name or len(name) < 2:
        return False
    
    try:
        # Check with pycountry
        if pycountry.countries.get(name=name):
            return True
        
        # Check common alternative names
        common_countries = {
            'United States', 'United Kingdom', 'Germany', 'France', 'Italy', 'Spain',
            'China', 'Japan', 'South Korea', 'India', 'Canada', 'Australia',
            'Netherlands', 'Switzerland', 'Sweden', 'Norway', 'Denmark', 'Finland',
            'Singapore', 'Taiwan', 'Hong Kong', 'New Zealand', 'Austria', 'Belgium'
        }
        
        return name in common_countries
    
    except Exception:
        return False


def calculate_rank_score(citations: int, h_index: int, i10_index: int) -> float:
    """Calculate a ranking score based on citation metrics"""
    if citations <= 0:
        return 0.0
    
    # Weighted scoring algorithm
    # Citations: 50% weight, h-index: 30% weight, i10-index: 20% weight
    
    # Normalize metrics (log scale for citations to reduce extreme values)
    normalized_citations = math.log10(max(1, citations)) / math.log10(100000)  # Max expected ~100k
    normalized_h_index = min(h_index / 150.0, 1.0)  # Max expected ~150
    normalized_i10_index = min(i10_index / 500.0, 1.0)  # Max expected ~500
    
    # Calculate weighted score
    score = (
        0.5 * normalized_citations +
        0.3 * normalized_h_index +
        0.2 * normalized_i10_index
    )
    
    # Scale to 0-100
    return round(score * 100, 2)


def determine_relationship_direction(researcher1: dict, researcher2: dict) -> str:
    """Determine the relationship direction between two researchers"""
    
    # Simple heuristic based on metrics
    score1 = calculate_rank_score(
        researcher1.get('citations', 0),
        researcher1.get('h_index', 0),
        researcher1.get('i10_index', 0)
    )
    
    score2 = calculate_rank_score(
        researcher2.get('citations', 0),
        researcher2.get('h_index', 0),
        researcher2.get('i10_index', 0)
    )
    
    # If significant difference, assume mentor-student relationship
    if score1 > score2 * 1.5:
        return "mentor_to_student"  # researcher1 -> researcher2
    elif score2 > score1 * 1.5:
        return "student_to_mentor"  # researcher1 -> researcher2 (but reversed semantically)
    else:
        return "peer"


def calculate_collaboration_strength(co_publications: int, total_pubs_1: int, total_pubs_2: int) -> float:
    """Calculate collaboration strength between two researchers"""
    if co_publications <= 0:
        return 0.0
    
    # Jaccard-like coefficient
    if total_pubs_1 > 0 and total_pubs_2 > 0:
        # Use harmonic mean of individual publication counts as denominator
        harmonic_mean = 2 * total_pubs_1 * total_pubs_2 / (total_pubs_1 + total_pubs_2)
        strength = co_publications / harmonic_mean
    else:
        # Fallback: simple ratio
        strength = co_publications / 10.0  # Assume average of 10 collaborations is "strong"
    
    return min(strength, 1.0)  # Cap at 1.0


def extract_university_from_affiliation(affiliation: str) -> Optional[str]:
    """Extract university name from affiliation string"""
    if not affiliation:
        return None
    
    # Patterns to identify university names
    university_patterns = [
        r'(.*?University.*?)(?:,|$)',
        r'(.*?Institute.*?)(?:,|$)',
        r'(.*?College.*?)(?:,|$)',
        r'(.*?School.*?)(?:,|$)',
        r'(MIT|Stanford|Harvard|Berkeley|CMU|Caltech|ETH|EPFL|NUS|NTU|Tsinghua|PKU)',
    ]
    
    for pattern in university_patterns:
        match = re.search(pattern, affiliation, re.IGNORECASE)
        if match:
            university = match.group(1).strip()
            # Clean up common prefixes/suffixes
            university = re.sub(r'^(The|A)\s+', '', university, flags=re.IGNORECASE)
            return university
    
    # Fallback: take first part before comma
    parts = affiliation.split(',')
    if parts:
        return parts[0].strip()
    
    return None


def format_researcher_name(name: str) -> str:
    """Format researcher name consistently"""
    if not name:
        return ""
    
    # Remove extra whitespace
    name = re.sub(r'\s+', ' ', name.strip())
    
    # Capitalize properly
    parts = name.split()
    formatted_parts = []
    
    for part in parts:
        # Handle common academic titles and suffixes
        if part.lower() in ['jr', 'sr', 'ii', 'iii', 'iv', 'phd', 'dr', 'prof', 'professor']:
            formatted_parts.append(part.upper() if part.lower() in ['jr', 'sr', 'ii', 'iii', 'iv'] else part.title())
        else:
            formatted_parts.append(part.title())
    
    return ' '.join(formatted_parts)


def is_academic_email(email: str) -> bool:
    """Check if an email address is likely academic"""
    if not email:
        return False
    
    academic_domains = [
        '.edu', '.ac.', '.university', '.univ', '.college',
        'mit.edu', 'stanford.edu', 'harvard.edu', 'berkeley.edu',
        'cmu.edu', 'caltech.edu', 'ethz.ch', 'epfl.ch'
    ]
    
    email_lower = email.lower()
    return any(domain in email_lower for domain in academic_domains)