"""
Basic Agent Gym Integration Example

This example shows how to integrate Agent Gym with a custom AI agent.
"""

import requests
import json
import uuid
from typing import Dict, Any, Optional

class AgentGymClient:
    """Client for interacting with Agent Gym API"""
    
    def __init__(self, base_url: str = "http://localhost:8000", api_key: Optional[str] = None):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}" if api_key else None
        }
    
    def register_agent(self, name: str, description: str = "") -> Dict[str, Any]:
        """Register a new agent with Agent Gym"""
        agent_data = {
            "name": name,
            "description": description,
            "model_type": "custom",
            "model_config": {}
        }
        
        response = requests.post(
            f"{self.base_url}/api/v1/agents/",
            json=agent_data,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def execute_with_feedback(self, agent_id: str, input_data: Dict[str, Any], 
                            context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute agent and record execution for feedback collection"""
        execution_data = {
            "input_data": input_data,
            "context": context or {},
            "metadata": {
                "source": "example_integration"
            }
        }
        
        response = requests.post(
            f"{self.base_url}/api/v1/agents/{agent_id}/execute",
            json=execution_data,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def submit_feedback(self, execution_id: str, rating: int, 
                       comment: Optional[str] = None) -> Dict[str, Any]:
        """Submit feedback for an agent execution"""
        feedback_data = {
            "execution_id": execution_id,
            "type": "rating",
            "rating": rating,
            "comment": comment,
            "reviewer_id": "example_user"
        }
        
        response = requests.post(
            f"{self.base_url}/api/v1/feedback/",
            json=feedback_data,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def get_agent_metrics(self, agent_id: str) -> Dict[str, Any]:
        """Get performance metrics for an agent"""
        response = requests.get(
            f"{self.base_url}/api/v1/agents/{agent_id}/metrics",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def create_ab_test(self, agent_id: str, name: str, 
                      variants: Dict[str, str]) -> Dict[str, Any]:
        """Create an A/B test for agent versions"""
        # First, get or create model versions for variants
        model_versions = {}
        for variant_name, model_path in variants.items():
            # In a real scenario, you'd register model versions first
            model_versions[variant_name] = str(uuid.uuid4())
        
        ab_test_data = {
            "name": name,
            "description": f"A/B test for {name}",
            "traffic_split": {k: 1.0/len(variants) for k in variants.keys()},
            "metrics": ["success_rate", "avg_execution_time", "avg_rating"]
        }
        
        response = requests.post(
            f"{self.base_url}/api/v1/ab-testing/",
            json=ab_test_data,
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

class CustomAgent:
    """Example custom AI agent"""
    
    def __init__(self, name: str, gym_client: AgentGymClient):
        self.name = name
        self.gym = gym_client
        self.agent_id = None
    
    def initialize(self):
        """Initialize agent with Agent Gym"""
        print(f"Initializing agent: {self.name}")
        agent_info = self.gym.register_agent(self.name, "Example custom agent")
        self.agent_id = agent_info["id"]
        print(f"Agent registered with ID: {self.agent_id}")
        return self
    
    def process(self, user_input: str, context: Dict[str, Any] = None) -> str:
        """Process user input and record execution"""
        if not self.agent_id:
            raise ValueError("Agent not initialized. Call initialize() first.")
        
        # Prepare input data
        input_data = {
            "user_input": user_input,
            "timestamp": "2024-01-20T23:15:00Z"
        }
        
        # Execute through Agent Gym
        execution = self.gym.execute_with_feedback(
            self.agent_id, 
            input_data, 
            context
        )
        
        # In a real scenario, you'd actually run your agent here
        # For this example, we'll return a mock response
        response = f"Processed: {user_input}"
        
        # The execution is recorded in Agent Gym for later feedback
        print(f"Execution recorded: {execution['id']}")
        
        return response
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get performance report from Agent Gym"""
        if not self.agent_id:
            raise ValueError("Agent not initialized.")
        
        return self.gym.get_agent_metrics(self.agent_id)

def main():
    """Example usage of Agent Gym integration"""
    
    # Initialize Agent Gym client
    gym = AgentGymClient()
    
    # Create and initialize custom agent
    agent = CustomAgent("Customer Support Bot", gym)
    agent.initialize()
    
    # Process some example inputs
    examples = [
        "Hello, I need help with my order",
        "What's your return policy?",
        "My product arrived damaged",
        "Can I change my shipping address?"
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\nExample {i}: {example}")
        response = agent.process(example)
        print(f"Response: {response}")
        
        # Simulate user feedback (in reality, this would come from users)
        # For this example, we'll use mock feedback
        execution_id = f"execution_{i}"  # In reality, get from execution response
        rating = 5 if i % 2 == 0 else 3  # Mock ratings
        feedback = gym.submit_feedback(execution_id, rating, "Example feedback")
        print(f"Feedback submitted: Rating {rating}")
    
    # Get performance report
    print("\n" + "="*50)
    print("Performance Report:")
    report = agent.get_performance_report()
    print(json.dumps(report, indent=2))
    
    # Example: Create an A/B test
    print("\n" + "="*50)
    print("Creating A/B test...")
    variants = {
        "version_1": "/models/agent_v1",
        "version_2": "/models/agent_v2"
    }
    
    try:
        ab_test = gym.create_ab_test(agent.agent_id, "Response Time Optimization", variants)
        print(f"A/B test created: {ab_test['id']}")
    except Exception as e:
        print(f"Note: A/B test creation requires additional setup. Error: {e}")

if __name__ == "__main__":
    # Note: This example assumes Agent Gym is running locally
    # Start it with: docker-compose up or python backend/main.py
    print("Agent Gym Integration Example")
    print("="*50)
    print("\nThis example demonstrates how to integrate Agent Gym with a custom AI agent.")
    print("\nPrerequisites:")
    print("1. Start Agent Gym: docker-compose up")
    print("2. Run this example: python examples/basic_integration.py")
    print("\nThe example will:")
    print("1. Register an agent with Agent Gym")
    print("2. Process example inputs and record executions")
    print("3. Submit mock feedback")
    print("4. Generate a performance report")
    print("5. Demonstrate A/B test creation")
    
    # Uncomment to run the example
    # main()