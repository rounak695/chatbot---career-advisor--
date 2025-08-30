# tests/test_rule_engine.py
# Person B (tests for rule-based logic)

import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.rule_engine import (
    RuleEngine, UserProfile, CareerPath, SkillLevel, InterestLevel,
    create_user_profile_from_dict
)

class TestRuleEngine(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.rule_engine = RuleEngine()
        
        # Create test user profile
        self.test_user = UserProfile(
            skills={
                "programming": SkillLevel.INTERMEDIATE,
                "problem_solving": SkillLevel.ADVANCED,
                "communication": SkillLevel.INTERMEDIATE
            },
            interests={
                "technology": InterestLevel.HIGH,
                "innovation": InterestLevel.HIGH,
                "creativity": InterestLevel.MODERATE
            },
            experience_years=3,
            education_level="bachelor",
            preferred_work_style="remote",
            salary_expectation=85000,
            location_preference="anywhere"
        )
        
        # Create test career path
        self.test_career = CareerPath(
            id="test_software_engineer",
            title="Software Engineer",
            description="Test software engineer role",
            required_skills={"programming": 2, "problem_solving": 3},
            relevant_interests={"technology": 3, "innovation": 3},
            min_experience=2,
            min_education="bachelor",
            typical_salary_range=(70000, 120000),
            work_style_compatibility=["remote", "hybrid"],
            growth_potential=9,
            job_market_demand=8
        )
    
    def test_skill_match_rule(self):
        """Test skill matching rule"""
        score = self.rule_engine._skill_match_rule(self.test_user, self.test_career)
        
        # Should get high score for matching skills
        self.assertGreater(score, 0.3)  # 40% weight, so > 75% match
        self.assertLessEqual(score, 0.4)  # Max 40% of total
    
    def test_interest_alignment_rule(self):
        """Test interest alignment rule"""
        score = self.rule_engine._interest_alignment_rule(self.test_user, self.test_career)
        
        # Should get good score for aligned interests
        self.assertGreater(score, 0.15)  # 25% weight, good alignment
        self.assertLessEqual(score, 0.25)  # Max 25% of total
    
    def test_experience_requirement_rule(self):
        """Test experience requirement rule"""
        score = self.rule_engine._experience_requirement_rule(self.test_user, self.test_career)
        
        # User has 3 years, career needs 2, should get full score + bonus
        self.assertGreater(score, 0.12)  # 15% weight with bonus
        self.assertLessEqual(score, 0.15)
    
    def test_education_compatibility_rule(self):
        """Test education compatibility rule"""
        score = self.rule_engine._education_compatibility_rule(self.test_user, self.test_career)
        
        # Both have bachelor's requirement, should get full score
        self.assertEqual(score, 0.1)  # Full 10% weight
    
    def test_salary_expectation_rule(self):
        """Test salary expectation rule"""
        score = self.rule_engine._salary_expectation_rule(self.test_user, self.test_career)
        
        # User expects 85k, career offers 70-120k, should be perfect match
        self.assertEqual(score, 0.05)  # Full 5% weight
    
    def test_work_style_preference_rule(self):
        """Test work style preference rule"""
        score = self.rule_engine._work_style_preference_rule(self.test_user, self.test_career)
        
        # User prefers remote, career supports remote
        self.assertEqual(score, 0.03)  # Full 3% weight
    
    def test_calculate_career_score(self):
        """Test overall career score calculation"""
        score = self.rule_engine.calculate_career_score(self.test_user, self.test_career)
        
        # Should be a high score given good alignment
        self.assertGreater(score, 0.7)
        self.assertLessEqual(score, 1.0)
    
    def test_get_recommendations(self):
        """Test getting career recommendations"""
        recommendations = self.rule_engine.get_recommendations(self.test_user, top_n=5)
        
        # Should return recommendations
        self.assertGreater(len(recommendations), 0)
        self.assertLessEqual(len(recommendations), 5)
        
        # Check structure of recommendations
        for career, score, explanation in recommendations:
            self.assertIsInstance(career, CareerPath)
            self.assertIsInstance(score, float)
            self.assertIsInstance(explanation, dict)
            self.assertIn('overall', explanation)
            self.assertIn('strengths', explanation)
            self.assertIn('considerations', explanation)
    
    def test_create_user_profile_from_dict(self):
        """Test creating user profile from dictionary"""
        user_data = {
            'skills': {
                'programming': 'intermediate',
                'communication': 2
            },
            'interests': {
                'technology': 'high',
                'business': 3
            },
            'experience_years': 5,
            'education_level': 'master',
            'preferred_work_style': 'hybrid',
            'salary_expectation': 95000
        }
        
        user_profile = create_user_profile_from_dict(user_data)
        
        self.assertEqual(user_profile.skills['programming'], SkillLevel.INTERMEDIATE)
        self.assertEqual(user_profile.skills['communication'], SkillLevel.INTERMEDIATE)
        self.assertEqual(user_profile.interests['technology'], InterestLevel.HIGH)
        self.assertEqual(user_profile.interests['business'], InterestLevel.HIGH)
        self.assertEqual(user_profile.experience_years, 5)
        self.assertEqual(user_profile.education_level, 'master')

class TestRuleEngineEdgeCases(unittest.TestCase):
    
    def setUp(self):
        self.rule_engine = RuleEngine()
    
    def test_user_lacks_required_skills(self):
        """Test scoring when user lacks required skills"""
        user = UserProfile(
            skills={"writing": SkillLevel.ADVANCED},  # No programming skills
            interests={"technology": InterestLevel.HIGH},
            experience_years=1,
            education_level="bachelor",
            preferred_work_style="remote",
            salary_expectation=70000,
            location_preference=""
        )
        
        # Test against software engineer role
        career = CareerPath(
            id="software_engineer",
            title="Software Engineer",
            description="Programming role",
            required_skills={"programming": 3, "problem_solving": 2},
            relevant_interests={"technology": 3},
            min_experience=2,
            min_education="bachelor",
            typical_salary_range=(70000, 120000),
            work_style_compatibility=["remote"],
            growth_potential=8,
            job_market_demand=9
        )
        
        score = self.rule_engine.calculate_career_score(user, career)
        self.assertLess(score, 0.5)  # Should be low due to missing skills
    
    def test_overqualified_user(self):
        """Test scoring for overqualified user"""
        user = UserProfile(
            skills={
                "programming": SkillLevel.EXPERT,
                "leadership": SkillLevel.EXPERT,
                "architecture": SkillLevel.ADVANCED
            },
            interests={"technology": InterestLevel.VERY_HIGH},
            experience_years=15,
            education_level="phd",
            preferred_work_style="hybrid",
            salary_expectation=200000,
            location_preference=""
        )
        
        # Test against junior role
        career = CareerPath(
            id="junior_dev",
            title="Junior Developer",
            description="Entry level role",
            required_skills={"programming": 1},
            relevant_interests={"technology": 2},
            min_experience=0,
            min_education="bachelor",
            typical_salary_range=(45