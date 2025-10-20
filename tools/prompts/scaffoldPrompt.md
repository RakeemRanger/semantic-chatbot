# Project Scaffold Generation Instructions# Project Scaffold Generation Instructions



## ⚠️ Critical Rules## ⚠️ Critical Rules



**ONLY return a valid JSON object** with the structure defined below.**ONLY return a valid JSON object** with the structure defined below.



### ❌ DO NOT:### ❌ DO NOT:



- Don't Include \`\`\`json code fences in the response- Include \`\`\`json code fences in the response

- Don't Include any text before or after the JSON- Include any text before or after the JSON

- Don't Return anything if you cannot generate valid JSON- Return anything if you cannot generate valid JSON 

{

## Required JSON Structure    "project_name": "string",

    "description": "string",

```json    "structure": {

{        "folders": ["folder1", "folder1/subfolder", "folder2"],

    "project_name": "string",        "files": {

    "description": "string",            "path/to/file.ext": "file content here",

    "structure": {            "another/file.py": "content"

        "folders": ["folder1", "folder1/subfolder", "folder2"],        }

        "files": {    }

            "path/to/file.ext": "file content here",}

            "another/file.py": "content"

        }Include:

    }1. All necessary folders (use forward slashes for nested folders)

}2. All essential files with actual boilerplate code

```3. Configuration files (package.json, requirements.txt, etc.)

4. README.md with setup instructions

## Requirements Checklist5. .gitignore appropriate for the project type



Include the following in every response:Make it production-ready with best practices.



1. **All necessary folders** (use forward slashes for nested folders)Example bad return 

2. **All essential files** with actual boilerplate code

3. **Configuration files** (package.json, requirements.txt, etc.)```json

4. **README.md** with setup instructions{

5. **.gitignore** appropriate for the project type    "project_name": "bls-data-api",

    "description": "Production-ready FastAPI application for querying Bureau of Labor Statistics (BLS) data with caching, rate limiting, and comprehensive error handling",

Make it **production-ready** with best practices.    "structure": {

        "folders": [

---            "app",

            "app/api",

## ❌ Example of INCORRECT Response            "app/api/v1",

            "app/core",

**This is WRONG** because it includes \`\`\`json markers:            "app/models",

            "app/services",

\`\`\`json            "app/schemas",

{            "app/utils",

    "project_name": "my-project",            "tests",

    "description": "A sample project"            "tests/api",

}            "tests/services"

\`\`\`        ],

        "files": {

**Never do this!** The AI should return **raw JSON only and don't use ```json in response**.            "requirements.txt": "fastapi==0.104.1\nuvicorn[standard]==0.24.0\npydantic==2.5.0\npydantic-settings==2.1.0\nhttpx==0.25.2\npython-dotenv==1.0.0\nredis==5.0.1\npython-jose[cryptography]==3.3.0\nslowapi==0.1.9\nprometheus-fastapi-instrumentator==6.1.0\npytest==7.4.3\npytest-asyncio==0.21.1\npytest-cov==4.1.0\nblack==23.12.0\nflake8==6.1.0\nmypy==1.7.1\npre-commit==3.5.0",

            "requirements-dev.txt": "pytest==7.4.3\npytest-asyncio==0.21.1\npytest-cov==4.1.0\npytest-mock==3.12.0\nblack==23.12.0\nflake8==6.1.0\nmypy==1.7.1\nisort==5.13.2\npre-commit==3.5.0\nhttpx==0.25.2",

---            ".env.example": "# Application Settings\nAPP_NAME=BLS Data API\nAPP_VERSION=1.0.0\nENVIRONMENT=development\nDEBUG=True\n\n# BLS API Configuration\nBLS_API_KEY=your_bls_api_key_here\nBLS_API_BASE_URL=https://api.bls.gov/publicAPI/v2\nBLS_API_TIMEOUT=30\nBLS_API_MAX_RETRIES=3\n\n# Redis Configuration\nREDIS_HOST=localhost\nREDIS_PORT=6379\nREDIS_DB=0\nREDIS_PASSWORD=\nCACHE_TTL=3600\n\n# API Security\nAPI_KEY_HEADER=X-API-Key\nALLOWED_HOSTS=*\nCORS_ORIGINS=[\"http://localhost:3000\",\"http://localhost:8000\"]\n\n# Rate Limiting\nRATE_LIMIT_PER_MINUTE=60\nRATE_LIMIT_PER_HOUR=1000\n\n# Logging\nLOG_LEVEL=INFO",

            ".gitignore": "# Python\n__pycache__/\n*.py[cod]\n*$py.class\n*.so\n.Python\nbuild/\ndevelop-eggs/\ndist/\ndownloads/\neggs/\n.eggs/\nlib/\nlib64/\nparts/\nsdist/\nvar/\nwheels/\npip-wheel-metadata/\nshare/python-wheels/\n*.egg-info/\n.installed.cfg\n*.egg\nPIPFILE.lock\n\n# Virtual Environment\nvenv/\nenv/\nENV/\nenv.bak/\nvenv.bak/\n\n# IDEs\n.vscode/\n.idea/\n*.swp\n*.swo\n*~\n.DS_Store\n\n# Environment Variables\n.env\n.env.local\n.env.*.local\n\n# Testing\n.pytest_cache/\n.coverage\nhtmlcov/\n.tox/\n\n# Logs\n*.log\nlogs/\n\n# Database\n*.db\n*.sqlite3\n\n# Misc\n.mypy_cache/\n.dmypy.json\ndmypy.json",

## ✅ Example of CORRECT Response            "README.md": "# BLS Data API\n\nA production-ready FastAPI application for querying Bureau of Labor Statistics (BLS) data with built-in caching, rate limiting, and comprehensive error handling.\n\n## Features\n\n- 🚀 Fast and async API built with FastAPI\n- 📊 Query BLS economic data series\n- 🔄 Redis caching for improved performance\n- 🛡️ Rate limiting to prevent API abuse\n- 🔐 API key authentication\n- 📝 Comprehensive logging and monitoring\n- ✅ Input validation with Pydantic\n- 🧪 Unit and integration tests\n- 📚 Auto-generated OpenAPI documentation\n\n## Prerequisites\n\n- Python 3.9+\n- Redis Server\n- BLS API Key (register at https://www.bls.gov/developers/)\n\n## Installation\n\n1. Clone the repository:\n```bash\ngit clone <repository-url>\ncd bls-data-api\n```\n\n2. Create and activate virtual environment:\n```bash\npython -m venv venv\nsource venv/bin/activate  # On Windows: venv\\Scripts\\activate\n```\n\n3. Install dependencies:\n```bash\npip install -r requirements.txt\n```\n\n4. Set up environment variables:\n```bash\ncp .env.example .env\n# Edit .env with your configuration\n```\n\n5. Start Redis (using Docker):\n```bash\ndocker run -d -p 6379:6379 redis:alpine\n```\n\n## Running the Application\n\n### Development\n```bash\nuvicorn app.main:app --reload --host 0.0.0.0 --port 8000\n```\n\n### Production\n```bash\nuvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4\n```\n\n## API Documentation\n\nOnce running, visit:\n- Swagger UI: http://localhost:8000/docs\n- ReDoc: http://localhost:8000/redoc\n- OpenAPI JSON: http://localhost:8000/openapi.json\n\n## API Endpoints\n\n### Health Check\n```\nGET /health\n```\n\n### Get Series Data\n```\nGET /api/v1/series/{series_id}\n```\n\nQuery Parameters:\n- `start_year` (required): Start year (YYYY)\n- `end_year` (required): End year (YYYY)\n- `catalog` (optional): Include catalog metadata\n\n### Get Multiple Series\n```\nPOST /api/v1/series/batch\n```\n\nBody:\n```json\n{\n  \"series_ids\": [\"LAUCN040010000000005\", \"LAUCN040010000000006\"],\n  \"start_year\": \"2020\",\n  \"end_year\": \"2023\"\n}\n```\n\n## Popular BLS Series IDs\n\n- `LAUCN040010000000005` - Unemployment Rate\n- `CUUR0000SA0` - Consumer Price Index (CPI-U)\n- `CES0000000001` - Total Nonfarm Employment\n- `LNS14000000` - Unemployment Rate (National)\n\n## Testing\n\nRun tests:\n```bash\npytest\n```\n\nWith coverage:\n```bash\npytest --cov=app --cov-report=html\n```\n\n## Code Quality\n\nFormat code:\n```bash\nblack app/\nisort app/\n```\n\nLint:\n```bash\nflake8 app/\nmypy app/\n```\n\n## Docker Deployment\n\nBuild image:\n```bash\ndocker build -t bls-data-api .\n```\n\nRun container:\n```bash\ndocker-compose up -d\n```\n\n## Environment Variables\n\nSee `.env.example` for all available configuration options.\n\n## License\n\nMIT\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first.",

            "Dockerfile": "FROM python:3.11-slim\n\nWORKDIR /app\n\n# Install system dependencies\nRUN apt-get update && apt-get install -y \\\n    gcc \\\n    && rm -rf /var/lib/apt/lists/*\n\n# Copy requirements\nCOPY requirements.txt .\n\n# Install Python dependencies\nRUN pip install --no-cache-dir -r requirements.txt\n\n# Copy application code\nCOPY . .\n\n# Create non-root user\nRUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app\nUSER appuser\n\n# Expose port\nEXPOSE 8000\n\n# Run application\nCMD [\"uvicorn\", \"app.main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]",

**This is CORRECT** - pure JSON with no code fences:            "docker-compose.yml": "version: '3.8'\n\nservices:\n  api:\n    build: .\n    ports:\n      - \"8000:8000\"\n    environment:\n      - REDIS_HOST=redis\n      - REDIS_PORT=6379\n    env_file:\n      - .env\n    depends_on:\n      - redis\n    restart: unless-stopped\n\n  redis:\n    image: redis:alpine\n    ports:\n      - \"6379:6379\"\n    volumes:\n      - redis_data:/data\n    restart: unless-stopped\n\nvolumes:\n  redis_data:",

            "pytest.ini": "[pytest]\npythonpath = .\ntestpaths = tests\npython_files = test_*.py\npython_classes = Test*\npython_functions = test_*\naddopts = \n    -v\n    --strict-markers\n    --tb=short\n    --asyncio-mode=auto\nmarkers =\n    slow: marks tests as slow\n    integration: marks tests as integration tests",

{            ".pre-commit-config.yaml": "repos:\n  - repo: https://github.com/pre-commit/pre-commit-hooks\n    rev: v4.5.0\n    hooks:\n      - id: trailing-whitespace\n      - id: end-of-file-fixer\n      - id: check-yaml\n      - id: check-added-large-files\n\n  - repo: https://github.com/psf/black\n    rev: 23.12.0\n    hooks:\n      - id: black\n\n  - repo: https://github.com/pycqa/isort\n    rev: 5.13.2\n    hooks:\n      - id: isort\n\n  - repo: https://github.com/pycqa/flake8\n    rev: 6.1.0\n    hooks:\n      - id: flake8\n        args: [--max-line-length=100, --ignore=E203 W503]",

    "project_name": "my-project",            "app/__init__.py": "",

    "description": "A production-ready application",            "app/main.py": "\"\"\"Main FastAPI application module.\"\"\"\nimport logging\nfrom contextlib import asynccontextmanager\n\nfrom fastapi import FastAPI\nfrom fastapi.middleware.cors import CORSMiddleware\nfrom fastapi.responses import JSONResponse\nfrom prometheus_fastapi_instrumentator import Instrumentator\nfrom slowapi import Limiter, _rate_limit_exceeded_handler\nfrom slowapi.errors import RateLimitExceeded\nfrom slowapi.util import get_remote_address\n\nfrom app.api.v1 import series\nfrom app.core.config import settings\nfrom app.core.logging_config import setup_logging\nfrom app.services.cache import cache_service\n\n# Setup logging\nsetup_logging()\nlogger = logging.getLogger(__name__)\n\n# Initialize rate limiter\nlimiter = Limiter(key_func=get_remote_address)\n\n\n@asynccontextmanager\nasync def lifespan(app: FastAPI):\n    \"\"\"Application lifespan manager.\"\"\"\n    logger.info(\"Starting up BLS Data API...\")\n    await cache_service.connect()\n    yield\n    logger.info(\"Shutting down BLS Data API...\")\n    await cache_service.disconnect()\n\n\n# Create FastAPI app\napp = FastAPI(\n    title=settings.APP_NAME,\n    description=\"API for querying Bureau of Labor Statistics data\",\n    version=settings.APP_VERSION,\n    lifespan=lifespan,\n    docs_url=\"/docs\",\n    redoc_url=\"/redoc\",\n)\n\n# Add rate limiter\napp.state.limiter = limiter\napp.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)\n\n# Add CORS middleware\napp.add_middleware(\n    CORSMiddleware,\n    allow_origins=settings.CORS_ORIGINS,\n    allow_credentials=True,\n    allow_methods=[\"*\"],\n    allow_headers=[\"*\"],\n)\n\n# Add Prometheus metrics\nInstrumentator().instrument(app).expose(app)\n\n# Include routers\napp.include_router(series.router, prefix=\"/api/v1\", tags=[\"Series\"])\n\n\n@app.get(\"/\", include_in_schema=False)\nasync def root():\n    \"\"\"Root endpoint.\"\"\"\n    return {\n        \"name\": settings.APP_NAME,\n        \"version\": settings.APP_VERSION,\n        \"status\": \"running\",\n    }\n\n\n@app.get(\"/health\")\nasync def health_check():\n    \"\"\"Health check endpoint.\"\"\"\n    redis_status = \"healthy\" if await cache_service.ping() else \"unhealthy\"\n    return {\n        \"status\": \"healthy\",\n        \"redis\": redis_status,\n        \"version\": settings.APP_VERSION,\n    }\n\n\n@app.exception_handler(Exception)\nasync def global_exception_handler(request, exc):\n    \"\"\"Global exception handler.\"\"\"\n    logger.error(f\"Unhandled exception: {exc}\", exc_info=True)\n    return JSONResponse(\n        status_code=500,\n        content={\"detail\": \"Internal server error\"},\n    )",

    "structure": {            "app/core/__init__.py": "",

        "folders": ["src", "tests"],            "app/core/config.py": "\"\"\"Application configuration.\"\"\"\nfrom typing import List\n\nfrom pydantic_settings import BaseSettings, SettingsConfigDict\n\n\nclass Settings(BaseSettings):\n    \"\"\"Application settings.\"\"\"\n\n    model_config = SettingsConfigDict(\n        env_file=\".env\",\n        env_file_encoding=\"utf-8\",\n        case_sensitive=False,\n    )\n\n    # Application\n    APP_NAME: str = \"BLS Data API\"\n    APP_VERSION: str = \"1.0.0\"\n    ENVIRONMENT: str = \"development\"\n    DEBUG: bool = False\n\n    # BLS API\n    BLS_API_KEY: str = \"\"\n    BLS_API_BASE_URL: str = \"https://api.bls.gov/publicAPI/v2\"\n    BLS_API_TIMEOUT: int = 30\n    BLS_API_MAX_RETRIES: int = 3\n\n    # Redis\n    REDIS_HOST: str = \"localhost\"\n    REDIS_PORT: int = 6379\n    REDIS_DB: int = 0\n    REDIS_PASSWORD: str = \"\"\n    CACHE_TTL: int = 3600\n\n    # Security\n    API_KEY_HEADER: str = \"X-API-Key\"\n    ALLOWED_HOSTS: str = \"*\"\n    CORS_ORIGINS: List[str] = [\"*\"]\n\n    # Rate Limiting\n    RATE_LIMIT_PER_MINUTE: int = 60\n    RATE_LIMIT_PER_HOUR: int = 1000\n\n    # Logging\n    LOG_LEVEL: str = \"INFO\"\n\n    @property\n    def redis_url(self) -> str:\n        \"\"\"Construct Redis URL.\"\"\"\n        if self.REDIS_PASSWORD:\n            return f\"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}\"\n        return f\"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}\"\n\n\nsettings = Settings()",

        "files": {            "app/core/logging_config.py": "\"\"\"Logging configuration.\"\"\"\nimport logging\nimport sys\n\nfrom app.core.config import settings\n\n\ndef setup_logging():\n    \"\"\"Configure application logging.\"\"\"\n    log_level = getattr(logging, settings.LOG_LEVEL.upper())\n\n    # Create formatter\n    formatter = logging.Formatter(\n        \"%(asctime)s - %(name)s - %(levelname)s - %(message)s\",\n        datefmt=\"%Y-%m-%d %H:%M:%S\",\n    )\n\n    # Configure root logger\n    root_logger = logging.getLogger()\n    root_logger.setLevel(log_level)\n\n    # Console handler\n    console_handler = logging.StreamHandler(sys.stdout)\n    console_handler.setLevel(log_level)\n    console_handler.setFormatter(formatter)\n    root_logger.addHandler(console_handler)\n\n    # Reduce noise from third-party libraries\n    logging.getLogger(\"httpx\").setLevel(logging.WARNING)\n    logging.getLogger(\"httpcore\").setLevel(logging.WARNING)\n    logging.getLogger(\"redis\").setLevel(logging.WARNING)",

            "src/main.py": "# Application entry point",            "app/api/__init__.py": "",

            "README.md": "# My Project"            "app/api/v1/__init__.py": "",

        }            "app/api/v1/series.py": "\"\"\"Series API endpoints.\"\"\"\nimport logging\nfrom typing import List, Optional\n\nfrom fastapi import APIRouter, Depends, HTTPException, Query, Request\nfrom slowapi import Limiter\nfrom slowapi.util import get_remote_address\n\nfrom app.core.config import settings\nfrom app.schemas.series import (\n    BatchSeriesRequest,\n    BatchSeriesResponse,\n    SeriesResponse,\n)\nfrom app.services.bls_client import bls_client\n\nlogger = logging.getLogger(__name__)\nrouter = APIRouter()\nlimiter = Limiter(key_func=get_remote_address)\n\n\n@router.get(\"/series/{series_id}\", response_model=SeriesResponse)\n@limiter.limit(f\"{settings.RATE_LIMIT_PER_MINUTE}/minute\")\nasync def get_series(\n    request: Request,\n    series_id: str,\n    start_year: str = Query(..., description=\"Start year (YYYY)\", regex=\"^\\\\d{4}$\"),\n    end_year: str = Query(..., description=\"End year (YYYY)\", regex=\"^\\\\d{4}$\"),\n    catalog: bool = Query(False, description=\"Include catalog metadata\"),\n) -> SeriesResponse:\n    \"\"\"Get BLS series data for a single series.\n\n    Args:\n        request: FastAPI request object\n        series_id: BLS series identifier (e.g., 'LAUCN040010000000005')\n        start_year: Start year for data (YYYY format)\n        end_year: End year for data (YYYY format)\n        catalog: Include catalog metadata\n\n    Returns:\n        SeriesResponse with data and metadata\n\n    Raises:\n        HTTPException: If series not found or API error occurs\n    \"\"\"\n    logger.info(f\"Fetching series {series_id} from {start_year} to {end_year}\")\n\n    try:\n        result = await bls_client.get_series(\n            series_ids=[series_id],\n            start_year=start_year,\n            end_year=end_year,\n            catalog=catalog,\n        )\n\n        if not result or \"seriesID\" not in result:\n            raise HTTPException(status_code=404, detail=\"Series not found\")\n\n        return SeriesResponse(\n            series_id=result[\"seriesID\"],\n            data=result.get(\"data\", []),\n            catalog=result.get(\"catalog\"),\n        )\n\n    except ValueError as e:\n        logger.error(f\"Validation error: {e}\")\n        raise HTTPException(status_code=400, detail=str(e))\n    except Exception as e:\n        logger.error(f\"Error fetching series: {e}\", exc_info=True)\n        raise HTTPException(status_code=500, detail=\"Failed to fetch series data\")\n\n\n@router.post(\"/series/batch\", response_model=BatchSeriesResponse)\n@limiter.limit(f\"{settings.RATE_LIMIT_PER_MINUTE}/minute\")\nasync def get_batch_series(\n    request: Request,\n    batch_request: BatchSeriesRequest,\n) -> BatchSeriesResponse:\n    \"\"\"Get BLS series data for multiple series.\n\n    Args:\n        request: FastAPI request object\n        batch_request: Batch request with series IDs and date range\n\n    Returns:\n        BatchSeriesResponse with data for all requested series\n\n    Raises:\n        HTTPException: If API error occurs\n    \"\"\"\n    logger.info(\n        f\"Fetching batch of {len(batch_request.series_ids)} series \"\n        f\"from {batch_request.start_year} to {batch_request.end_year}\"\n    )\n\n    try:\n        results = await bls_client.get_series(\n            series_ids=batch_request.series_ids,\n            start_year=batch_request.start_year,\n            end_year=batch_request.end_year,\n            catalog=batch_request.catalog,\n        )\n\n        series_list = [\n            SeriesResponse(\n                series_id=series[\"seriesID\"],\n                data=series.get(\"data\", []),\n                catalog=series.get(\"catalog\"),\n            )\n            for series in results\n        ]\n\n        return BatchSeriesResponse(series=series_list)\n\n    except ValueError as e:\n        logger.error(f\"Validation error: {e}\")\n        raise HTTPException(status_code=400, detail=str(e))\n    except Exception as e:\n        logger.error(f\"Error fetching batch series: {e}\", exc_info=True)\n        raise HTTPException(status_code=500, detail=\"Failed to fetch series data\")",

    }            "app/schemas/__init__.py": "",

}            "app/schemas/series.py": "\"\"\"Series data schemas.\"\"\"\nfrom typing import Any, Dict, List, Optional\n\nfrom pydantic import BaseModel, Field, field_validator\n\n\nclass SeriesDataPoint(BaseModel):\n    \"\"\"Individual data point in a series.\"\"\"\n\n    year: str\n    period: str\n    period_name: str = Field(alias=\"periodName\")\n    value: str\n    footnotes: Optional[List[Dict[str, Any]]] = None\n\n    class Config:\n        populate_by_name = True\n\n\nclass SeriesResponse(BaseModel):\n    \"\"\"Response for a single series.\"\"\"\n\n    series_id: str = Field(..., description=\"BLS series identifier\")\n    data: List[SeriesDataPoint] = Field(default_factory=list)\n    catalog: Optional[Dict[str, Any]] = None\n\n\nclass BatchSeriesRequest(BaseModel):\n    \"\"\"Request for multiple series.\"\"\"\n\n    series_ids: List[str] = Field(\n        ...,\n        min_length=1,\n        max_length=50,\n        description=\"List of BLS series identifiers (max 50)\",\n    )\n    start_year: str = Field(..., description=\"Start year (YYYY)\", pattern=\"^\\\\d{4}$\")\n    end_year: str = Field(..., description=\"End year (YYYY)\", pattern=\"^\\\\d{4}$\")\n    catalog: bool = Field(False, description=\"Include catalog metadata\")\n\n    @field_validator(\"series_ids\")\n    @classmethod\n    def validate_series_ids(cls, v: List[str]) -> List[str]:\n        \"\"\"Validate series IDs.\"\"\"\n        if not v:\n            raise ValueError(\"At least one series ID is required\")\n        if len(v) > 50:\n            raise ValueError(\"Maximum 50 series IDs allowed\")\n        return v\n\n    @field_validator(\"end_year\")\n    @classmethod\n    def validate_years(cls, v: str, info) -> str:\n        \"\"\"Validate year range.\"\"\"\n        if \"start_year\" in info.data:\n            start = int(info.data[\"start_year\"])\n            end = int(v)\n            if end < start:\n                raise ValueError(\"End year must be greater than or equal to start year\")\n            if end - start > 20:\n                raise ValueError(\"Date range cannot exceed 20 years\")\n        return v\n\n\nclass BatchSeriesResponse(BaseModel):\n    \"\"\"Response for multiple series.\"\"\"\n\n    series: List[SeriesResponse]",

            "app/services/__init__.py": "",

---            "app/services/bls_client.py": "\"\"\"BLS API client service.\"\"\"\nimport hashlib\nimport json\nimport logging\nfrom typing import Any, Dict, List, Optional\n\nimport httpx\n\nfrom app.core.config import settings\nfrom app.services.cache import cache_service\n\nlogger = logging.getLogger(__name__)\n\n\nclass BLSClient:\n    \"\"\"Client for interacting with BLS API.\"\"\"\n\n    def __init__(self):\n        self.base_url = settings.BLS_API_BASE_URL\n        self.api_key = settings.BLS_API_KEY\n        self.timeout = settings.BLS_API_TIMEOUT\n        self.max_retries = settings.BLS_API_MAX_RETRIES\n\n    def _generate_cache_key(self, series_ids: List[str], start_year: str, end_year: str) -> str:\n        \"\"\"Generate cache key for request.\"\"\"\n        key_string = f\"{','.join(sorted(series_ids))}:{start_year}:{end_year}\"\n        return f\"bls:series:{hashlib.md5(key_string.encode()).hexdigest()}\"\n\n    async def get_series(\n        self,\n        series_ids: List[str],\n        start_year: str,\n        end_year: str,\n        catalog: bool = False,\n    ) -> List[Dict[str, Any]]:\n        \"\"\"Fetch series data from BLS API.\n\n        Args:\n            series_ids: List of BLS series identifiers\n            start_year: Start year (YYYY)\n            end_year: End year (YYYY)\n            catalog: Include catalog metadata\n\n        Returns:\n            List of series data\n\n        Raises:\n            ValueError: If validation fails\n            httpx.HTTPError: If API request fails\n        \"\"\"\n        # Validate inputs\n        if not series_ids:\n            raise ValueError(\"At least one series ID required\")\n        if len(series_ids) > 50:\n            raise ValueError(\"Maximum 50 series IDs allowed\")\n\n        # Check cache\n        cache_key = self._generate_cache_key(series_ids, start_year, end_year)\n        cached_data = await cache_service.get(cache_key)\n        if cached_data:\n            logger.info(f\"Cache hit for {cache_key}\")\n            return json.loads(cached_data)\n\n        # Prepare request\n        payload = {\n            \"seriesid\": series_ids,\n            \"startyear\": start_year,\n            \"endyear\": end_year,\n            \"catalog\": catalog,\n        }\n\n        if self.api_key:\n            payload[\"registrationkey\"] = self.api_key\n\n        logger.info(f\"Fetching data from BLS API for {len(series_ids)} series\")\n\n        async with httpx.AsyncClient(timeout=self.timeout) as client:\n            for attempt in range(self.max_retries):\n                try:\n                    response = await client.post(\n                        f\"{self.base_url}/timeseries/data/\",\n                        json=payload,\n                    )\n                    response.raise_for_status()\n                    data = response.json()\n\n                    if data.get(\"status\") != \"REQUEST_SUCCEEDED\":\n                        error_msg = data.get(\"message\", [\"Unknown error\"])\n                        raise ValueError(f\"BLS API error: {error_msg}\")\n\n                    results = data.get(\"Results\", {}).get(\"series\", [])\n\n                    # Cache results\n                    await cache_service.set(\n                        cache_key,\n                        json.dumps(results),\n                        ttl=settings.CACHE_TTL,\n                    )\n\n                    return results\n\n                except httpx.HTTPError as e:\n                    logger.warning(\n                        f\"HTTP error on attempt {attempt + 1}/{self.max_retries}: {e}\"\n                    )\n                    if attempt == self.max_retries - 1:\n                        raise\n                except Exception as e:\n                    logger.error(f\"Unexpected error: {e}\", exc_info=True)\n                    raise\n\n        return []\n\n\nbls_client = BLSClient()",

            "app/services/cache.py": "\"\"\"Redis cache service.\"\"\"\nimport logging\nfrom typing import Optional\n\nimport redis.asyncio as redis\n\nfrom app.core.config import settings\n\nlogger = logging.getLogger(__name__)\n\n\nclass CacheService:\n    \"\"\"Redis cache service for caching API responses.\"\"\"\n\n    def __init__(self):\n        self.redis_client: Optional[redis.Redis] = None\n\n    async def connect(self):\n        \"\"\"Connect to Redis.\"\"\"\n        try:\n            self.redis_client = redis.from_url(\n                settings.redis_url,\n                encoding=\"utf-8\",\n                decode_responses=True,\n            )\n            await self.redis_client.ping()\n            logger.info(\"Connected to Redis successfully\")\n        except Exception as e:\n            logger.error(f\"Failed to connect to Redis: {e}\")\n            self.redis_client = None\n\n    async def disconnect(self):\n        \"\"\"Disconnect from Redis.\"\"\"\n        if self.redis_client:\n            await self.redis_client.close()\n            logger.info(\"Disconnected from Redis\")\n\n    async def get(self, key: str) -> Optional[str]:\n        \"\"\"Get value from cache.\n\n        Args:\n            key: Cache key\n\n        Returns:\n            Cached value or None\n        \"\"\"\n        if not self.redis_client:\n            return None\n\n        try:\n            value = await self.redis_client.get(key)\n            return value\n        except Exception as e:\n            logger.error(f\"Cache get error: {e}\")\n            return None\n\n    async def set(self, key: str, value: str, ttl: int = 3600) -> bool:\n        \"\"\"Set value in cache.\n\n        Args:\n            key: Cache key\n            value: Value to cache\n            ttl: Time to live in seconds\n\n        Returns:\n            True if successful, False otherwise\n        \"\"\"\n        if not self.redis_client:\n            return False\n\n        try:\n            await self.redis_client.setex(key, ttl, value)\n            return True\n        except Exception as e:\n            logger.error(f\"Cache set error: {e}\")\n            return False\n\n    async def delete(self, key: str) -> bool:\n        \"\"\"Delete key from cache.\n\n        Args:\n            key: Cache key\n\n        Returns:\n            True if successful, False otherwise\n        \"\"\"\n        if not self.redis_client:\n            return False\n\n        try:\n            await self.redis_client.delete(key)\n            return True\n        except Exception as e:\n            logger.error(f\"Cache delete error: {e}\")\n            return False\n\n    async def ping(self) -> bool:\n        \"\"\"Check Redis connection.\n\n        Returns:\n            True if connected, False otherwise\n        \"\"\"\n        if not self.redis_client:\n            return False\n\n        try:\n            await self.redis_client.ping()\n            return True\n        except Exception:\n            return False\n\n\ncache_service = CacheService()",

## Summary            "app/models/__init__.py": "",

            "app/utils/__init__.py": "",

- ✅ **Return**: Raw JSON object only            "tests/__init__.py": "",

- ❌ **Don't return**: Code fences, markdown formatting, or explanatory text              "tests/conftest.py": "\"\"\"Pytest configuration and fixtures.\"\"\"\nimport pytest\nfrom fastapi.testclient import TestClient\n\nfrom app.main import app\n\n\n@pytest.fixture\ndef client():\n    \"\"\"Create test client.\"\"\"\n    return TestClient(app)\n\n\n@pytest.fixture\ndef mock_bls_response():\n    \"\"\"Mock BLS API response.\"\"\"\n

- 🎯 **Goal**: Production-ready project scaffolds with best practices

            - above bad example does not return valid json and includes ```json in the response