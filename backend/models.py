from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime, 
    Float, ForeignKey, JSON, Enum, BigInteger
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from datetime import datetime

from database import Base

class AgentStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    TRAINING = "training"
    ERROR = "error"

class FeedbackType(str, enum.Enum):
    RATING = "rating"
    CORRECTION = "correction"
    COMMENT = "comment"
    BINARY = "binary"

class ABTestStatus(str, enum.Enum):
    DRAFT = "draft"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class FineTuningStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    role = Column(String, default="user")
    organization_id = Column(String, ForeignKey("organizations.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    organization = relationship("Organization", back_populates="users")
    agents = relationship("Agent", back_populates="owner")

class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    plan = Column(String, default="free")
    settings = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    users = relationship("User", back_populates="organization")
    agents = relationship("Agent", back_populates="organization")

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    owner_id = Column(String, ForeignKey("users.id"))
    organization_id = Column(String, ForeignKey("organizations.id"))
    model_type = Column(String)
    model_config = Column(JSON)
    status = Column(Enum(AgentStatus), default=AgentStatus.ACTIVE)
    metadata = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    owner = relationship("User", back_populates="agents")
    organization = relationship("Organization", back_populates="agents")
    executions = relationship("AgentExecution", back_populates="agent")
    feedback = relationship("Feedback", back_populates="agent")
    ab_tests = relationship("ABTest", back_populates="agent")
    fine_tuning_jobs = relationship("FineTuningJob", back_populates="agent")
    model_versions = relationship("ModelVersion", back_populates="agent")

class AgentExecution(Base):
    __tablename__ = "agent_executions"
    
    id = Column(String, primary_key=True, index=True)
    agent_id = Column(String, ForeignKey("agents.id"))
    input_data = Column(JSON)
    output_data = Column(JSON)
    context = Column(JSON)
    success = Column(Boolean)
    execution_time_ms = Column(Integer)
    cost = Column(Float)
    metadata = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    agent = relationship("Agent", back_populates="executions")
    feedback = relationship("Feedback", back_populates="execution", uselist=False)

class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(String, primary_key=True, index=True)
    agent_id = Column(String, ForeignKey("agents.id"))
    execution_id = Column(String, ForeignKey("agent_executions.id"), unique=True)
    type = Column(Enum(FeedbackType))
    rating = Column(Integer)  # 1-5 scale
    correction = Column(Text)  # Correct answer if wrong
    comment = Column(Text)
    binary_feedback = Column(Boolean)  # Good/bad
    reviewer_id = Column(String)  # Could be user ID or "auto"
    metadata = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    agent = relationship("Agent", back_populates="feedback")
    execution = relationship("AgentExecution", back_populates="feedback")

class ABTest(Base):
    __tablename__ = "ab_tests"
    
    id = Column(String, primary_key=True, index=True)
    agent_id = Column(String, ForeignKey("agents.id"))
    name = Column(String, nullable=False)
    description = Column(Text)
    status = Column(Enum(ABTestStatus), default=ABTestStatus.DRAFT)
    traffic_split = Column(JSON)  # {"variant_a": 0.5, "variant_b": 0.5}
    metrics = Column(JSON)  # Metrics to track
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    winner_variant_id = Column(String)
    confidence_level = Column(Float)
    metadata = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    agent = relationship("Agent", back_populates="ab_tests")
    variants = relationship("ABTestVariant", back_populates="ab_test")
    results = relationship("ABTestResult", back_populates="ab_test")

class ABTestVariant(Base):
    __tablename__ = "ab_test_variants"
    
    id = Column(String, primary_key=True, index=True)
    ab_test_id = Column(String, ForeignKey("ab_tests.id"))
    name = Column(String, nullable=False)
    model_version_id = Column(String, ForeignKey("model_versions.id"))
    traffic_percentage = Column(Float)
    metadata = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    ab_test = relationship("ABTest", back_populates="variants")
    model_version = relationship("ModelVersion")
    results = relationship("ABTestResult", back_populates="variant")

class ABTestResult(Base):
    __tablename__ = "ab_test_results"
    
    id = Column(String, primary_key=True, index=True)
    ab_test_id = Column(String, ForeignKey("ab_tests.id"))
    variant_id = Column(String, ForeignKey("ab_test_variants.id"))
    executions_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    avg_execution_time = Column(Float)
    avg_cost = Column(Float)
    avg_rating = Column(Float)
    metrics = Column(JSON)  # Custom metrics
    period_start = Column(DateTime(timezone=True))
    period_end = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    ab_test = relationship("ABTest", back_populates="results")
    variant = relationship("ABTestVariant", back_populates="results")

class FineTuningJob(Base):
    __tablename__ = "fine_tuning_jobs"
    
    id = Column(String, primary_key=True, index=True)
    agent_id = Column(String, ForeignKey("agents.id"))
    name = Column(String, nullable=False)
    description = Column(Text)
    status = Column(Enum(FineTuningStatus), default=FineTuningStatus.PENDING)
    training_dataset_id = Column(String, ForeignKey("training_datasets.id"))
    base_model_version_id = Column(String, ForeignKey("model_versions.id"))
    new_model_version_id = Column(String, ForeignKey("model_versions.id"))
    hyperparameters = Column(JSON)
    metrics = Column(JSON)  # Training metrics
    error_message = Column(Text)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    metadata = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    agent = relationship("Agent", back_populates="fine_tuning_jobs")
    training_dataset = relationship("TrainingDataset")
    base_model_version = relationship("ModelVersion", foreign_keys=[base_model_version_id])
    new_model_version = relationship("ModelVersion", foreign_keys=[new_model_version_id])

class TrainingDataset(Base):
    __tablename__ = "training_datasets"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    source_type = Column(String)  # "feedback", "synthetic", "manual", "import"
    data = Column(JSON)  # Training examples
    statistics = Column(JSON)  # Dataset statistics
    metadata = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    fine_tuning_jobs = relationship("FineTuningJob", back_populates="training_dataset")

class ModelVersion(Base):
    __tablename__ = "model_versions"
    
    id = Column(String, primary_key=True, index=True)
    agent_id = Column(String, ForeignKey("agents.id"))
    version = Column(String, nullable=False)  # Semantic version: 1.0.0
    model_path = Column(String)  # Path to model files
    performance_metrics = Column(JSON)
    training_data_hash = Column(String)
    is_production = Column(Boolean, default=False)
    metadata = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    agent = relationship("Agent", back_populates="model_versions")
    ab_test_variants = relationship("ABTestVariant", back_populates="model_version")
    fine_tuning_jobs_as_base = relationship("FineTuningJob", foreign_keys=[FineTuningJob.base_model_version_id], back_populates="base_model_version")
    fine_tuning_jobs_as_new = relationship("FineTuningJob", foreign_keys=[FineTuningJob.new_model_version_id], back_populates="new_model_version")

class SyntheticScenario(Base):
    __tablename__ = "synthetic_scenarios"
    
    id = Column(String, primary_key=True, index=True)
    agent_id = Column(String, ForeignKey("agents.id"))
    name = Column(String, nullable=False)
    description = Column(Text)
    scenario_type = Column(String)  # "edge_case", "common", "failure", "success"
    input_data = Column(JSON)
    expected_output = Column(JSON)
    difficulty = Column(Integer)  # 1-5 scale
    tags = Column(JSON)  # List of tags
    metadata = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    agent = relationship("Agent")