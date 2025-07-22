// Core data types for the Robotics Academia Network

export interface Researcher {
  id: number;
  scholar_id: string;
  name: string;
  affiliation?: string;
  university?: string;
  country?: string;
  region?: string;
  citations: number;
  h_index: number;
  i10_index: number;
  rank_score: number;
  interests: string[];
  research_categories: string[];
  photo_url?: string;
  homepage?: string;
  email?: string;
  last_updated: string;
  created_at: string;
  is_verified: boolean;
}

export interface GraphNode {
  id: number;
  name: string;
  university?: string;
  country?: string;
  region?: string;
  citations: number;
  h_index: number;
  i10_index: number;
  rank_score: number;
  photo_url?: string;
  research_categories: string[];
  x?: number; // For graph positioning
  y?: number; // For graph positioning
}

export interface GraphEdge {
  source: number;
  target: number;
  strength: number;
  direction: 'mentor_to_student' | 'student_to_mentor' | 'peer';
  co_publications: number;
}

export interface GraphData {
  nodes: GraphNode[];
  edges: GraphEdge[];
  metadata: {
    total_nodes: number;
    total_edges: number;
    filters_applied: FilterState;
  };
}

export interface FilterState {
  categories: string[];
  regions: string[];
  minCitations: number;
  maxNodes: number;
}

export interface SearchFilters {
  categories?: string[];
  regions?: string[];
  min_citations?: number;
  max_nodes?: number;
  include_edges?: boolean;
}

export interface SearchRequest {
  keywords?: string[];
  categories?: string[];
  max_results?: number;
  min_citations?: number;
}

export interface SearchResponse {
  search_id: string;
  status: 'started' | 'in_progress' | 'completed' | 'failed' | 'cancelled';
  message: string;
  keywords?: string[];
  categories?: string[];
  estimated_duration?: string;
}

export interface SearchProgress {
  status: 'started' | 'in_progress' | 'completed' | 'failed' | 'cancelled';
  progress: number; // 0-1
  current_step: string;
  results_found: number;
  estimated_completion?: string;
}

export interface ResearchCategory {
  key: string;
  label: string;
  keywords: string[];
  color?: string;
  description?: string;
}

export interface Region {
  key: string;
  label: string;
  countries: string[];
  color?: string;
}

// Graph visualization types
export interface NodePosition {
  x: number;
  y: number;
}

export interface GraphLayout {
  positions: Record<number, NodePosition>;
  layout_info: {
    algorithm: string;
    width: number;
    height: number;
    iterations?: number;
  };
}

export interface GraphMetrics {
  network_size: {
    nodes: number;
    edges: number;
    density: number;
  };
  centrality: {
    most_central_researchers: Researcher[];
    avg_clustering_coefficient: number;
  };
  communities: {
    num_communities: number;
    modularity: number;
  };
  small_world: {
    avg_path_length: number;
    clustering_coefficient: number;
    small_world_coefficient: number;
  };
}

export interface Cluster {
  id: string;
  name: string;
  researcher_ids: number[];
  center?: NodePosition;
  color?: string;
  metadata?: Record<string, any>;
}

export interface ClusterData {
  clusters: Record<string, number[]>;
  method: 'regional' | 'topical' | 'collaborative';
  metadata: {
    total_clusters: number;
    largest_cluster_size: number;
    silhouette_score?: number;
  };
}

// API response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: 'success' | 'error';
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

// Component prop types
export interface GraphComponentProps {
  filters: FilterState;
  selectedResearcher?: number | null;
  onNodeClick: (researcherId: number) => void;
  width?: number;
  height?: number;
}

export interface FilterPanelProps {
  filters: FilterState;
  onFiltersChange: (filters: FilterState) => void;
  selectedResearcher?: number | null;
  onResearcherSelect: (researcherId: number | null) => void;
}

export interface ResearcherCardProps {
  researcher: Researcher;
  onClick?: () => void;
  showDetails?: boolean;
  compact?: boolean;
}

// Utility types
export type SortField = 'rank_score' | 'citations' | 'h_index' | 'name';
export type SortDirection = 'asc' | 'desc';

export interface SortOptions {
  field: SortField;
  direction: SortDirection;
}

export interface ViewState {
  zoom: number;
  center: NodePosition;
  selectedNodes: number[];
  highlightedNodes: number[];
}

// Error types
export interface ApiError {
  message: string;
  code?: string;
  details?: any;
}

// Theme and styling
export interface ThemeColors {
  primary: string;
  secondary: string;
  accent: string;
  background: string;
  surface: string;
  text: string;
  textSecondary: string;
  border: string;
  error: string;
  warning: string;
  success: string;
}

export interface RegionColors {
  'North America': string;
  'Europe': string;
  'China': string;
  'Japan': string;
  'South Korea': string;
  'Singapore': string;
  'Australia': string;
  'India': string;
  'Other': string;
}