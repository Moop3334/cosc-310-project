# How to run using Docker Compose

## Running with Docker Compose

To start both the frontend and backend services:

```bash
docker-compose up --build
```

### Service URLs:
- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:8000
- **Backend Health Check**: http://localhost:8000/health

### Services:
- **backend**: FastAPI server running on port 80 (mapped to 8000)
  - Environment: Python 3.14
  - Volumes: ./backend/app synced for live reload
  
- **frontend**: Vite + React dev server running on port 5173
  - Environment: Node 20
  - API Base URL: http://backend:80 (within Docker network)
  - Volumes: ./frontend/the-graveyard-shift synced for live reload

## Individual Service Commands

### Start services in the background:
```bash
docker-compose up -d
```

### Stop services:
```bash
docker-compose down
```

### Rebuild services:
```bash
docker-compose up --build
```

### View logs:
```bash
docker-compose logs -f
```

### View specific service logs:
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Rebuild specific services:
```bash
docker-compose build backend
docker-compose build frontend
```

## Network Communication

The backend and frontend communicate via the Docker internal network:
- Backend service name: `backend`
- Frontend connects to backend at: `http://backend:80`
- External access remains through localhost ports: 8000 and 5173

## Hot Reload

Both services support hot reload:
- **Backend**: Changes to files in `./backend/app` trigger restart
- **Frontend**: Changes to files in `./frontend/the-graveyard-shift/src` trigger browser reload

## Health Check

The docker-compose configuration includes a health check for the backend:
- The frontend waits for backend to be healthy before starting
- Health check endpoint: `/health`
- Checks every 10 seconds

## Environment Variables

Frontend environment variable:
- `VITE_API_BASE_URL`: Set to `http://backend:80` in docker-compose

To override, create a `.env` file in the frontend directory:
```
VITE_API_BASE_URL=http://backend:80
```

## Troubleshooting

### Frontend can't reach backend:
- Ensure both services are running: `docker-compose ps`
- Check backend logs: `docker-compose logs backend`
- Verify health check: `docker-compose logs backend | grep healthcheck`

### Port already in use:
```bash
# Change ports in docker-compose.yml
# or kill existing services on those ports
```

### Need to clear volumes:
```bash
docker-compose down -v
```

### Rebuild everything fresh:
```bash
docker-compose down
docker-compose up --build
```
