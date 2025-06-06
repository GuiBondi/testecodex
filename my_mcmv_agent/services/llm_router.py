"""Interface to Google Vertex AI (Gemini) for LLM calls."""
from google.cloud import aiplatform
from google.cloud.aiplatform.gapic import PredictionServiceClient
from google.cloud.aiplatform.gapic.schema import predict

from ..utils.config import GEMINI_API_ENDPOINT, GOOGLE_CLOUD_PROJECT


aiplatform.init(project=GOOGLE_CLOUD_PROJECT, api_endpoint=GEMINI_API_ENDPOINT)
_client = PredictionServiceClient(client_options={"api_endpoint": GEMINI_API_ENDPOINT})
_model_path = f"projects/{GOOGLE_CLOUD_PROJECT}/locations/us-central1/publishers/google/models/chat-bison-001"


def call_gemini(prompt: str) -> str:
    """Send prompt to Gemini model and return generated text."""
    instance = predict.instance.TextPrompt(text=prompt)
    instances = [instance]
    parameters = predict.params.TextGenerationParams(temperature=0.7, max_output_tokens=512)
    response = _client.predict(endpoint=_model_path, instances=instances, parameters=parameters)
    predictions = response.predictions
    if predictions:
        content = predictions[0].get("content", "")
        return content
    return ""
