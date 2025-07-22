# Robotics Academia Network - Project Structure

## Directory Structure
```
robotics-academia-network/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── researchers.py
│   │   │   │   ├── graph.py
│   │   │   │   └── search.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   ├── models/
│   │   │   ├── researcher.py
│   │   │   └── collaboration.py
│   │   ├── services/
│   │   │   ├── scholar_scraper.py
│   │   │   ├── graph_builder.py
│   │   │   └── location_mapper.py
│   │   └── utils/
│   │       ├── helpers.py
│   │       └── constants.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Graph/
│   │   │   ├── ResearcherCard/
│   │   │   ├── FilterPanel/
│   │   │   └── common/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── types/
│   │   └── utils/
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Phase-by-Phase Implementation

### Phase 1: Data Collection (Weeks 1-2)
1. **Google Scholar API Integration**
   - Use `scholarly` Python library
   - Implement rate limiting and error handling
   - Create keyword-based search functionality

2. **Data Models Design**
   - Researcher profile structure
   - Collaboration relationships
   - Citation metrics

### Phase 2: Graph Analysis (Weeks 3-4)
1. **Relationship Detection**
   - Co-authorship analysis
   - Citation hierarchy mapping
   - Influence scoring algorithm

2. **Location Clustering**
   - University-to-location mapping
   - Regional grouping logic

### Phase 3: Backend API (Weeks 5-6)
1. **FastAPI Implementation**
   - RESTful endpoints
   - Data filtering and pagination
   - Graph data serialization

### Phase 4: Frontend Development (Weeks 7-9)
1. **React Application**
   - Interactive graph visualization
   - Researcher profile cards
   - Filter and search interface

2. **Graph Visualization**
   - D3.js integration
   - Node interaction handlers
   - Dynamic layout algorithms

### Phase 5: Integration & Polish (Weeks 10-11)
1. **Full-stack integration**
2. **Performance optimization**
3. **UI/UX refinements**

## Key Technical Challenges

### 1. Google Scholar Scraping
- **Challenge**: Rate limiting and IP blocking
- **Solution**: 
  - Implement exponential backoff
  - Use proxy rotation
  - Respect robots.txt
  - Consider using official APIs where available

### 2. Relationship Detection
- **Challenge**: Determining mentor-student relationships
- **Solution**:
  - Analyze publication timeline
  - Consider citation patterns
  - Use career stage indicators (PhD year, first publications)

### 3. Graph Performance
- **Challenge**: Rendering 200+ nodes efficiently
- **Solution**:
  - Implement viewport culling
  - Use canvas rendering for performance
  - Add zoom levels with different detail

### 4. Data Accuracy
- **Challenge**: Ensuring profile accuracy
- **Solution**:
  - Multiple verification sources
  - Manual review flags
  - Community correction features