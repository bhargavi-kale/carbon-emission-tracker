# Architecture Design

## System Overview
The Carbon Commute Calculator follows a full-stack web architecture.

### Frontend
- HTML (Jinja2 templates)
- CSS responsive layout
- JavaScript + Google Maps API

### Backend
- Python Flask server
- Route handling
- Emissions calculation logic

### Database
- SQLite database
- SQLAlchemy ORM

### External Data Sources
- Google Routes API → distance calculation
- EPA vehicle CSV dataset → fuel type information

## Data Flow
1. User adds vehicle
2. Vehicle saved to database
3. User inputs commute
4. Google API calculates distance
5. Backend computes emissions
6. Dashboard displays results

## Key Components

### Emissions Calculation Engine
- Takes vehicle fuel type, fuel efficiency, and distance as inputs
- References EPA vehicle dataset for accurate emissions factors
- Outputs CO₂ equivalent (kg) for each commute

### Responsive Design
- Mobile-first CSS approach
- Breakpoints for tablet and desktop views
- Google Maps API integration for interactive route visualization

### Data Models
- **Vehicle**: stores fuel type, MPG, user associations
- **Route**: caches distance calculations from Google API
- **Commute/Trip**: logs individual journeys with emissions data

## Technology Choices
- **Flask**: lightweight, suitable for small-to-medium applications
- **SQLite**: serverless database, easy deployment
- **Google Routes API**: accurate real-world distance calculations
- **SQLAlchemy ORM**: type-safe database interactions