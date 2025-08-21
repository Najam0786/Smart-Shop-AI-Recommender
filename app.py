import uuid
from flask import Flask, render_template, request, Response, session

# --- Prometheus Metrics ---
from prometheus_client import Counter, generate_latest

# --- Custom Modules ---
from config.config import AppConfig
from utils.data_ingestion import DataIngestor
from chain.rag_chain import create_rag_chain
from utils.logger import setup_logger
from utils.custom_exception import CustomException

# ==============================================================================
# 1. INITIAL SETUP
# ==============================================================================

# Initialize a logger for the application
logger = setup_logger(__name__)

# Initialize Prometheus metrics to monitor application health
REQUEST_COUNT = Counter("http_requests_total", "Total number of HTTP requests")
SUCCESS_COUNT = Counter("http_requests_success_total", "Total number of successful responses")
ERROR_COUNT = Counter("http_requests_error_total", "Total number of error responses")

# ==============================================================================
# 2. APPLICATION FACTORY
# ==============================================================================

def create_app() -> Flask:
    """
    Creates and configures the Flask application.
    This pattern is useful for scaling and testing.
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = AppConfig.FLASK_SECRET_KEY
    logger.info("Flask application created with secret key.")

    # --- Initialize Core Services (Vector Store & RAG Chain) ---
    # This is done once when the application starts for efficiency.
    try:
        logger.info("Initializing core services...")
        # We only need to get the vector store connection, not ingest data again.
        vector_store = DataIngestor().vstore
        # Create the conversational RAG chain
        rag_chain = create_rag_chain(vector_store)
        logger.info("Core services (Vector Store, RAG Chain) initialized successfully.")
    except CustomException as e:
        logger.error(f"FATAL: Failed to initialize core services. Application cannot start. Error: {e}")
        # If services fail, the app is non-functional. We exit.
        exit(1)

    # ==========================================================================
    # 3. DEFINE FLASK ROUTES
    # ==========================================================================

    @app.route("/")
    def index() -> str:
        """
        Renders the main chat page.
        Initializes a unique session ID for each user.
        """
        REQUEST_COUNT.inc()
        # If a user doesn't have a session ID, create a new unique one.
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
            logger.info(f"New user session created with ID: {session['session_id']}")
        return render_template("index.html")

    @app.route("/get", methods=["POST"])
    def get_response() -> str:
        """
        Handles POST requests from the chat interface, gets a response from the
        RAG chain, and returns it.
        """
        session_id = session.get('session_id', 'default_session') # Fallback
        try:
            user_input = request.form.get("msg")
            if not user_input:
                logger.warning(f"Received empty message from session {session_id}")
                return "Please provide a message."

            logger.info(f"Received input from session {session_id}: '{user_input}'")

            # Invoke the RAG chain with the user's input and their unique session ID
            response = rag_chain.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": session_id}}
            )["answer"]

            logger.info(f"Generated response for session {session_id}: '{response[:80]}...'")
            SUCCESS_COUNT.inc()
            return response

        except Exception as e:
            logger.error(f"An error occurred handling request for session {session_id}: {e}", exc_info=True)
            ERROR_COUNT.inc()
            # Return a user-friendly error message
            return "I'm sorry, but I encountered an error while processing your request. Please try again."

    @app.route("/metrics")
    def metrics() -> Response:
        """
        Exposes Prometheus metrics for scraping.
        """
        return Response(generate_latest(), mimetype="text/plain")

    return app

# ==============================================================================
# 4. RUN THE APPLICATION
# ==============================================================================

if __name__ == "__main__":
    # Create the Flask app using the factory
    app = create_app()
    # Run the app (debug=False is important for production)
    app.run(host="0.0.0.0", port=5000, debug=False)