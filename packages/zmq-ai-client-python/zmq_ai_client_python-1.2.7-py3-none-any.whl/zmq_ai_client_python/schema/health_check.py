from dataclasses import dataclass

from zmq_ai_client_python.schema.base import Base


@dataclass
class HealthCheck(Base):
    """
    Dataclass representing a health check response.
    """
    status: str
    host: str
    worker_count: int
