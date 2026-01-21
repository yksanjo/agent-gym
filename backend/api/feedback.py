from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from datetime import datetime

from database import get_db
from models import Feedback, AgentExecution, Agent
from schemas import FeedbackCreate, FeedbackResponse

router = APIRouter()

@router.get("/", response_model=List[FeedbackResponse])
async def list_feedback(
    agent_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all feedback"""
    query = db.query(Feedback)
    if agent_id:
        query = query.filter(Feedback.agent_id == agent_id)
    
    feedback = query.order_by(Feedback.created_at.desc())\
        .offset(skip)\
        .limit(limit)\
        .all()
    
    return feedback

@router.post("/", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
async def create_feedback(
    feedback: FeedbackCreate,
    db: Session = Depends(get_db)
):
    """Create feedback for an agent execution"""
    # Check if execution exists
    execution = db.query(AgentExecution)\
        .filter(AgentExecution.id == feedback.execution_id)\
        .first()
    
    if not execution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Execution not found"
        )
    
    # Check if feedback already exists for this execution
    existing_feedback = db.query(Feedback)\
        .filter(Feedback.execution_id == feedback.execution_id)\
        .first()
    
    if existing_feedback:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Feedback already exists for this execution"
        )
    
    # Create feedback
    db_feedback = Feedback(
        id=str(uuid.uuid4()),
        agent_id=execution.agent_id,
        execution_id=feedback.execution_id,
        **feedback.dict(exclude={"execution_id"})
    )
    
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

@router.get("/{feedback_id}", response_model=FeedbackResponse)
async def get_feedback(
    feedback_id: str,
    db: Session = Depends(get_db)
):
    """Get feedback by ID"""
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    return feedback

@router.get("/agent/{agent_id}/summary")
async def get_feedback_summary(
    agent_id: str,
    db: Session = Depends(get_db)
):
    """Get feedback summary for an agent"""
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    feedback_list = db.query(Feedback)\
        .filter(Feedback.agent_id == agent_id)\
        .all()
    
    if not feedback_list:
        return {
            "total_feedback": 0,
            "avg_rating": None,
            "rating_distribution": {},
            "feedback_types": {}
        }
    
    # Calculate statistics
    total = len(feedback_list)
    
    # Rating distribution
    rating_dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    ratings = []
    
    # Feedback type distribution
    type_dist = {}
    
    for fb in feedback_list:
        if fb.rating:
            rating_dist[fb.rating] = rating_dist.get(fb.rating, 0) + 1
            ratings.append(fb.rating)
        
        fb_type = fb.type.value if fb.type else "unknown"
        type_dist[fb_type] = type_dist.get(fb_type, 0) + 1
    
    avg_rating = sum(ratings) / len(ratings) if ratings else None
    
    return {
        "total_feedback": total,
        "avg_rating": avg_rating,
        "rating_distribution": rating_dist,
        "feedback_types": type_dist
    }

@router.get("/execution/{execution_id}")
async def get_feedback_for_execution(
    execution_id: str,
    db: Session = Depends(get_db)
):
    """Get feedback for a specific execution"""
    execution = db.query(AgentExecution)\
        .filter(AgentExecution.id == execution_id)\
        .first()
    
    if not execution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Execution not found"
        )
    
    feedback = db.query(Feedback)\
        .filter(Feedback.execution_id == execution_id)\
        .first()
    
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No feedback found for this execution"
        )
    
    return feedback

@router.post("/auto/{execution_id}")
async def create_auto_feedback(
    execution_id: str,
    db: Session = Depends(get_db)
):
    """Create automated feedback for an execution"""
    execution = db.query(AgentExecution)\
        .filter(AgentExecution.id == execution_id)\
        .first()
    
    if not execution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Execution not found"
        )
    
    # Check if feedback already exists
    existing_feedback = db.query(Feedback)\
        .filter(Feedback.execution_id == execution_id)\
        .first()
    
    if existing_feedback:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Feedback already exists for this execution"
        )
    
    # TODO: Implement actual automated feedback logic
    # For now, create mock feedback based on execution success
    if execution.success:
        rating = 5
        binary_feedback = True
        comment = "Execution successful"
    else:
        rating = 1
        binary_feedback = False
        comment = "Execution failed"
    
    db_feedback = Feedback(
        id=str(uuid.uuid4()),
        agent_id=execution.agent_id,
        execution_id=execution_id,
        type="rating",
        rating=rating,
        binary_feedback=binary_feedback,
        comment=comment,
        reviewer_id="auto_feedback_system"
    )
    
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback