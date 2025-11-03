# Architecture Overview

## System Architecture

The application uses a three-tier design:

```mermaid
graph TB
    subgraph "Presentation Layer"
        UI[Bootstrap 5 + Leaflet.js]
        Client[JavaScript API Client]
    end
    
    subgraph "Application Layer - Django MVC"
        Models[Models<br/>Business<br/>BusinessCategory<br/>ServiceArea]
        Views[Views/Viewsets<br/>BusinessViewSet<br/>IndexView]
        Serializers[Serializers<br/>GeoJSON Serialization<br/>Data Validation]
        URLs[URL Routing<br/>RESTful Endpoints]
        
        Models --> Views
        Views --> Serializers
        Serializers --> URLs
    end
    
    subgraph "Data Layer"
        DB[(PostgreSQL + PostGIS)]
        Queries[Spatial Queries<br/>- Proximity Search<br/>- Nearest Neighbor<br/>- Containment]
        
        DB --> Queries
    end
    
    UI --> Client
    Client -->|HTTP/REST| URLs
    URLs -->|ORM + PostGIS| DB
    Views --> Queries
```


## Component Interactions

### Request Flow

1. User interaction → JavaScript API client
2. API request → Django views
3. Query → PostGIS
4. Results → GeoJSON
5. Rendering → Leaflet markers

### MVC Pattern

- **Models**: Business, BusinessCategory, ServiceArea
- **Views**: BusinessViewSet, IndexView
- **Controllers**: URL routing
