# core/career_db_manager.py
# Person B (career DB for rule engine) - Database management utilities

import pandas as pd
import json
from typing import Dict, Any

class CareerDatabaseManager:
    """Utility class to manage and validate the career database."""

    def __init__(self, csv_path: str = "data/careers.csv"):
        self.csv_path = csv_path
        self.required_columns = [
            'id', 'title', 'description', 'required_skills', 'relevant_interests',
            'min_experience', 'min_education', 'salary_min', 'salary_max',
            'work_style_compatibility', 'growth_potential', 'job_market_demand'
        ]
        self.numeric_fields = [
            'min_experience', 'salary_min', 'salary_max', 
            'growth_potential', 'job_market_demand'
        ]
        self.json_fields = [
            'required_skills', 'relevant_interests', 'work_style_compatibility'
        ]

    def validate_csv_structure(self) -> Dict[str, Any]:
        """Validate the CSV structure and return validation results."""
        results = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'stats': {}
        }

        try:
            df = pd.read_csv(self.csv_path)
            if df.empty:
                results['warnings'].append("CSV file is empty.")
                return results
        except FileNotFoundError:
            results['valid'] = False
            results['errors'].append(f"CSV file not found: {self.csv_path}")
            return results
        except Exception as e:
            results['valid'] = False
            results['errors'].append(f"Failed to read CSV file: {e}")
            return results

        # 1. Check for missing columns
        missing_columns = set(self.required_columns) - set(df.columns)
        if missing_columns:
            results['valid'] = False
            results['errors'].append(f"Missing required columns: {list(missing_columns)}")
            # Return early as other checks will fail without required columns
            return results

        # 2. Check for duplicate IDs
        duplicate_ids = df[df.duplicated(subset=['id'])]['id'].tolist()
        if duplicate_ids:
            results['valid'] = False
            results['errors'].append(f"Duplicate career IDs found: {duplicate_ids}")

        # 3. Validate and convert numeric fields *before* using them
        for field in self.numeric_fields:
            # Coerce non-numeric values to NaN (Not a Number)
            original_type = df[field].dtype
            df[field] = pd.to_numeric(df[field], errors='coerce')
            if df[field].isnull().any():
                results['valid'] = False
                invalid_rows = df[df[field].isnull()]['title'].tolist()
                results['errors'].append(f"Non-numeric or empty values in '{field}': {invalid_rows}")
        
        # If there were numeric conversion errors, stop before doing calculations
        if not results['valid']:
             return results

        # 4. Validate JSON fields
        for field in self.json_fields:
            invalid_json_rows = []
            for index, value in df[field].items():
                try:
                    # Check if it's already a list/dict (pandas can auto-parse sometimes)
                    if isinstance(value, (str)):
                        json.loads(value)
                except (json.JSONDecodeError, TypeError):
                    invalid_json_rows.append(df.loc[index, 'title'])
            if invalid_json_rows:
                results['valid'] = False
                results['errors'].append(f"Invalid JSON format in '{field}': {invalid_json_rows}")

        # 5. Perform logical checks on now-validated numeric data
        # Validate ranges (salary_min < salary_max)
        salary_issues = df[df['salary_min'] >= df['salary_max']]['title'].tolist()
        if salary_issues:
            results['warnings'].append(f"Salary min is greater than or equal to max for: {salary_issues}")

        # Validate scales (1-10)
        for field in ['growth_potential', 'job_market_demand']:
            out_of_range = df[~df[field].between(1, 10)]['title'].tolist()
            if out_of_range:
                results['warnings'].append(f"Values in '{field}' are outside the valid range of 1-10 for: {out_of_range}")
        
        # 6. Generate statistics (only if data is valid)
        results['stats'] = {
            'total_careers': len(df),
            'unique_education_levels': df['min_education'].unique().tolist(),
            'salary_range': {
                'min': int(df['salary_min'].min()),
                'max': int(df['salary_max'].max()),
                'avg_min': int(df['salary_min'].mean()),
                'avg_max': int(df['salary_max'].mean())
            },
            'experience_range': {
                'min': int(df['min_experience'].min()),
                'max': int(df['min_experience'].max()),
                'avg': round(df['min_experience'].mean(), 1)
            }
        }
        
        return results