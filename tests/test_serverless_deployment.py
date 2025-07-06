import unittest
import os
from src.serverless_deployment import ServerlessDeploymentStrategy

class TestServerlessDeploymentStrategy(unittest.TestCase):

    def setUp(self):
        self.strategy = ServerlessDeploymentStrategy()

    def test_component_analysis(self):
        # Test with a component suitable for serverless
        suitable_component = {
            "name": "auth_service",
            "characteristics": ["event-driven", "stateless", "short-lived"]
        }
        analysis_result = self.strategy.analyze_component_for_serverless(suitable_component)
        self.assertTrue(analysis_result["suitable"])
        self.assertIn("Auth service is highly suitable for serverless deployment", analysis_result["reason"])

        # Test with a component not suitable for serverless
        unsuitable_component = {
            "name": "database_server",
            "characteristics": ["stateful", "long-running", "high-resource"]
        }
        analysis_result = self.strategy.analyze_component_for_serverless(unsuitable_component)
        self.assertFalse(analysis_result["suitable"])
        self.assertIn("Database server is generally not suitable for serverless deployment", analysis_result["reason"])

    def test_get_deployment_strategy(self):
        # Test AWS Lambda strategy
        aws_strategy = self.strategy.get_deployment_strategy("AWS Lambda")
        self.assertIn("AWS Lambda", aws_strategy["platform"])
        self.assertIn("Event-driven functions", aws_strategy["description"])

        # Test Azure Functions strategy
        azure_strategy = self.strategy.get_deployment_strategy("Azure Functions")
        self.assertIn("Azure Functions", azure_strategy["platform"])
        self.assertIn("Microsoft's serverless compute service", azure_strategy["description"])

        # Test Google Cloud Functions strategy
        gcp_strategy = self.strategy.get_deployment_strategy("Google Cloud Functions")
        self.assertIn("Google Cloud Functions", gcp_strategy["platform"])
        self.assertIn("Google's lightweight, event-driven compute solution", gcp_strategy["description"])

        # Test unknown platform
        unknown_strategy = self.strategy.get_deployment_strategy("Unknown Platform")
        self.assertIsNone(unknown_strategy)

    def test_get_cost_efficiency_considerations(self):
        considerations = self.strategy.get_cost_efficiency_considerations()
        self.assertIsInstance(considerations, list)
        self.assertGreater(len(considerations), 0)
        self.assertIn("Pay-per-execution model", considerations[0])

    def test_get_scalability_considerations(self):
        considerations = self.strategy.get_scalability_considerations()
        self.assertIsInstance(considerations, list)
        self.assertGreater(len(considerations), 0)
        self.assertIn("Automatic scaling based on demand", considerations[0])

if __name__ == '__main__':
    unittest.main()