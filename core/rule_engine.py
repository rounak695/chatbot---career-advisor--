#core/rule_engine.py                                                                                                                                                                           # core/rule_engine.py
# Person B (career DB for rule engine)

import json
import pandas as pd
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from enum import Enum

class SkillLevel(Enum):
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    EXPERT = 4

class InterestLevel(Enum):
    LOW = 1
    MODERATE = 2
    HIGH = 3
    VERY_HIGH = 4

@dataclass
class UserProfile:
    """User profile structure for rule matching"""
    skills: Dict[str, SkillLevel]
    interests: Dict[str, InterestLevel]
    experience_years: int
    education_level: str
    preferred_work_style: str  # remote, hybrid, onsite
    salary_expectation: int
    location_preference: str

@dataclass
class CareerPath:
    """Career path data structure"""
    id: str
    title: str
    description: str
    required_skills: Dict[str, SkillLevel]
    relevant_interests: Dict[str, InterestLevel]
    min_experience: int
    min_education: str
    typical_salary_range: Tuple[int, int]
    work_style_compatibility: List[str]
    growth_potential: int  # 1-10 scale
    job_market_demand: int  # 1-10 scale

class RuleEngine:
    """Core rule-based recommendation engine"""
    
    def __init__(self, career_db_path: str = "data/careers.csv"):
        self.career_paths = self._load_career_database(career_db_path)
        self.rules = self._initialize_rules()
    
    def _load_career_database(self, db_path: str) -> List[CareerPath]:
        """Load career database from CSV"""
        try:
            df = pd.read_csv(db_path)
            career_paths = []
            
            for _, row in df.iterrows():
                career = CareerPath(
                    id=str(row['id']),
                    title=row['title'],
                    description=row['description'],
                    required_skills=json.loads(row['required_skills']),
                    relevant_interests=json.loads(row['relevant_interests']),
                    min_experience=int(row['min_experience']),
                    min_education=row['min_education'],
                    typical_salary_range=(int(row['salary_min']), int(row['salary_max'])),
                    work_style_compatibility=json.loads(row['work_style_compatibility']),
                    growth_potential=int(row['growth_potential']),
                    job_market_demand=int(row['job_market_demand'])
                )
                career_paths.append(career)
            
            return career_paths
        except Exception as e:
            print(f"Error loading career database: {e}")
            return self._get_default_careers()
    
    def _get_default_careers(self) -> List[CareerPath]:
        """Fallback career data if CSV loading fails"""
        return [
            CareerPath(
                id="software_engineer",
                title="Software Engineer",
                description="Develop and maintain software applications",
                required_skills={"programming": SkillLevel.INTERMEDIATE.value, "problem_solving": SkillLevel.ADVANCED.value},
                relevant_interests={"technology": InterestLevel.HIGH.value, "innovation": InterestLevel.HIGH.value},
                min_experience=2,
                min_education="bachelor",
                typical_salary_range=(70000, 120000),
                work_style_compatibility=["remote", "hybrid", "onsite"],
                growth_potential=9,
                job_market_demand=9
            ),
            CareerPath(
                id="data_scientist",
                title="Data Scientist",
                description="Analyze complex data to derive business insights",
                required_skills={"statistics": SkillLevel.ADVANCED.value, "programming": SkillLevel.INTERMEDIATE.value},
                relevant_interests={"analytics": InterestLevel.HIGH.value, "research": InterestLevel.HIGH.value},
                min_experience=3,
                min_education="bachelor",
                typical_salary_range=(80000, 140000),
                work_style_compatibility=["remote", "hybrid"],
                growth_potential=10,
                job_market_demand=8
            )
        ]
    
    def _initialize_rules(self) -> List[callable]:
        """Initialize scoring rules"""
        return [
            self._skill_match_rule,
            self._interest_alignment_rule,
            self._experience_requirement_rule,
            self._education_compatibility_rule,
            self._salary_expectation_rule,
            self._work_style_preference_rule,
            self._market_demand_bonus_rule,
            self._growth_potential_bonus_rule
        ]
    
    def _skill_match_rule(self, user: UserProfile, career: CareerPath) -> float:
        """Score based on skill matching (40% weight)"""
        if not career.required_skills:
            return 0.0
        
        total_skills = len(career.required_skills)
        matched_skills = 0
        skill_quality_bonus = 0
        
        for skill, required_level in career.required_skills.items():
            if skill in user.skills:
                user_level = user.skills[skill].value if isinstance(user.skills[skill], SkillLevel) else user.skills[skill]
                if user_level >= required_level:
                    matched_skills += 1
                    # Bonus for exceeding requirements
                    skill_quality_bonus += max(0, (user_level - required_level) * 0.1)
        
        base_score = matched_skills / total_skills
        return min(1.0, base_score + skill_quality_bonus) * 0.4
    
    def _interest_alignment_rule(self, user: UserProfile, career: CareerPath) -> float:
        """Score based on interest alignment (25% weight)"""
        if not career.relevant_interests:
            return 0.0
        
        total_interests = len(career.relevant_interests)
        alignment_score = 0
        
        for interest, career_importance in career.relevant_interests.items():
            if interest in user.interests:
                user_interest = user.interests[interest].value if isinstance(user.interests[interest], InterestLevel) else user.interests[interest]
                # Higher score when user interest matches or exceeds career importance
                alignment_score += min(user_interest / career_importance, 1.5)
        
        return min(1.0, alignment_score / total_interests) * 0.25
    
    def _experience_requirement_rule(self, user: UserProfile, career: CareerPath) -> float:
        """Score based on experience requirements (15% weight)"""
        if user.experience_years >= career.min_experience:
            # Bonus for exceeding minimum requirements
            bonus = min(0.2, (user.experience_years - career.min_experience) * 0.02)
            return min(1.0, 0.8 + bonus) * 0.15
        else:
            # Penalty for not meeting requirements
            deficit = career.min_experience - user.experience_years
            penalty = min(0.6, deficit * 0.1)
            return max(0.0, 0.4 - penalty) * 0.15
    
    def _education_compatibility_rule(self, user: UserProfile, career: CareerPath) -> float:
        """Score based on education compatibility (10% weight)"""
        education_hierarchy = {
            "high_school": 1,
            "associate": 2,
            "bachelor": 3,
            "master": 4,
            "phd": 5
        }
        
        user_edu_level = education_hierarchy.get(user.education_level.lower(), 1)
        required_edu_level = education_hierarchy.get(career.min_education.lower(), 1)
        
        if user_edu_level >= required_edu_level:
            return 1.0 * 0.1
        else:
            # Partial credit for being close
            return max(0.0, (user_edu_level / required_edu_level) * 0.7) * 0.1
    
    def _salary_expectation_rule(self, user: UserProfile, career: CareerPath) -> float:
        """Score based on salary alignment (5% weight)"""
        salary_min, salary_max = career.typical_salary_range
        
        if salary_min <= user.salary_expectation <= salary_max:
            return 1.0 * 0.05
        elif user.salary_expectation < salary_min:
            # User expects less - still good match
            return 0.8 * 0.05
        else:
            # User expects more - check if it's reasonable
            overage = user.salary_expectation - salary_max
            if overage <= salary_max * 0.2:  # Within 20% of max
                return 0.6 * 0.05
            else:
                return 0.2 * 0.05
    
    def _work_style_preference_rule(self, user: UserProfile, career: CareerPath) -> float:
        """Score based on work style compatibility (3% weight)"""
        if user.preferred_work_style in career.work_style_compatibility:
            return 1.0 * 0.03
        else:
            return 0.0
    
    def _market_demand_bonus_rule(self, user: UserProfile, career: CareerPath) -> float:
        """Bonus for high market demand (1% weight)"""
        return (career.job_market_demand / 10) * 0.01
    
    def _growth_potential_bonus_rule(self, user: UserProfile, career: CareerPath) -> float:
        """Bonus for high growth potential (1% weight)"""
        return (career.growth_potential / 10) * 0.01
    
    def calculate_career_score(self, user: UserProfile, career: CareerPath) -> float:
        """Calculate total compatibility score for a career path"""
        total_score = 0.0
        
        for rule in self.rules:
            score = rule(user, career)
            total_score += score
        
        return min(1.0, total_score)  # Cap at 1.0
    
    def get_recommendations(self, user: UserProfile, top_n: int = 10) -> List[Tuple[CareerPath, float, Dict[str, str]]]:
        """Get top career recommendations with explanations"""
        scored_careers = []
        
        for career in self.career_paths:
            score = self.calculate_career_score(user, career)
            explanation = self._generate_explanation(user, career, score)
            scored_careers.append((career, score, explanation))
        
        # Sort by score descending
        scored_careers.sort(key=lambda x: x[1], reverse=True)
        
        return scored_careers[:top_n]
    
    def _generate_explanation(self, user: UserProfile, career: CareerPath, score: float) -> Dict[str, str]:
        """Generate explanation for the recommendation"""
        explanations = {
            "overall": f"Overall compatibility: {score:.1%}",
            "strengths": [],
            "considerations": []
        }
        
        # Skill analysis
        skill_score = self._skill_match_rule(user, career) / 0.4  # Normalize
        if skill_score > 0.8:
            explanations["strengths"].append("Strong skill alignment")
        elif skill_score < 0.5:
            explanations["considerations"].append("May need to develop additional skills")
        
        # Interest analysis
        interest_score = self._interest_alignment_rule(user, career) / 0.25
        if interest_score > 0.8:
            explanations["strengths"].append("Excellent interest match")
        elif interest_score < 0.5:
            explanations["considerations"].append("Interest alignment could be better")
        
        # Experience check
        if user.experience_years < career.min_experience:
            diff = career.min_experience - user.experience_years
            explanations["considerations"].append(f"Needs {diff} more years of experience")
        
        # Salary alignment
        salary_min, salary_max = career.typical_salary_range
        if user.salary_expectation > salary_max:
            explanations["considerations"].append("Salary expectations may be above typical range")
        
        return explanations

