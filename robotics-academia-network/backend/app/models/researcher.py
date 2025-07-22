from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict
from datetime import datetime

Base = declarative_base()


class Researcher(Base):
    __tablename__ = "researchers"
    
    id = Column(Integer, primary_key=True, index=True)
    scholar_id = Column(String, unique=True, index=True)
    name = Column(String, nullable=False, index=True)
    affiliation = Column(String)
    email = Column(String)
    
    # Location Information
    university = Column(String)
    country = Column(String)
    region = Column(String)
    
    # Metrics
    citations = Column(Integer, default=0)
    h_index = Column(Integer, default=0)
    i10_index = Column(Integer, default=0)
    rank_score = Column(Float, default=0.0)  # Calculated ranking score
    
    # Profile Information
    photo_url = Column(String)
    interests = Column(JSON)  # List of research interests
    homepage = Column(String)
    
    # Metadata
    last_updated = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    is_verified = Column(Boolean, default=False)
    
    # Research Categories (which keywords they match)
    research_categories = Column(JSON)  # List of categories they belong to


class Collaboration(Base):
    __tablename__ = "collaborations"
    
    id = Column(Integer, primary_key=True, index=True)
    researcher_id = Column(Integer, index=True)  # Foreign key to researcher
    collaborator_id = Column(Integer, index=True)  # Foreign key to collaborator
    
    # Relationship metrics
    co_publications = Column(Integer, default=0)
    relationship_strength = Column(Float, default=0.0)
    direction = Column(String)  # 'mentor_to_student', 'peer', 'student_to_mentor'
    
    # Temporal information
    first_collaboration = Column(DateTime)
    last_collaboration = Column(DateTime)
    
    created_at = Column(DateTime, default=func.now())


# Pydantic models for API
class ResearcherBase(BaseModel):
    name: str
    affiliation: Optional[str] = None
    university: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    citations: int = 0
    h_index: int = 0
    i10_index: int = 0
    interests: List[str] = []
    research_categories: List[str] = []


class ResearcherCreate(ResearcherBase):
    scholar_id: str
    email: Optional[str] = None
    photo_url: Optional[str] = None
    homepage: Optional[str] = None


class ResearcherUpdate(BaseModel):
    name: Optional[str] = None
    affiliation: Optional[str] = None
    university: Optional[str] = None
    country: Optional[str] = None
    citations: Optional[int] = None
    h_index: Optional[int] = None
    i10_index: Optional[int] = None
    interests: Optional[List[str]] = None
    photo_url: Optional[str] = None
    is_verified: Optional[bool] = None


class ResearcherResponse(ResearcherBase):
    id: int
    scholar_id: str
    rank_score: float
    photo_url: Optional[str] = None
    homepage: Optional[str] = None
    last_updated: datetime
    created_at: datetime
    is_verified: bool
    
    class Config:
        from_attributes = True


class CollaborationBase(BaseModel):
    researcher_id: int
    collaborator_id: int
    co_publications: int = 0
    relationship_strength: float = 0.0
    direction: str = "peer"


class CollaborationCreate(CollaborationBase):
    first_collaboration: Optional[datetime] = None
    last_collaboration: Optional[datetime] = None


class CollaborationResponse(CollaborationBase):
    id: int
    first_collaboration: Optional[datetime] = None
    last_collaboration: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class GraphNode(BaseModel):
    id: int
    name: str
    university: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    citations: int
    h_index: int
    i10_index: int
    rank_score: float
    photo_url: Optional[str] = None
    research_categories: List[str] = []


class GraphEdge(BaseModel):
    source: int
    target: int
    strength: float
    direction: str
    co_publications: int


class GraphData(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]
    metadata: Dict = {}