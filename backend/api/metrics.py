# backend/api/metrics.py
from fastapi import APIRouter, Response
from prometheus_client import CONTENT_TYPE_LATEST
from backend.services.metrics_service import MetricsService

router = APIRouter()

@router.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint"""
    metrics_data = MetricsService.get_metrics()
    return Response(
        content=metrics_data,
        media_type=CONTENT_TYPE_LATEST,
        headers={"Cache-Control": "no-cache"}
    )