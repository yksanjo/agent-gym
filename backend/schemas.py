from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

from models import AgentStatus, FeedbackType, ABTestStatus, FineTuningStatus

# Base schemas
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

# User schemas
class UserBase(BaseSchema):
    email: str
    name: Optional[str] = None
    role: Optional[str] = "user"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

# Organization schemas
class OrganizationBase(BaseSchema):
    name: str
    plan: Optional[str] = "free"
    settings: Optional[Dict[str, Any]] = {}

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationResponse(OrganizationBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

# Agent schemas
class AgentBase(BaseSchema):
    name: str
    description: Optional[str] = None
    model_type: Optional[str] = None
    model_config: Optional[Dict[str, Any]] = {}
    metadata: Optional[Dict[str, Any]] = {}

class AgentCreate(AgentBase):
    owner_id: Optional[str] = None
    organization_id: Optional[str] = None

class AgentUpdate(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[AgentStatus] = None
    model_config: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

class AgentResponse(AgentBase):
    id: str
    owner_id: Optional[str] = None
    organization_id: Optional[str] = None
    status: AgentStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

# Agent Execution schemas
class AgentExecutionBase(BaseSchema):
    input_data: Dict[str, Any]
    context: Optional[Dict[str, Any]] = {}
    metadata: Optional[Dict[str, Any]] = {}

class AgentExecutionCreate(AgentExecutionBase):
    pass

class AgentExecutionResponse(AgentExecutionBase):
    id: str
    agent_id: str
    output_data: Optional[Dict[str, Any]] = None
    success: Optional[bool] = None
    execution_time_ms: Optional[int] = None
    cost: Optional[float] = None
    created_at: datetime

# Feedback schemas
class FeedbackBase(BaseSchema):
    type: FeedbackType
    rating: Optional[int] = Field(None, ge=1, le=5)
    correction: Optional[str] = None
    comment: Optional[str] = None
    binary_feedback: Optional[bool] = None
    reviewer_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}

class FeedbackCreate(FeedbackBase):
    execution_id: str

class FeedbackResponse(FeedbackBase):
    id: str
    agent_id: str
    execution_id: str
    created_at: datetime

# A/B Testing schemas
class ABTestBase(BaseSchema):
    name: str
    description: Optional[str] = None
    traffic_split: Dict[str, float] = {"variant_a": 0.5, "variant_b": 0.5}
    metrics: Optional[List[str]] = ["success_rate", "avg_execution_time", "avg_rating"]
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = {}

class ABTestCreate(ABTestBase):
    pass

class ABTestResponse(ABTestBase):
    id: str
    agent_id: str
    status: ABTestStatus
    winner_variant_id: Optional[str] = None
    confidence_level: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

class ABTestVariantBase(BaseSchema):
    name: str
    model_version_id: str
    traffic_percentage: float
    metadata: Optional[Dict[str, Any]] = {}

class ABTestVariantCreate(ABTestVariantBase):
    pass

class ABTestVariantResponse(ABTestVariantBase):
    id: str
    ab_test_id: str
    created_at: datetime

class ABTestResultBase(BaseSchema):
    executions_count: int = 0
    success_count: int = 0
    avg_execution_time: Optional[float] = None
    avg_cost: Optional[float] = None
    avg_rating: Optional[float] = None
    metrics: Optional[Dict[str, Any]] = {}
    period_start: datetime
    period_end: datetime

class ABTestResultResponse(ABTestResultBase):
    id: str
    ab_test_id: str
    variant_id: str
    created_at: datetime

# Fine-tuning schemas
class FineTuningJobBase(BaseSchema):
    name: str
    description: Optional[str] = None
    training_dataset_id: str
    base_model_version_id: str
    hyperparameters: Optional[Dict[str, Any]] = {}
    metadata: Optional[Dict[str, Any]] = {}

class FineTuningJobCreate(FineTuningJobBase):
    pass

class FineTuningJobResponse(FineTuningJobBase):
    id: str
    agent_id: str
    status: FineTuningStatus
    new_model_version_id: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

# Training Dataset schemas
class TrainingDatasetBase(BaseSchema):
    name: str
    description: Optional[str] = None
    source_type: str = "feedback"
    data: List[Dict[str, Any]]
    statistics: Optional[Dict[str, Any]] = {}
    metadata: Optional[Dict[str, Any]] = {}

class TrainingDatasetCreate(TrainingDatasetBase):
    pass

class TrainingDatasetResponse(TrainingDatasetBase):
    id: str
    created_at: datetime

# Model Version schemas
class ModelVersionBase(BaseSchema):
    version: str
    model_path: str
    performance_metrics: Optional[Dict[str, Any]] = {}
    training_data_hash: Optional[str] = None
    is_production: bool = False
    metadata: Optional[Dict[str, Any]] = {}

class ModelVersionCreate(ModelVersionBase):
    pass

class ModelVersionResponse(ModelVersionBase):
    id: str
    agent_id: str
    created_at: datetime

# Synthetic Scenario schemas
class SyntheticScenarioBase(BaseSchema):
    name: str
    description: Optional[str] = None
    scenario_type: str = "common"
    input_data: Dict[str, Any]
    expected_output: Optional[Dict[str, Any]] = None
    difficulty: Optional[int] = Field(1, ge=1, le=5)
    tags: Optional[List[str]] = []
    metadata: Optional[Dict[str, Any]] = {}

class SyntheticScenarioCreate(SyntheticScenarioBase):
    pass

class SyntheticScenarioResponse(SyntheticScenarioBase):
    id: str
    agent_id: Optional[str] = None
    created_at: datetime

# Analytics schemas
class AgentMetricsResponse(BaseSchema):
    total_executions: int
    success_rate: float
    avg_execution_time_ms: float
    avg_cost: float
    last_execution: Optional[str] = None

class FeedbackSummaryResponse(BaseSchema):
    total_feedback: int
    avg_rating: Optional[float] = None
    rating_distribution: Dict[int, int]
    feedback_types: Dict[str, int]

class ABTestSummaryResponse(BaseSchema):
    total_tests: int
    active_tests: int
    completed_tests: int
    avg_improvement: Optional[float] = None
    test_distribution: Dict[str, int]