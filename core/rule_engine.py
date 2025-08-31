#core/rule_engine.py                                                                                                                                                                           
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
                description="Analyze complex data to extract business insights",
                required_skills={"statistics": SkillLevel.ADVANCED.value, "programming": SkillLevel.INTERMEDIATE.value},
                relevant_interests={"analytics": InterestLevel.VERY_HIGH.value, "research": InterestLevel.HIGH.value},
                min_experience=3,
                min_education="bachelor",
                typical_salary_range=(80000, 140000),
                work_style_compatibility=["remote", "hybrid"],
                growth_potential=10,
                job_market_demand=8
            )
        ]
    
    def _initialize_rules(self) -> Dict[str, Any]:
        """Initialize rule weights and thresholds"""
        return {
            "skill_weight": 0.4,
            "interest_weight": 0.25,
            "experience_weight": 0.2,
            "salary_weight": 0.15,
            "min_score_threshold": 0.3
        }
    
    def get_recommendations(self, user_query: str) -> str:
        """
        Get career recommendations based on user query.
        This is a simplified version that provides general recommendations.
        """
        try:
            # For now, return top careers by market demand and growth potential
            top_careers = sorted(self.career_paths, 
                               key=lambda x: (x.job_market_demand, x.growth_potential), 
                               reverse=True)[:5]
            
            response = "Based on current market trends and growth potential, here are some promising career paths:\n\n"
            
            for i, career in enumerate(top_careers, 1):
                response += f"{i}. **{career.title}**\n"
                response += f"   - {career.description}\n"
                response += f"   - Salary: ${career.typical_salary_range[0]:,} - ${career.typical_salary_range[1]:,}\n"
                response += f"   - Growth Potential: {career.growth_potential}/10\n"
                response += f"   - Market Demand: {career.job_market_demand}/10\n\n"
            
            response += "Would you like me to analyze your specific skills and interests to provide more personalized recommendations?"
            return response
            
        except Exception as e:
            return f"I'm having trouble accessing the career database right now. Please try again later. Error: {str(e)}"
    
    def calculate_career_score(self, user: UserProfile, career: CareerPath) -> float:
        """Calculate compatibility score between user and career"""
        skill_score = self._skill_match_rule(user, career)
        interest_score = self._interest_alignment_rule(user, career)
        experience_score = self._experience_requirement_rule(user, career)
        salary_score = self._salary_expectation_rule(user, career)
        
        # Weighted combination
        total_score = (
            skill_score * self.rules["skill_weight"] +
            interest_score * self.rules["interest_weight"] +
            experience_score * self.rules["experience_weight"] +
            salary_score * self.rules["salary_weight"]
        )
        
        return total_score
    
    def _skill_match_rule(self, user: UserProfile, career: CareerPath) -> float:
        """Calculate skill match score"""
        if not user.skills:
            return 0.5  # Neutral score if no skills specified
        
        total_score = 0
        required_skills = len(career.required_skills)
        
        for skill, required_level in career.required_skills.items():
            user_level = user.skills.get(skill, SkillLevel.BEGINNER)
            if user_level.value >= required_level:
                total_score += 1.0
            elif user_level.value >= required_level - 1:
                total_score += 0.7
            else:
                total_score += 0.3
        
        return total_score / required_skills if required_skills > 0 else 0
    
    def _interest_alignment_rule(self, user: UserProfile, career: CareerPath) -> float:
        """Calculate interest alignment score"""
        if not user.interests:
            return 0.5  # Neutral score if no interests specified
        
        total_score = 0
        relevant_interests = len(career.relevant_interests)
        
        for interest, required_level in career.relevant_interests.items():
            user_level = user.interests.get(interest, InterestLevel.MODERATE)
            if user_level.value >= required_level:
                total_score += 1.0
            elif user_level.value >= required_level - 1:
                total_score += 0.8
            else:
                total_score += 0.4
        
        return total_score / relevant_interests if relevant_interests > 0 else 0
    
    def _experience_requirement_rule(self, user: UserProfile, career: CareerPath) -> float:
        """Calculate experience requirement score"""
        if user.experience_years >= career.min_experience:
            return 1.0
        elif user.experience_years >= career.min_experience * 0.7:
            return 0.8
        elif user.experience_years >= career.min_experience * 0.5:
            return 0.6
        else:
            return 0.3
    
    def _salary_expectation_rule(self, user: UserProfile, career: CareerPath) -> float:
        """Calculate salary expectation alignment"""
        min_salary, max_salary = career.typical_salary_range
        mid_salary = (min_salary + max_salary) / 2
        
        if user.salary_expectation <= max_salary and user.salary_expectation >= min_salary:
            return 1.0
        elif user.salary_expectation <= max_salary * 1.2:
            return 0.8
        elif user.salary_expectation <= max_salary * 1.5:
            return 0.6
        else:
            return 0.4
    
    def get_top_recommendations(self, user: UserProfile, top_n: int = 5) -> List[Tuple[CareerPath, float, Dict[str, str]]]:
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