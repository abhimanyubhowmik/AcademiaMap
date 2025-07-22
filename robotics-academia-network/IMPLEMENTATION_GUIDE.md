# Robotics Academia Network - Implementation Guide

This document provides a comprehensive step-by-step guide to implement the Robotics Academia Network application.

## 🎯 Project Goals Recap

1. **Data Collection**: Scrape Google Scholar for robotics researchers
2. **Relationship Analysis**: Identify mentor-student and peer relationships
3. **Geographic Clustering**: Group researchers by regions
4. **Interactive Visualization**: Create network graphs with clickable nodes
5. **Filtering & Search**: Allow category and keyword-based filtering

## 📋 Implementation Phases

### Phase 1: Foundation & Setup (Week 1)

#### 1.1 Environment Setup
```bash
# Clone and setup project
git clone <your-repo>
cd robotics-academia-network

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup  
cd ../frontend
npm install

# Database setup
docker-compose up -d db redis
```

#### 1.2 Database Schema Implementation
```bash
# Create migration files
cd backend
alembic init alembic
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

**Create database tables:**
- `researchers` table with all fields from the model
- `collaborations` table for relationships
- `search_history` table for tracking searches
- Indexes on frequently queried fields

#### 1.3 Basic API Structure
- ✅ FastAPI app with CORS setup
- ✅ Router structure (researchers, graph, search)
- ✅ Pydantic models for request/response
- ✅ Error handling and logging

### Phase 2: Data Collection Engine (Week 2)

#### 2.1 Google Scholar Integration
**Priority Tasks:**
1. **Rate Limiting**: Implement robust rate limiting (10 req/min)
2. **Proxy Support**: Add proxy rotation to avoid IP blocking
3. **Error Handling**: Handle network timeouts and parsing errors
4. **Data Validation**: Validate extracted researcher data

**Implementation Steps:**
```python
# 1. Enhanced ScholarScraper class
- Add proxy rotation
- Implement exponential backoff
- Add request queuing system
- Cache successful requests

# 2. Data extraction improvements
- Better affiliation parsing
- University name standardization
- Country detection with multiple sources
- Photo URL validation
```

#### 2.2 Background Task System
```python
# Using Celery + Redis for background tasks
pip install celery redis

# Create tasks for:
- Keyword-based search
- Category-based search  
- Researcher profile updates
- Collaboration detection
```

#### 2.3 Database Operations
```python
# Implement CRUD operations
- create_researcher()
- update_researcher()
- get_researchers_by_filters()
- bulk_insert_researchers()

# Add database connection pooling
# Implement connection retry logic
```

### Phase 3: Relationship Detection (Week 3)

#### 3.1 Co-authorship Analysis
**Algorithm Design:**
```python
def detect_collaborations(researcher_id):
    """
    1. Get researcher's publications from Google Scholar
    2. Extract co-authors from each publication
    3. Match co-authors to existing researchers in DB
    4. Calculate collaboration strength metrics
    5. Determine relationship direction (mentor/student/peer)
    """
    
# Key metrics:
- Number of joint publications
- Publication timeline analysis
- Citation impact of joint work
- Career stage indicators
```

#### 3.2 Relationship Direction Algorithm
```python
def determine_relationship_direction(researcher1, researcher2):
    """
    Heuristics for mentor-student detection:
    1. Significant difference in citations/h-index
    2. Publication timeline (earlier vs later career)
    3. Institutional affiliation history
    4. First author patterns in joint publications
    """
```

#### 3.3 Graph Building
```python
# Use NetworkX for graph operations
import networkx as nx

def build_collaboration_graph(researchers):
    """
    1. Create nodes from researchers
    2. Add edges based on collaborations
    3. Calculate graph metrics
    4. Detect communities
    5. Apply layout algorithms
    """
```

### Phase 4: Backend API Implementation (Week 4)

#### 4.1 Complete API Endpoints

**Researchers API (`/api/v1/researchers/`):**
```python
# Implement all CRUD operations
GET    /                    # List with filtering
GET    /{id}               # Get single researcher
POST   /                   # Create researcher
PUT    /{id}               # Update researcher
DELETE /{id}               # Delete researcher
GET    /stats/summary      # Statistics
GET    /search/similar/{id} # Similar researchers
```

**Graph API (`/api/v1/graph/`):**
```python
GET /                      # Complete graph data
GET /nodes                 # Nodes only
GET /edges                 # Edges only
GET /layout/force          # Force-directed layout
GET /clusters              # Cluster analysis
GET /metrics               # Network metrics
```

**Search API (`/api/v1/search/`):**
```python
GET    /categories         # Available categories
POST   /keywords          # Search by keywords
POST   /categories        # Search by categories
GET    /status/{id}       # Search progress
GET    /results/{id}      # Search results
DELETE /cancel/{id}       # Cancel search
```

#### 4.2 Performance Optimization
```python
# Add caching layer
from functools import lru_cache
import redis

