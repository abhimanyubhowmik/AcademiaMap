import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Layout, ConfigProvider, theme } from 'antd';
import styled from 'styled-components';

import NetworkGraph from './components/Graph/NetworkGraph';
import FilterPanel from './components/FilterPanel/FilterPanel';
import ResearcherProfile from './components/ResearcherCard/ResearcherProfile';
import SearchInterface from './components/Search/SearchInterface';
import Header from './components/common/Header';

const { Content, Sider } = Layout;

// Create a client for React Query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

const AppContainer = styled(Layout)`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
`;

const StyledSider = styled(Sider)`
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 0 20px 20px 0;
  margin: 20px 0;
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
`;

const StyledContent = styled(Content)`
  margin: 20px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
  overflow: hidden;
`;

const GraphContainer = styled.div`
  height: calc(100vh - 140px);
  position: relative;
  border-radius: 20px;
  overflow: hidden;
`;

const App: React.FC = () => {
  const [selectedResearcher, setSelectedResearcher] = React.useState<number | null>(null);
  const [filters, setFilters] = React.useState({
    categories: [] as string[],
    regions: [] as string[],
    minCitations: 1000,
    maxNodes: 200
  });

  return (
    <ConfigProvider
      theme={{
        algorithm: theme.defaultAlgorithm,
        token: {
          colorPrimary: '#667eea',
          borderRadius: 8,
        },
      }}
    >
      <QueryClientProvider client={queryClient}>
        <Router>
          <AppContainer>
            <Header />
            
            <Layout style={{ background: 'transparent' }}>
              <StyledSider 
                width={320} 
                collapsible
                defaultCollapsed={false}
              >
                <Routes>
                  <Route path="/search" element={
                    <SearchInterface />
                  } />
                  <Route path="*" element={
                    <FilterPanel 
                      filters={filters}
                      onFiltersChange={setFilters}
                      selectedResearcher={selectedResearcher}
                      onResearcherSelect={setSelectedResearcher}
                    />
                  } />
                </Routes>
              </StyledSider>

              <StyledContent>
                <Routes>
                  <Route path="/researcher/:id" element={<ResearcherProfile />} />
                  <Route path="/search" element={
                    <div style={{ padding: '40px', textAlign: 'center' }}>
                      <h2 style={{ color: 'white', marginBottom: '20px' }}>
                        Search for Robotics Researchers
                      </h2>
                      <p style={{ color: 'rgba(255, 255, 255, 0.8)' }}>
                        Use the panel on the left to search by keywords or categories
                      </p>
                    </div>
                  } />
                  <Route path="*" element={
                    <GraphContainer>
                      <NetworkGraph
                        filters={filters}
                        selectedResearcher={selectedResearcher}
                        onNodeClick={setSelectedResearcher}
                      />
                    </GraphContainer>
                  } />
                </Routes>
              </StyledContent>
            </Layout>
          </AppContainer>
        </Router>
      </QueryClientProvider>
    </ConfigProvider>
  );
};

export default App;