import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import json
from app import create_app
from database import db_session, Base, engine
from app.models.user import User
from app.models.courses import Course
from flask_jwt_extended import create_access_token

class StudentsAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Setup a fresh database
        Base.metadata.create_all(bind=engine)
        
        # Create dummy user and course for testing
        self.user = User(username='testadmin', password='pwd', role='admin', email='test@test.com')
        self.course = Course(name='Math 101', credits=3)
        db_session.add(self.user)
        db_session.add(self.course)
        db_session.commit()
        
        # Cache the IDs safely so they don't expire from the session
        self.user_id = self.user.id
        self.course_id = self.course.id
        
        with self.app.app_context():
            self.token = create_access_token(identity=str(self.user_id), additional_claims={"role": self.user.role})
            self.headers = {"Authorization": f"Bearer {self.token}"}

    def tearDown(self):
        db_session.remove()
        Base.metadata.drop_all(bind=engine)

    def test_get_all_students_empty(self):
        response = self.client.get('/api/students', headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_create_student(self):
        response = self.client.post('/api/students', headers=self.headers, json={'name': 'Jane Doe', 'gpa': 3.8, 'user_id': self.user_id, 'courses': [self.course_id]})
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)
        self.assertEqual(response.json['name'], 'Jane Doe')
        self.assertEqual(response.json['user_id'], self.user_id)
        self.assertEqual(response.json['courses'][0]['id'], self.course_id)

    def test_create_student_invalid_data(self):
        response = self.client.post('/api/students', headers=self.headers, json={'name': 'No GPA'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)

    def test_get_student(self):
        # Create first
        post_resp = self.client.post('/api/students', headers=self.headers, json={'name': 'John Smith', 'gpa': 3.5, 'user_id': self.user_id, 'courses': [self.course_id]})
        student_id = post_resp.json['id']
        
        # Get it
        get_resp = self.client.get(f'/api/students/{student_id}', headers=self.headers)
        self.assertEqual(get_resp.status_code, 200)
        self.assertEqual(get_resp.json['name'], 'John Smith')
        self.assertEqual(get_resp.json['gpa'], 3.5)

    def test_get_student_not_found(self):
        response = self.client.get('/api/students/999', headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_update_student(self):
        # Create first
        post_resp = self.client.post('/api/students', headers=self.headers, json={'name': 'Bob', 'gpa': 2.5, 'user_id': self.user_id, 'courses': []})
        student_id = post_resp.json['id']
        
        # Update
        put_resp = self.client.put(f'/api/students/{student_id}', headers=self.headers, json={'name': 'Bob', 'gpa': 3.0, 'user_id': self.user_id, 'courses': [self.course_id]})
        self.assertEqual(put_resp.status_code, 200)
        self.assertEqual(put_resp.json['gpa'], 3.0)
        self.assertEqual(len(put_resp.json['courses']), 1)

    def test_delete_student(self):
        # Create first
        post_resp = self.client.post('/api/students', headers=self.headers, json={'name': 'To Be Deleted', 'gpa': 1.0, 'user_id': self.user_id, 'courses': []})
        student_id = post_resp.json['id']
        
        # Delete
        del_resp = self.client.delete(f'/api/students/{student_id}', headers=self.headers)
        self.assertEqual(del_resp.status_code, 200)
        
        # Verify it's gone
        get_resp = self.client.get(f'/api/students/{student_id}', headers=self.headers)
        self.assertEqual(get_resp.status_code, 404)

if __name__ == '__main__':
    unittest.main()
