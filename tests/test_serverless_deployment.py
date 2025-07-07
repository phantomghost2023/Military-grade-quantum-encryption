import unittest
import os
from src.serverless_deployment import ServerlessDeployment

class TestServerlessDeployment(unittest.TestCase):

    def setUp(self):
        self.deployment = ServerlessDeployment()

    def test_component_analysis(self):
        # Test with a component suitable for serverless
        recommendations = self.deployment.analyze_component_for_serverless("Auth service", "API_ENDPOINT")
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)

        # Test with a component not suitable for serverless
        recommendations = self.deployment.analyze_component_for_serverless("Database server", "STATEFUL_SERVICE")
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)

    def test_outline_deployment_strategy(self):
        aws_strategy = self.deployment.outline_deployment_strategy("aws")
        self.assertIsInstance(aws_strategy, list)
        self.assertGreater(len(aws_strategy), 0)

        azure_strategy = self.deployment.outline_deployment_strategy("azure")
        self.assertIsInstance(azure_strategy, list)
        self.assertGreater(len(azure_strategy), 0)

        gcp_strategy = self.deployment.outline_deployment_strategy("google cloud")
        self.assertIsInstance(gcp_strategy, list)
        self.assertGreater(len(gcp_strategy), 0)

    def test_consider_cost_efficiency(self):
        considerations = self.deployment.consider_cost_efficiency()
        self.assertIsInstance(considerations, list)
        self.assertGreater(len(considerations), 0)
        self.assertIn("Pay-per-execution model", considerations[0])

    def test_consider_scalability(self):
        considerations = self.deployment.consider_scalability()
        self.assertIsInstance(considerations, list)
        self.assertGreater(len(considerations), 0)
        self.assertIn("Automatic scaling based on demand", considerations[0])

if __name__ == '__main__':
    unittest.main()