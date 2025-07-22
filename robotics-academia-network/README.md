# Robotics Academia Network

A web application to understand and visualize the robotics academia landscape through interactive network graphs. This tool helps identify influential researchers, their collaborations, and geographic distributions in the field of robotics.

## 🚀 Features

- **Researcher Discovery**: Search and identify prominent robotics researchers using Google Scholar
- **Citation Analysis**: Rank researchers based on citations, h-index, and i10-index
- **Collaboration Networks**: Visualize mentor-student and peer relationships
- **Geographic Clustering**: Group researchers by regions (US, Europe, Asia-Pacific, etc.)
- **Interactive Graphs**: Clickable nodes with detailed researcher profiles
- **Category Filtering**: Filter by research areas (SLAM, Computer Vision, Aerial Robotics, etc.)
- **Responsive Design**: Modern UI with smooth interactions

## 🏗️ Architecture

### Backend (Python/FastAPI)
- **FastAPI**: Modern, fast web framework for building APIs
- **PostgreSQL**: Primary database for storing researcher data
- **SQLAlchemy**: ORM for database operations
- **Scholarly**: Google Scholar scraping library
- **NetworkX**: Graph analysis and relationship detection

### Frontend (React/TypeScript)
- **React 18**: Modern React with hooks and concurrent features
- **TypeScript**: Type-safe development
- **D3.js/Cytoscape.js**: Interactive graph visualization
- **Ant Design**: UI component library
- **Styled Components**: CSS-in-JS styling

### Infrastructure
- **Docker**: Containerized deployment
- **Redis**: Caching layer
- **nginx**: Reverse proxy (production)

## 📋 Prerequisites

- Docker and Docker Compose
- Node.js 16+ (for local development)
- Python 3.9+ (for local development)
- PostgreSQL 12+ (for local development)

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
```bash
git clone <repository-url>
cd robotics-academia-network
```

2. **Start the application**
```bash
docker-compose up -d
```

3. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Local Development Setup

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your database configuration

# Start the backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup
```bash
cd frontend
npm install
npm start
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/robotics_academia

# Scholar API Settings
SCHOLAR_RATE_LIMIT=10
MAX_RESULTS_PER_SEARCH=100
MIN_CITATIONS_THRESHOLD=1000
TOP_RESEARCHERS_LIMIT=200

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]
```

## 📊 Usage

### 1. Data Collection
The application automatically scrapes Google Scholar based on predefined research categories:

- **General Robotics**: Basic robotics research
- **SLAM**: Simultaneous Localization and Mapping
- **Robot Vision**: Computer vision for robotics
- **Aerial Robotics**: UAVs, drones, quadcopters
- **Marine Robotics**: Underwater and marine systems
- **Space Robotics**: Planetary rovers, space systems
- **Field Robotics**: Outdoor and agricultural robotics
- **Path Planning**: Navigation and motion planning
- **Human-Robot Interaction**: Social robotics
- **Swarm Robotics**: Multi-robot systems
- **Medical Robotics**: Surgical and rehabilitation robots
- **Manipulation**: Grasping and dexterous manipulation

### 2. Graph Visualization
- **Node Size**: Represents researcher's rank score (citations, h-index, i10-index)
- **Node Color**: Indicates geographic region
- **Edges**: Show collaboration relationships
- **Edge Direction**: Points from mentor to student (when detectable)

### 3. Interactive Features
- **Click nodes** to view detailed researcher profiles
- **Filter by categories** using the sidebar
- **Zoom and pan** to explore the network
- **Regional clustering** to focus on specific areas

## 🔍 API Endpoints

### Researchers
- `GET /api/v1/researchers/` - List all researchers
- `GET /api/v1/researchers/{id}` - Get researcher details
- `POST /api/v1/researchers/` - Create new researcher
- `PUT /api/v1/researchers/{id}` - Update researcher

### Graph Data
- `GET /api/v1/graph/` - Get network graph data
- `GET /api/v1/graph/nodes` - Get graph nodes only
- `GET /api/v1/graph/edges` - Get graph edges only

### Search
- `POST /api/v1/search/keywords` - Search by keywords
- `POST /api/v1/search/categories` - Search by categories
- `GET /api/v1/search/categories` - List available categories

## 🛠️ Development

### Backend Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Format code
black app/
isort app/

# Type checking
mypy app/
```

### Frontend Development
```bash
# Install dependencies
npm install

# Start development server
npm start

# Run tests
npm test

# Build for production
npm run build

# Lint code
npm run lint
npm run lint:fix
```

## 📈 Performance Considerations

### Rate Limiting
Google Scholar has strict rate limits. The application implements:
- Exponential backoff
- Request throttling (10 requests/minute by default)
- Proxy rotation (when available)

### Caching
- Redis caching for API responses
- Browser caching for static assets
- Database query optimization

### Graph Rendering
- Viewport culling for large networks
- Canvas rendering for better performance
- Progressive loading of node details

## 🚀 Deployment

### Production Deployment
```bash
# Build and deploy with Docker
docker-compose -f docker-compose.prod.yml up -d

# Or deploy to cloud platforms
# (Add specific instructions for AWS, GCP, Azure, etc.)
```

### Environment Setup
- Set up SSL certificates
- Configure domain names
- Set up monitoring and logging
- Configure backup strategies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Scholar for providing academic data
- The robotics research community
- Open source libraries and frameworks used

## 📞 Support

For questions, issues, or contributions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation at `/docs`

## 🔮 Future Enhancements

- Real-time collaboration updates
- Machine learning for better relationship detection
- Integration with other academic databases
- Mobile application
- Social features for researchers
- Publication trend analysis
- Conference and journal impact metrics