# Cache frequently accessed data
@lru_cache(maxsize=128)
def get_graph_data(filters_hash):
    # Implementation
    
# Database query optimization
- Add proper indexes
- Use connection pooling
- Implement query result caching
```

### Phase 5: Frontend Development (Weeks 5-6)

#### 5.1 Core Components Structure
```typescript
src/
├── components/
│   ├── Graph/
│   │   ├── NetworkGraph.tsx        # Main graph component
│   │   ├── GraphNode.tsx          # Individual node
│   │   ├── GraphEdge.tsx          # Edge rendering
│   │   └── GraphControls.tsx      # Zoom, pan controls
│   ├── FilterPanel/
│   │   ├── FilterPanel.tsx        # Main filter interface
│   │   ├── CategoryFilter.tsx     # Category selection
│   │   ├── RegionFilter.tsx       # Region selection
│   │   └── MetricsFilter.tsx      # Citation/h-index filters
│   ├── ResearcherCard/
│   │   ├── ResearcherProfile.tsx  # Detailed profile
│   │   ├── ResearcherCard.tsx     # Compact card
│   │   └── ResearcherMetrics.tsx  # Metrics display
│   └── Search/
│       ├── SearchInterface.tsx    # Search UI
│       ├── KeywordSearch.tsx      # Keyword input
│       └── SearchProgress.tsx     # Progress tracking
```

#### 5.2 Graph Visualization Implementation

**Option A: D3.js Implementation**
```typescript
// NetworkGraph.tsx using D3.js
import * as d3 from 'd3';

const NetworkGraph: React.FC<GraphComponentProps> = ({ 
  filters, 
  selectedResearcher, 
  onNodeClick 
}) => {
  const svgRef = useRef<SVGSVGElement>(null);
  
  useEffect(() => {
    // D3 force simulation
    const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(edges).id(d => d.id))
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width / 2, height / 2));
      
    // Render nodes and edges
    // Add interaction handlers
  }, [filters]);
};
```

**Option B: Cytoscape.js Implementation (Recommended)**
```typescript
// NetworkGraph.tsx using Cytoscape.js
import cytoscape from 'cytoscape';
import fcose from 'cytoscape-fcose';

cytoscape.use(fcose);

const NetworkGraph: React.FC<GraphComponentProps> = (props) => {
  const cyRef = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    const cy = cytoscape({
      container: cyRef.current,
      elements: [...nodes, ...edges],
      style: [
        {
          selector: 'node',
          style: {
            'background-color': (node) => getRegionColor(node.data('region')),
            'width': (node) => Math.max(20, node.data('rank_score') / 2),
            'height': (node) => Math.max(20, node.data('rank_score') / 2),
            'label': 'data(name)'
          }
        }
      ],
      layout: { name: 'fcose' }
    });
    
    // Event handlers
    cy.on('tap', 'node', (evt) => {
      onNodeClick(evt.target.data('id'));
    });
  }, [filters]);
};
```

#### 5.3 State Management
```typescript
// Using Zustand for state management
import { create } from 'zustand';

interface AppState {
  filters: FilterState;
  selectedResearcher: number | null;
  graphData: GraphData | null;
  loading: boolean;
  setFilters: (filters: FilterState) => void;
  selectResearcher: (id: number | null) => void;
  loadGraphData: () => Promise<void>;
}

const useAppStore = create<AppState>((set, get) => ({
  filters: { categories: [], regions: [], minCitations: 1000, maxNodes: 200 },
  selectedResearcher: null,
  graphData: null,
  loading: false,
  setFilters: (filters) => set({ filters }),
  selectResearcher: (id) => set({ selectedResearcher: id }),
  loadGraphData: async () => {
    set({ loading: true });
    // API call implementation
    set({ loading: false });
  }
}));
```

### Phase 6: Graph Interaction & UI Polish (Week 7)

#### 6.1 Interactive Features
```typescript
// Node interaction features
- Click to select researcher
- Hover to highlight connections
- Double-click to center and zoom
- Right-click for context menu

