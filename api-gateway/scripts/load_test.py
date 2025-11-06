"""
Load testing script using Locust
Run with: locust -f scripts/load_test.py --host=http://localhost:8080
"""

from locust import HttpUser, task, between
import random


class APIGatewayUser(HttpUser):
    """Simulated user for load testing API Gateway"""
    
    wait_time = between(1, 3)  # Wait 1-3 seconds between tasks
    
    @task(3)
    def check_health(self):
        """Test health endpoint (most common)"""
        self.client.get("/health")
    
    @task(2)
    def list_services(self):
        """Test services listing"""
        self.client.get("/services")
    
    @task(1)
    def check_circuit_breakers(self):
        """Test circuit breakers listing"""
        self.client.get("/circuit-breakers")
    
    @task(1)
    def root_endpoint(self):
        """Test root endpoint"""
        self.client.get("/")
    
    @task(2)
    def proxy_auth_request(self):
        """Test proxying to auth service"""
        # Simulate authentication request
        self.client.post(
            "/api/auth/login",
            json={
                "email": f"test{random.randint(1, 100)}@example.com",
                "password": "password123"
            }
        )
    
    def on_start(self):
        """Called when user starts"""
        pass
