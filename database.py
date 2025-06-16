from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Database:
    def __init__(self):
        # Get MongoDB connection string from environment variable
        mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        self.client = MongoClient(mongo_uri)
        self.db = self.client['ai_council']
        
        # Initialize collections
        self.ai_models = self.db['ai_models']
        self.discussions = self.db['discussions']
        self.user_contributions = self.db['user_contributions']
        self.system_settings = self.db['system_settings']
        
        # Create indexes
        self._create_indexes()
    
    def _create_indexes(self):
        # AI Models indexes
        self.ai_models.create_index('model_id', unique=True)
        self.ai_models.create_index('is_active')
        
        # Discussions indexes
        self.discussions.create_index('discussion_id', unique=True)
        self.discussions.create_index('status')
        self.discussions.create_index('created_at')
        self.discussions.create_index('active_models')
        
        # User Contributions indexes
        self.user_contributions.create_index('discussion_id')
        self.user_contributions.create_index('timestamp')
        self.user_contributions.create_index('round_number')
        
        # System Settings indexes
        self.system_settings.create_index('key', unique=True)
    
    # AI Models operations
    def get_all_models(self):
        return list(self.ai_models.find())
    
    def get_active_models(self):
        return list(self.ai_models.find({'is_active': True}))
    
    def get_model(self, model_id):
        return self.ai_models.find_one({'model_id': model_id})
    
    def update_model(self, model_id, update_data):
        update_data['updated_at'] = datetime.utcnow()
        if 'created_at' not in update_data:
            update_data['created_at'] = datetime.utcnow()
        return self.ai_models.update_one(
            {'model_id': model_id},
            {'$set': update_data},
            upsert=True
        )
    
    def toggle_model_active(self, model_id, is_active):
        return self.ai_models.update_one(
            {'model_id': model_id},
            {'$set': {'is_active': is_active, 'updated_at': datetime.utcnow()}}
        )
    
    # Discussions operations
    def create_discussion(self, discussion_data):
        discussion_data['created_at'] = datetime.utcnow()
        discussion_data['updated_at'] = datetime.utcnow()
        discussion_data['status'] = 'in_progress'
        discussion_data['results'] = []
        result = self.discussions.insert_one(discussion_data)
        return str(result.inserted_id)
    
    def get_discussion(self, discussion_id):
        return self.discussions.find_one({'discussion_id': discussion_id})
    
    def update_discussion_status(self, discussion_id, status):
        return self.discussions.update_one(
            {'discussion_id': discussion_id},
            {'$set': {'status': status}}
        )
    
    def add_discussion_round(self, discussion_id, round_data):
        round_data['timestamp'] = datetime.utcnow()
        return self.discussions.update_one(
            {'discussion_id': discussion_id},
            {
                '$push': {'results': round_data},
                '$set': {'metadata.last_activity': datetime.utcnow()}
            }
        )
    
    def get_all_discussions(self):
        return list(self.discussions.find().sort('created_at', DESCENDING))
    
    # User Contributions operations
    def add_user_contribution(self, contribution_data):
        contribution_data['timestamp'] = datetime.utcnow()
        return self.user_contributions.insert_one(contribution_data)
    
    def get_discussion_contributions(self, discussion_id):
        return list(self.user_contributions.find(
            {'discussion_id': discussion_id}
        ).sort('timestamp', ASCENDING))
    
    # System Settings operations
    def get_setting(self, key):
        setting = self.system_settings.find_one({'key': key})
        return setting['value'] if setting else None
    
    def update_setting(self, key, value, description=None):
        update_data = {
            'value': value,
            'updated_at': datetime.utcnow()
        }
        if description:
            update_data['description'] = description
        return self.system_settings.update_one(
            {'key': key},
            {'$set': update_data},
            upsert=True
        )

# Create a global database instance
db = Database() 