// Graph controls
- Zoom in/out with mouse wheel
- Pan by dragging
- Reset view button
- Fullscreen mode
- Export graph as image
```

#### 6.2 Researcher Profile Modal
```typescript
const ResearcherProfile: React.FC<{ researcher: Researcher }> = ({ researcher }) => {
  return (
    <Modal title={researcher.name} open={true}>
      <div className="researcher-profile">
        {researcher.photo_url && (
          <img src={researcher.photo_url} alt={researcher.name} />
        )}
        <div className="metrics">
          <Statistic title="Citations" value={researcher.citations} />
          <Statistic title="h-index" value={researcher.h_index} />
          <Statistic title="i10-index" value={researcher.i10_index} />
        </div>
        <div className="details">
          <p><strong>University:</strong> {researcher.university}</p>
          <p><strong>Country:</strong> {researcher.country}</p>
          <Flag country={researcher.country} />
        </div>
        <div className="interests">
          {researcher.interests.map(interest => (
            <Tag key={interest}>{interest}</Tag>
          ))}
        </div>
      </div>
    </Modal>
  );
};
```

### Phase 7: Search & Data Management (Week 8)

#### 7.1 Search Interface
```typescript
const SearchInterface: React.FC = () => {
  const [searchType, setSearchType] = useState<'keywords' | 'categories'>('keywords');
  const [searchProgress, setSearchProgress] = useState<SearchProgress | null>(null);
  
  const handleSearch = async (request: SearchRequest) => {
    const response = await api.search(request);
    // Poll for progress updates
    const interval = setInterval(async () => {
      const progress = await api.getSearchStatus(response.search_id);
      setSearchProgress(progress);
      if (progress.status === 'completed') {
        clearInterval(interval);
        // Load results
      }
    }, 2000);
  };
};
```

#### 7.2 Progress Tracking
```typescript
const SearchProgress: React.FC<{ progress: SearchProgress }> = ({ progress }) => {
  return (
    <div className="search-progress">
      <Progress 
        percent={progress.progress * 100}
        status={progress.status === 'completed' ? 'success' : 'active'}
      />
      <p>{progress.current_step}</p>
      <p>Found {progress.results_found} researchers</p>
      {progress.estimated_completion && (
        <p>Estimated completion: {progress.estimated_completion}</p>
      )}
    </div>
  );
};
```

### Phase 8: Testing & Optimization (Week 9)

#### 8.1 Backend Testing
```python
# pytest for API testing
def test_get_researchers():
    response = client.get("/api/v1/researchers/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_search_by_keywords():
    request = {"keywords": ["robotics"], "max_results": 10}
    response = client.post("/api/v1/search/keywords", json=request)
    assert response.status_code == 200
    assert "search_id" in response.json()
```

#### 8.2 Frontend Testing
```typescript
// Jest + React Testing Library
import { render, screen, fireEvent } from '@testing-library/react';

test('filters researchers by category', async () => {
  render(<FilterPanel {...props} />);
  
  const slamCheckbox = screen.getByLabelText('SLAM');
  fireEvent.click(slamCheckbox);
  
  await waitFor(() => {
    expect(props.onFiltersChange).toHaveBeenCalledWith({
      ...props.filters,
      categories: ['slam']
    });
  });
});
```

#### 8.3 Performance Testing
```python
# Load testing with locust
from locust import HttpUser, task

class ApiUser(HttpUser):
    @task
    def get_graph_data(self):
        self.client.get("/api/v1/graph/")
    
    @task
    def search_researchers(self):
        self.client.get("/api/v1/researchers/?limit=50")
```

### Phase 9: Deployment (Week 10)

#### 9.1 Production Setup
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl
  
  backend:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/robotics_academia
      - REDIS_URL=redis://redis:6379
      - ENVIRONMENT=production
  
  frontend:
    build: ./frontend
    environment:
      - REACT_APP_API_URL=https://your-domain.com
```

#### 9.2 CI/CD Pipeline
```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build and deploy
        run: |
          docker-compose -f docker-compose.prod.yml build
          docker-compose -f docker-compose.prod.yml up -d
```

## 🚀 Quick Start Commands

```bash
# Development setup
git clone <repo>
cd robotics-academia-network
docker-compose up -d

# Backend development
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend development  
cd frontend
npm install && npm start

# Run initial data collection
curl -X POST "http://localhost:8000/api/v1/search/categories" \
  -H "Content-Type: application/json" \
  -d '{"categories": ["general_robotics", "slam"], "max_results": 50}'
```

## 📊 Success Metrics

- **Data Quality**: >90% researcher profiles with complete information
- **Graph Performance**: <2s load time for 200 nodes
- **Search Speed**: <30s for keyword searches returning 50 results  
- **User Experience**: Smooth 60fps graph interactions
- **Data Coverage**: >1000 researchers across all major robotics areas

## 🔄 Iteration Plan

1. **MVP** (Weeks 1-4): Basic data collection + simple graph
2. **Beta** (Weeks 5-8): Full UI + advanced features  
3. **V1.0** (Weeks 9-10): Production deployment + optimization
4. **V1.1+**: ML-based relationship detection, real-time updates

## 📝 Notes

- Start with small datasets for testing (10-50 researchers)
- Implement comprehensive logging for debugging Scholar scraping
- Consider Google Scholar's terms of service and rate limits
- Plan for data storage growth (images, cached results)
- Monitor API performance and add caching where needed