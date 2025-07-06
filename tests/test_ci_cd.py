import unittest
import yaml
import os

class TestCI_CD(unittest.TestCase):

    def setUp(self):
        self.ci_yml_path = os.path.join(os.path.dirname(__file__), '..', '.github', 'workflows', 'ci.yml')
        self.assertTrue(os.path.exists(self.ci_yml_path), f"ci.yml not found at {self.ci_yml_path}")
        with open(self.ci_yml_path, 'r') as f:
            self.ci_config = yaml.safe_load(f)

    def test_ci_yml_exists(self):
        self.assertIsNotNone(self.ci_config)

    def test_ci_yml_has_build_job(self):
        self.assertIn('build', self.ci_config.get('jobs', {}))

    def test_ci_yml_has_deploy_job(self):
        self.assertIn('deploy', self.ci_config.get('jobs', {}))

    def test_deploy_job_depends_on_build(self):
        deploy_job = self.ci_config.get('jobs', {}).get('deploy', {})
        self.assertIn('needs', deploy_job)
        self.assertIn('build', deploy_job['needs'])

    def test_deploy_job_runs_on_ubuntu_latest(self):
        deploy_job = self.ci_config.get('jobs', {}).get('deploy', {})
        self.assertEqual(deploy_job.get('runs-on'), 'ubuntu-latest')

    def test_deploy_job_has_environment(self):
        deploy_job = self.ci_config.get('jobs', {}).get('deploy', {})
        self.assertIn('environment', deploy_job)
        self.assertEqual(deploy_job['environment'], 'production')

    def test_deploy_job_has_steps(self):
        deploy_job = self.ci_config.get('jobs', {}).get('deploy', {})
        self.assertIn('steps', deploy_job)
        self.assertGreater(len(deploy_job['steps']), 0)

    def test_deploy_job_has_python_setup_step(self):
        deploy_job = self.ci_config.get('jobs', {}).get('deploy', {})
        steps = deploy_job.get('steps', [])
        python_setup_found = False
        for step in steps:
            if 'uses' in step and 'actions/setup-python' in step['uses']:
                python_setup_found = True
                break
        self.assertTrue(python_setup_found, "Python setup step not found in deploy job")

    def test_deploy_job_has_install_dependencies_step(self):
        deploy_job = self.ci_config.get('jobs', {}).get('deploy', {})
        steps = deploy_job.get('steps', [])
        install_deps_found = False
        for step in steps:
            if 'name' in step and 'Install Dependencies' in step['name']:
                install_deps_found = True
                break
        self.assertTrue(install_deps_found, "Install Dependencies step not found in deploy job")

if __name__ == '__main__':
    unittest.main()