# Usage example and helper functions
def create_user_profile_from_dict(data: dict) -> UserProfile:
    """Helper to create UserProfile from dictionary data"""
    # Convert string skill levels to enums
    skills = {}
    for skill, level in data.get('skills', {}).items():
        if isinstance(level, str):
            skills[skill] = SkillLevel[level.upper()]
        else:
            skills[skill] = SkillLevel(level)
    
    # Convert string interest levels to enums
    interests = {}
    for interest, level in data.get('interests', {}).items():
        if isinstance(level, str):
            interests[interest] = InterestLevel[level.upper()]
        else:
            interests[interest] = InterestLevel(level)
    
    return UserProfile(
        skills=skills,
        interests=interests,
        experience_years=data.get('experience_years', 0),
        education_level=data.get('education_level', 'high_school'),
        preferred_work_style=data.get('preferred_work_style', 'hybrid'),
        salary_expectation=data.get('salary_expectation', 50000),
        location_preference=data.get('location_preference', '')
    )
# core/rule_engine.py
# Person B (rule-based recommendation system)

class RuleEngine:
    """
    Handles rule-based career recommendations based on user profiles and a career database.
    """
    def __init__(self):
        # In the future, this will load the careers.csv data using CareerDatabaseManager
        pass

    def get_recommendations(self, user_query: str) -> str:
        """
        Analyzes the user query and returns a list of career recommendations.
        
        This is a placeholder implementation.
        """
        # TODO: Implement the actual recommendation logic
        return (
            "Based on our rule engine, here are some careers you might be interested in:\n"
            "- Software Developer\n"
            "- Data Analyst\n"
            "- UX/UI Designer\n"
            "(Note: This is a placeholder response.)"
        )