import logging
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from backend.config import settings
from backend.schemas.qa import QARequest, QAResponse
from backend.schemas.explanation import ExplainRequest, ExplainResponse
from backend.schemas.quiz import QuizRequest, QuizResponse
from backend.schemas.summary import SummarizeRequest, SummarizeResponse
from backend.schemas.learning_path import LearningPathRequest, LearningPathResponse
from backend.schemas.flashcard import FlashcardRequest, FlashcardResponse
from backend.schemas.code_explainer import CodeExplainRequest, CodeExplainResponse
from backend.schemas.mindmap import MindMapRequest, MindMapResponse
from backend.schemas.study_plan import StudyPlanRequest, StudyPlanResponse

from backend.modules.qna import answer_question
from backend.modules.explanation import explain_topic
from backend.modules.quiz import generate_quiz
from backend.modules.summary import summarize_text
from backend.modules.learning_path import generate_learning_path
from backend.modules.flashcard import generate_flashcards
from backend.modules.code_explainer import explain_code
from backend.modules.mindmap import generate_mindmap
from backend.modules.study_plan import generate_study_plan

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("edugenie")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="EduGenie — Google Gemini Powered Flagship Learning Ecosystem"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static & Templates
app.mount("/static", StaticFiles(directory=str(settings.STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))

# Exception Handlers for Clean JSON Errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error on {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "message": "Invalid request input. Please check the provided data.",
            "details": exc.errors()
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail if isinstance(exc.detail, str) else "HTTP Error",
            "message": str(exc.detail)
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_msg = str(exc)
    logger.error(f"Unhandled exception on {request.url.path}: {error_msg}", exc_info=True)

    if "rate limit" in error_msg.lower() or "quota" in error_msg.lower():
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={
                "error": "Rate Limit Exceeded",
                "message": "EduGenie is receiving a high volume of requests right now. Please wait a moment and try again."
            }
        )
    elif "unavailable" in error_msg.lower() or "503" in error_msg:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "error": "Service Unavailable",
                "message": "The AI service is temporarily unavailable. Please try again in a few moments."
            }
        )
    elif "not configured" in error_msg.lower() or "api_key" in error_msg.lower():
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Configuration Error",
                "message": "EduGenie AI key is missing or invalid. Please configure GEMINI_API_KEY in the server .env file."
            }
        )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "EduGenie couldn't generate a response right now. Please try again."
        }
    )

# Routes

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Renders the main EduGenie single-page web app."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"app_name": settings.PROJECT_NAME, "tagline": settings.TAGLINE}
    )

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

@app.post("/qa", response_model=QAResponse)
async def api_qa(request: QARequest):
    """Answer academic or general educational questions."""
    return answer_question(request)

@app.post("/explain", response_model=ExplainResponse)
async def api_explain(request: ExplainRequest):
    """Explain an educational concept simply."""
    return explain_topic(request)

@app.post("/quiz", response_model=QuizResponse)
async def api_quiz(request: QuizRequest):
    """Generate exactly 3 MCQs based on text or topic."""
    return generate_quiz(request)

@app.post("/summarize", response_model=SummarizeResponse)
async def api_summarize(request: SummarizeRequest):
    """Summarize educational text concisely."""
    return summarize_text(request)

@app.post("/learn/recommendations", response_model=LearningPathResponse)
async def api_learning_path(request: LearningPathRequest):
    """Generate a structured 3-stage personalized learning roadmap."""
    return generate_learning_path(request)

@app.post("/flashcards", response_model=FlashcardResponse)
async def api_flashcards(request: FlashcardRequest):
    """Generate an interactive flashcard study deck."""
    return generate_flashcards(request)

@app.post("/code-explain", response_model=CodeExplainResponse)
async def api_code_explain(request: CodeExplainRequest):
    """Analyze code/algorithm, complexity (Big-O), and refactored code."""
    return explain_code(request)

@app.post("/mindmap", response_model=MindMapResponse)
async def api_mindmap(request: MindMapRequest):
    """Generate a hierarchical mind map knowledge graph."""
    return generate_mindmap(request)

@app.post("/study-plan", response_model=StudyPlanResponse)
async def api_study_plan(request: StudyPlanRequest):
    """Generate a daily structured study & exam revision schedule."""
    return generate_study_plan(request)
