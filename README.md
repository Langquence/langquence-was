# Langquence API

A FastAPI-based English correction service designed for Korean speakers preparing for English interviews. This service utilizes Large Language Models to analyze and improve English expressions, making them more natural and professional.

## Project Overview

Langquence API is part of a larger system designed to help Korean speakers improve their English interview skills. The system consists of multiple layers:

1. **Data Collection Layer**: Collects English interview data from sources like YouTube
2. **Data Processing Layer**: Processes the collected data including speech-to-text conversion
3. **Model Learning Layer**: Trains NLP models using the processed data
4. **Realtime Processing Layer (this project)**: Provides real-time English correction via API
5. **Presentation Layer**: User interfaces for interacting with the service

This repository implements the Realtime Processing Layer as a FastAPI application.

## Architecture

The application follows a modular architecture with clear separation of concerns:

```
langquence-was/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── api/                 # API routes
│   ├── config/              # Configuration management
│   ├── consts/              
│   ├── clients/             # External service clients
│   ├── services/            # Business logic
│   ├── dto/                 
│   └── utils/               
├── .env                     # Environment variables
└── requirements.txt         # Dependencies
```

### Key Components

- **API Layer**: Handles HTTP requests and responses
- **Correction Service**: Orchestrates the correction process
- **Qwen Client**: Interacts with Alibaba Cloud's Qwen LLM API
- **Pattern Matching Engine**: Validates and enhances LLM responses
- **Feedback Generator**: Creates user-friendly feedback from corrections

## Getting Started

### Prerequisites

- Python 3.8+
- An Alibaba Cloud account with access to DashScope API

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/langquence-was.git
cd langquence-was
```

2. Create and activate a virtual environment:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with the following contents:
```
APP_NAME=Langquence API
APP_EXECUTE_COMMAND=app.main:app
APP_HOST=127.0.0.1
APP_PORT=8000
APP_RELOAD=True
API_PREFIX=/api
DEBUG=True
LOG_LEVEL=INFO
ALIBABA_API_KEY=your_api_key_here
MODEL_NAME=qwen-plus
MAX_TOKENS=512
```

### Running the Application

Run the application using Uvicorn:

```bash
uvicorn app.main:app --reload
```

Or use the provided entry point:

```bash
python -m app.main
```

The API will be available at: http://localhost:8000

## API Usage

### Correction Endpoint

Corrects English text for interview settings.

**Endpoint**: `POST /api/correct`

**Request**:
```json
{
  "text": "I have work in this company for 5 years."
}
```

**Response**:
```json
{
  "original": "I have work in this company for 5 years.",
  "needs_correction": true,
  "corrected": "I have worked in this company for 5 years.",
  "explanation": "Changed 'work' to 'worked' to use present perfect tense correctly for an action that started in the past and continues to the present.",
  "alternatives": ["I have been working in this company for 5 years."]
}
```

## Architecture Details

### Pattern Matching Engine

The Pattern Matching Engine validates and enhances the LLM's corrections by:

1. Checking if the LLM identified errors correctly
2. Comparing against known error patterns
3. Providing additional validation for the corrections
4. Suggesting alternative expressions when appropriate

### Prompting Strategy

The application uses a carefully designed prompting strategy that:

1. Provides clear instructions to the LLM
2. Specifies the expected response format
3. Includes examples of common errors and corrections
4. Guides the model to produce consistent, high-quality responses

## Development

### Adding New Features

To add new features to the application:

1. Implement traffic rate limitation
2. Enhance security policies
3. Optimize prompt token usage
4. Refactoring the Architecture

### Testing

To run tests:

```bash
pytest
```