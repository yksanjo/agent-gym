from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from datetime import datetime

from database import get_db
from models import Agent, AgentExecution, AgentStatus
from schemas import (
    AgentCreate, AgentUpdate, AgentResponse,
    AgentExecutionCreate, AgentExecutionResponse
)

router = APIRouter()

@router.get("/", response_model=List[AgentResponse])
async def list_agents(
    skip: int = 0,
    limit: int = 100,
    status: Optional[AgentStatus] = None,
    db: Session = Depends(get_db)
):
    """List all agents"""
    query = db.query(Agent)
    if status:
        query = query.filter(Agent.status == status)
    agents = query.offset(skip).limit(limit).all()
    return agents

@router.post("/", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent: AgentCreate,
    db: Session = Depends(get_db)
):
    """Create a new agent"""
    db_agent = Agent(
        id=str(uuid.uuid4()),
        **agent.dict()
    )
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: str,
    db: Session = Depends(get_db)
):
    """Get agent by ID"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    return agent

@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: str,
    agent_update: AgentUpdate,
    db: Session = Depends(get_db)
):
    """Update agent"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    update_data = agent_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(agent, field, value)
    
    agent.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(agent)
    return agent

@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: str,
    db: Session = Depends(get_db)
):
    """Delete agent"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    db.delete(agent)
    db.commit()

@router.post("/{agent_id}/execute", response_model=AgentExecutionResponse)
async def execute_agent(
    agent_id: str,
    execution: AgentExecutionCreate,
    db: Session = Depends(get_db)
):
    """Execute an agent and record the execution"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    # TODO: Actually execute the agent using the appropriate model
    # For now, create a mock execution
    execution_id = str(uuid.uuid4())
    
    db_execution = AgentExecution(
        id=execution_id,
        agent_id=agent_id,
        input_data=execution.input_data,
        output_data={"result": "Mock execution result"},  # Mock output
        context=execution.context,
        success=True,
        execution_time_ms=100,  # Mock execution time
        cost=0.001,  # Mock cost
        metadata=execution.metadata
    )
    
    db.add(db_execution)
    db.commit()
    db.refresh(db_execution)
    return db_execution

@router.get("/{agent_id}/executions", response_model=List[AgentExecutionResponse])
async def list_agent_executions(
    agent_id: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all executions for an agent"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    executions = db.query(AgentExecution)\
        .filter(AgentExecution.agent_id == agent_id)\
        .order_by(AgentExecution.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return executions

@router.get("/{agent_id}/metrics")
async def get_agent_metrics(
    agent_id: str,
    db: Session = Depends(get_db)
):
    """Get agent performance metrics"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    # Calculate basic metrics
    executions = db.query(AgentExecution)\
        .filter(AgentExecution.agent_id == agent_id)\
        .all()
    
    if not executions:
        return {
            "total_executions": 0,
            "success_rate": 0,
            "avg_execution_time": 0,
            "avg_cost": 0
        }
    
    total = len(executions)
    successful = sum(1 for e in executions if e.success)
    avg_time = sum(e.execution_time_ms or 0 for e in executions) / total
    avg_cost = sum(e.cost or 0 for e in executions) / total
    
    return {
        "total_executions": total,
        "success_rate": successful / total if total > 0 else 0,
        "avg_execution_time_ms": avg_time,
        "avg_cost": avg_cost,
        "last_execution": max(e.created_at for e in executions).isoformat() if executions else None
    }