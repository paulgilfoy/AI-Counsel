import unittest
from datetime import datetime
import os
from database import db
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test database connection"""
        # Use a test database
        os.environ['MONGODB_URI'] = os.environ.get('MONGODB_TEST_URI', 'mongodb://localhost:27017/ai_council_test')
        cls.db = db

    def setUp(self):
        """Clear collections before each test"""
        self.db.ai_models.delete_many({})
        self.db.discussions.delete_many({})
        self.db.user_contributions.delete_many({})
        self.db.system_settings.delete_many({})

    def test_create_and_get_model(self):
        """Test creating and retrieving an AI model"""
        model_data = {
            'model_id': 'test-model',
            'name': 'Test Model',
            'provider': 'Test Provider',
            'description': 'A test model',
            'sprite': 'test-sprite.png',
            'system_prompt': 'You are a test model',
            'is_active': True
        }
        
        # Create model
        self.db.update_model('test-model', model_data)
        
        # Get model
        model = self.db.get_model('test-model')
        self.assertIsNotNone(model)
        self.assertEqual(model['model_id'], 'test-model')
        self.assertEqual(model['name'], 'Test Model')
        self.assertEqual(model['provider'], 'Test Provider')
        self.assertEqual(model['description'], 'A test model')
        self.assertEqual(model['sprite'], 'test-sprite.png')
        self.assertEqual(model['system_prompt'], 'You are a test model')
        self.assertTrue(model['is_active'])
        self.assertIn('created_at', model)
        self.assertIn('updated_at', model)

    def test_get_all_models(self):
        """Test retrieving all models"""
        # Create test models
        model1 = {
            'model_id': 'model1',
            'name': 'Model 1',
            'provider': 'Provider 1',
            'description': 'First test model',
            'sprite': 'sprite1.png',
            'system_prompt': 'You are model 1',
            'is_active': True
        }
        model2 = {
            'model_id': 'model2',
            'name': 'Model 2',
            'provider': 'Provider 2',
            'description': 'Second test model',
            'sprite': 'sprite2.png',
            'system_prompt': 'You are model 2',
            'is_active': False
        }
        
        self.db.update_model('model1', model1)
        self.db.update_model('model2', model2)
        
        # Get all models
        models = self.db.get_all_models()
        self.assertEqual(len(models), 2)
        
        # Get active models
        active_models = self.db.get_active_models()
        self.assertEqual(len(active_models), 1)
        self.assertEqual(active_models[0]['model_id'], 'model1')

    def test_toggle_model_active(self):
        """Test toggling model active status"""
        model_data = {
            'model_id': 'test-model',
            'name': 'Test Model',
            'provider': 'Test Provider',
            'description': 'A test model',
            'sprite': 'test-sprite.png',
            'system_prompt': 'You are a test model',
            'is_active': True
        }
        
        # Create model
        self.db.update_model('test-model', model_data)
        
        # Toggle active status
        self.db.toggle_model_active('test-model', False)
        model = self.db.get_model('test-model')
        self.assertFalse(model['is_active'])
        
        self.db.toggle_model_active('test-model', True)
        model = self.db.get_model('test-model')
        self.assertTrue(model['is_active'])

    def test_create_and_get_discussion(self):
        """Test creating and retrieving a discussion"""
        discussion_data = {
            'discussion_id': 'test-discussion',
            'topic': 'Test Topic',
            'rounds_requested': 2,
            'active_models': ['model1', 'model2'],
            'metadata': {
                'total_rounds': 0,
                'last_activity': datetime.utcnow()
            }
        }
        
        # Create discussion
        self.db.create_discussion(discussion_data)
        
        # Get discussion
        discussion = self.db.get_discussion('test-discussion')
        self.assertIsNotNone(discussion)
        self.assertEqual(discussion['discussion_id'], 'test-discussion')
        self.assertEqual(discussion['topic'], 'Test Topic')
        self.assertEqual(discussion['rounds_requested'], 2)
        self.assertEqual(discussion['active_models'], ['model1', 'model2'])
        self.assertEqual(discussion['status'], 'in_progress')
        self.assertEqual(len(discussion['results']), 0)
        self.assertIn('created_at', discussion)
        self.assertIn('updated_at', discussion)

    def test_add_discussion_round(self):
        """Test adding a round to a discussion"""
        # Create discussion
        discussion_data = {
            'discussion_id': 'test-discussion',
            'topic': 'Test Topic',
            'rounds_requested': 2,
            'active_models': ['model1', 'model2'],
            'metadata': {
                'total_rounds': 0,
                'last_activity': datetime.utcnow()
            }
        }
        self.db.create_discussion(discussion_data)
        
        # Add round
        round_data = {
            'round_number': 1,
            'responses': {
                'model1': 'Response from model 1',
                'model2': 'Response from model 2'
            },
            'timestamp': datetime.utcnow()
        }
        self.db.add_discussion_round('test-discussion', round_data)
        
        # Get discussion and verify round
        discussion = self.db.get_discussion('test-discussion')
        self.assertEqual(len(discussion['results']), 1)
        self.assertEqual(discussion['results'][0]['round_number'], 1)
        self.assertEqual(discussion['results'][0]['responses']['model1'], 'Response from model 1')
        self.assertEqual(discussion['results'][0]['responses']['model2'], 'Response from model 2')

    def test_update_discussion_status(self):
        """Test updating discussion status"""
        # Create discussion
        discussion_data = {
            'discussion_id': 'test-discussion',
            'topic': 'Test Topic',
            'rounds_requested': 2,
            'active_models': ['model1', 'model2'],
            'metadata': {
                'total_rounds': 0,
                'last_activity': datetime.utcnow()
            }
        }
        self.db.create_discussion(discussion_data)
        
        # Update status
        self.db.update_discussion_status('test-discussion', 'complete')
        
        # Verify status
        discussion = self.db.get_discussion('test-discussion')
        self.assertEqual(discussion['status'], 'complete')

    def test_add_user_contribution(self):
        """Test adding a user contribution"""
        # Create discussion
        discussion_data = {
            'discussion_id': 'test-discussion',
            'topic': 'Test Topic',
            'rounds_requested': 2,
            'active_models': ['model1', 'model2'],
            'metadata': {
                'total_rounds': 0,
                'last_activity': datetime.utcnow()
            }
        }
        self.db.create_discussion(discussion_data)
        
        # Add contribution
        contribution_data = {
            'discussion_id': 'test-discussion',
            'user_message': 'Test user message',
            'round_number': 1,
            'active_models': ['model1', 'model2']
        }
        self.db.add_user_contribution(contribution_data)
        
        # Verify contribution
        contribution = self.db.user_contributions.find_one({'discussion_id': 'test-discussion'})
        self.assertIsNotNone(contribution)
        self.assertEqual(contribution['user_message'], 'Test user message')
        self.assertEqual(contribution['round_number'], 1)
        self.assertEqual(contribution['active_models'], ['model1', 'model2'])

    def test_get_all_discussions(self):
        """Test retrieving all discussions"""
        # Create test discussions
        discussion1 = {
            'discussion_id': 'discussion1',
            'topic': 'Topic 1',
            'rounds_requested': 1,
            'active_models': ['model1'],
            'metadata': {
                'total_rounds': 0,
                'last_activity': datetime.utcnow()
            }
        }
        discussion2 = {
            'discussion_id': 'discussion2',
            'topic': 'Topic 2',
            'rounds_requested': 2,
            'active_models': ['model2'],
            'metadata': {
                'total_rounds': 0,
                'last_activity': datetime.utcnow()
            }
        }
        
        self.db.create_discussion(discussion1)
        self.db.create_discussion(discussion2)
        
        # Get all discussions
        discussions = self.db.get_all_discussions()
        self.assertEqual(len(discussions), 2)
        self.assertEqual(discussions[0]['discussion_id'], 'discussion2')  # Most recent first
        self.assertEqual(discussions[1]['discussion_id'], 'discussion1')

if __name__ == '__main__':
    unittest.main() 