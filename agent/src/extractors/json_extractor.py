"""JSON content extraction utilities"""

import re
import json
from typing import List, Optional


class JSONExtractor:
    """Utility class for extracting JSON content from LLM responses"""
    
    @staticmethod
    def extract_project_list(text: str) -> Optional[List[str]]:
        """Extract JSON array from LLM response for project selection"""
        # Pattern to match JSON array
        pattern = r'\[(.*?)\]'
        match = re.search(pattern, text, re.DOTALL)
        
        if match:
            try:
                json_str = '[' + match.group(1) + ']'
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
        
        # Fallback: try to extract quoted strings
        quoted_pattern = r'"([^"]+)"'
        quoted_matches = re.findall(quoted_pattern, text)
        
        if quoted_matches:
            return quoted_matches[:4]  # Return max 4 projects
        
        return None
    
    @staticmethod
    def extract_any_json(text: str) -> Optional[dict]:
        """Extract any JSON object from text"""
        # Try to find JSON object
        json_pattern = r'\{.*?\}'
        match = re.search(json_pattern, text, re.DOTALL)
        
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
        
        return None
    
    @staticmethod
    def validate_project_names(project_names: List[str], available_projects: List[dict]) -> List[str]:
        """Validate that selected project names exist in available projects"""
        available_titles = [project.get("title", "") for project in available_projects]
        valid_names = []
        
        for name in project_names:
            if name in available_titles:
                valid_names.append(name)
            else:
                # Try fuzzy matching
                for title in available_titles:
                    if name.lower() in title.lower() or title.lower() in name.lower():
                        valid_names.append(title)
                        break
        
        return valid_names