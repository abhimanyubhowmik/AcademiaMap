from pydantic_settings import BaseSettings
from typing import Optional, List
import os


class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Robotics Academia Network"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "A web application to understand robotics academia networks"
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/robotics_academia"
    
    # Scholar API Settings
    SCHOLAR_RATE_LIMIT: int = 10  # requests per minute
    MAX_RESULTS_PER_SEARCH: int = 100
    MIN_CITATIONS_THRESHOLD: int = 1000
    TOP_RESEARCHERS_LIMIT: int = 200
    
    # Geographic Regions
    REGIONS: dict = {
        "North America": ["United States", "Canada"],
        "Europe": ["United Kingdom", "Germany", "France", "Netherlands", "Switzerland", 
                  "Italy", "Spain", "Sweden", "Denmark", "Norway", "Finland", "Austria", "Belgium"],
        "Asia-Pacific": {
            "China": ["China", "Hong Kong", "Macau", "Taiwan"],
            "Japan": ["Japan"],
            "South Korea": ["South Korea"],
            "Singapore": ["Singapore"],
            "Australia": ["Australia", "New Zealand"],
            "India": ["India"]
        }
    }
    
    # Research Keywords by Category
    RESEARCH_CATEGORIES: dict = {
        "general_robotics": ["robotics", "autonomous systems", "robot control"],
        "slam": ["slam", "simultaneous localization and mapping", "visual slam", "lidar slam"],
        "robot_vision": ["computer vision", "robot vision", "visual perception", "object detection"],
        "aerial_robotics": ["unmanned aerial vehicles", "drone", "quadcopter", "UAV", "aerial robotics"],
        "marine_robotics": ["underwater robotics", "marine robotics", "AUV", "autonomous underwater vehicle"],
        "space_robotics": ["space robotics", "planetary rovers", "satellite robotics"],
        "field_robotics": ["field robotics", "outdoor robotics", "agricultural robotics"],
        "path_planning": ["path planning", "motion planning", "trajectory planning", "navigation"],
        "human_robot_interaction": ["human robot interaction", "HRI", "social robotics"],
        "swarm_robotics": ["swarm robotics", "multi-robot systems", "collective intelligence"],
        "medical_robotics": ["medical robotics", "surgical robotics", "rehabilitation robotics"],
        "manipulation": ["robot manipulation", "grasping", "dexterous manipulation"]
    }
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # React dev server
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "https://localhost:3000",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()