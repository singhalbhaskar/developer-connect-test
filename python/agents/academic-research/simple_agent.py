import json
from typing import Any

from google.adk.agents import llm_agent
from google.adk.sessions import in_memory_session_service
import google.auth
import vertexai
from vertexai.preview.reasoning_engines import AdkApp


InMemorySessionService = in_memory_session_service.InMemorySessionService


class ProductNameGenerator:
  """Generates product names using an ADK application."""

  def __init__(self, project_id):

    self.project_id = project_id
    self.app = None

  def session_service_builder(self):
    """Builds the session service to use in the ADK app."""
    return InMemorySessionService()

  def set_up(self):
    """Sets up the Vertex AI environment and the ADK application."""

    creds, _ = google.auth.default(quota_project_id=self.project_id)

    vertexai.init(
        project=self.project_id,
        location="us-central1",
        credentials=creds,
    )

    root_agent = llm_agent.LlmAgent(
        name="ProductNameGeneratorAgent",
        model="gemini-2.5-flash",
        description="Agent to generate product names.",
    )

    self.app = AdkApp(
        agent=root_agent,
        enable_tracing=True,
        session_service_builder=self.session_service_builder,
    )

  def stream_query(self, product: str) -> Any:
    for chunk in self.app.stream_query(
        message=f"What is a funny name for a company that makes {product}?",
        user_id="test",
    ):
      yield chunk


class FixedProductNameGenerator():

  def stream_query(self, product: str) -> Any:
    response_data = {
        "output": "updated-reasoning-engine-prober: expected query response"
    }
    yield json.dumps(response_data)


prod_name_generator = ProductNameGenerator(
    project_id="cloud-aiplatform-prober"
)
staging_name_generator = ProductNameGenerator(
    project_id="ucaip-prober-staging"
)
autopush_name_generator = ProductNameGenerator(
    project_id="ucaip-prober-autopush"
)
fixed_name_generator = FixedProductNameGenerator()
