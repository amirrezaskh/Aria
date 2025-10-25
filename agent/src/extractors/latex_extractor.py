"""LaTeX content extraction utilities"""

import re
from typing import List


class LaTeXExtractor:
    """Utility class for extracting clean LaTeX content from LLM responses"""
    
    @staticmethod
    def clean_markdown_blocks(text: str) -> str:
        """Remove markdown code block markers"""
        text = re.sub(r'```latex\n?', '', text)
        text = re.sub(r'```\n?', '', text)
        return text
    
    @staticmethod
    def extract_experiences(text: str) -> str:
        """Extract LaTeX experience entries from LLM response"""
        text = LaTeXExtractor.clean_markdown_blocks(text)
        
        # Pattern to match \\resumeSubheading blocks
        pattern = r'(\\resumeSubheading\s*\{[^}]*\}\{[^}]*\}\s*\{[^}]*\}\{[^}]*\}\s*\\resumeItemListStart.*?\\resumeItemListEnd)'
        matches = re.findall(pattern, text, re.DOTALL)
        
        if matches:
            return '\n\n'.join(matches)
        
        # Fallback: look for any \\resumeSubheading pattern
        fallback_pattern = r'(\\resumeSubheading.*?)(?=\\resumeSubheading|$)'
        fallback_matches = re.findall(fallback_pattern, text, re.DOTALL)
        
        if fallback_matches:
            return '\n\n'.join(fallback_matches)
        
        return text.strip()
    
    @staticmethod
    def extract_skills(text: str) -> str:
        """Extract comma-separated skills list from LLM response"""
        text = LaTeXExtractor.clean_markdown_blocks(text)
        
        # Remove common LLM response prefixes and explanatory text
        lines = text.split('\n')
        cleaned_lines = []
        
        skip_prefixes = [
            "Here's a",
            "Here is a", 
            "Based on",
            "I'll create",
            "The skills",
            "This skills",
            "Following the",
            "Generated skills:",
            "Skills:",
            "Technical Skills:",
            "**",  # Bold markdown
            "```",  # Code blocks
            "Note:",
            "Important:",
            "Skills list:"
        ]
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines at the beginning
            if not line and not cleaned_lines:
                continue
                
            # Skip instructional or explanatory lines
            should_skip = False
            for prefix in skip_prefixes:
                if line.startswith(prefix):
                    should_skip = True
                    break
            
            if not should_skip and line:
                cleaned_lines.append(line)
        
        # Join lines and look for comma-separated skills
        skills_text = ' '.join(cleaned_lines).strip()
        
        # Clean up excessive whitespace
        skills_text = re.sub(r'\s+', ' ', skills_text)
        
        # Remove any remaining markdown formatting
        skills_text = re.sub(r'\*\*(.*?)\*\*', r'\1', skills_text)  # Remove **bold**
        skills_text = re.sub(r'\*(.*?)\*', r'\1', skills_text)  # Remove *italic*
        
        # Validate that it looks like a comma-separated list
        if ',' in skills_text and len(skills_text) > 20:
            # Clean up spacing around commas
            skills_text = re.sub(r'\s*,\s*', ', ', skills_text)
            return skills_text
        
        # Fallback: return original cleaned text if format doesn't match expected
        return text.strip()
    
    @staticmethod
    def extract_projects(text: str) -> str:
        """Extract LaTeX project entries from LLM response"""
        text = LaTeXExtractor.clean_markdown_blocks(text)
        
        # Pattern to match \\resumeProjectHeading blocks
        pattern = r'(\\resumeProjectHeading\s*\{[^}]*\}\s*\{[^}]*\}\s*\\resumeItemListStart.*?\\resumeItemListEnd)'
        matches = re.findall(pattern, text, re.DOTALL)
        
        if matches:
            return '\n\n'.join(matches)
        
        # Fallback: look for any \\resumeProjectHeading pattern
        fallback_pattern = r'(\\resumeProjectHeading.*?)(?=\\resumeProjectHeading|$)'
        fallback_matches = re.findall(fallback_pattern, text, re.DOTALL)
        
        if fallback_matches:
            return '\n\n'.join(fallback_matches)
        
        return text.strip()
    
    @staticmethod
    def extract_summary(text: str) -> str:
        """Extract plain-text professional summary from LLM response"""
        text = LaTeXExtractor.clean_markdown_blocks(text)
        
        # Remove common LLM response prefixes and explanatory text
        lines = text.split('\n')
        cleaned_lines = []
        
        skip_prefixes = [
            "Here's a",
            "Here is a", 
            "Based on",
            "I'll create",
            "The summary",
            "This summary",
            "Following the",
            "Generated summary:",
            "Summary:",
            "Professional Summary:",
            "**",  # Bold markdown
            "```",  # Code blocks
            "Note:",
            "Important:",
            "Character count:",
            "Length:"
        ]
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines at the beginning
            if not line and not cleaned_lines:
                continue
                
            # Skip instructional or explanatory lines
            should_skip = False
            for prefix in skip_prefixes:
                if line.startswith(prefix):
                    should_skip = True
                    break
            
            if not should_skip and line:
                cleaned_lines.append(line)
        
        # Join lines into a single summary paragraph
        summary = ' '.join(cleaned_lines).strip()
        
        # Clean up excessive whitespace
        summary = re.sub(r'\s+', ' ', summary)
        
        # Remove any remaining markdown formatting
        summary = re.sub(r'\*\*(.*?)\*\*', r'\1', summary)  # Remove **bold**
        summary = re.sub(r'\*(.*?)\*', r'\1', summary)  # Remove *italic*
        
        # Validate summary length (should be 220-330 characters)
        if len(summary) < 50:  # Too short, likely an error
            return text.strip()  # Return original if cleaning went wrong
        
        return summary
    
    @staticmethod
    def extract_cover_letter(text: str) -> str:
        """Extract clean LaTeX cover letter content from LLM response"""
        text = LaTeXExtractor.clean_markdown_blocks(text)
        
        # Remove any explanatory text or instruction responses
        lines = text.split('\n')
        cleaned_lines = []
        
        # Skip common LLM response prefixes
        skip_prefixes = [
            "Here's a",
            "Here is a", 
            "Based on",
            "I'll create",
            "The cover letter",
            "This cover letter",
            "Following the",
            "**",  # Bold markdown
            "```",  # Code blocks
            "Note:",
            "Important:",
            "Generated cover letter:"
        ]
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines at the beginning
            if not line and not cleaned_lines:
                continue
                
            # Skip instructional or explanatory lines
            should_skip = False
            for prefix in skip_prefixes:
                if line.startswith(prefix):
                    should_skip = True
                    break
            
            if not should_skip:
                cleaned_lines.append(line)
        
        # Join lines and clean up extra whitespace
        cover_letter = '\n'.join(cleaned_lines).strip()
        
        # Remove any remaining markdown formatting
        cover_letter = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', cover_letter)  # Convert **bold** to \textbf{}
        cover_letter = re.sub(r'\*(.*?)\*', r'\\emph{\1}', cover_letter)  # Convert *italic* to \emph{}
        
        # Clean up excessive whitespace
        cover_letter = re.sub(r'\n\s*\n\s*\n+', '\n\n', cover_letter)  # Max 2 consecutive newlines
        cover_letter = re.sub(r'[ \t]+', ' ', cover_letter)  # Multiple spaces to single space
        
        # Ensure proper paragraph separation in LaTeX
        paragraphs = cover_letter.split('\n\n')
        clean_paragraphs = []
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if paragraph:
                # Ensure paragraph doesn't start with common LaTeX issues
                paragraph = re.sub(r'^\\\\+', '', paragraph)  # Remove leading line breaks
                clean_paragraphs.append(paragraph)
        
        # Join paragraphs with proper LaTeX paragraph separation
        final_cover_letter = '\n\n'.join(clean_paragraphs)
        
        # Final validation - ensure we have actual content
        if len(final_cover_letter.strip()) < 50:  # Too short, likely an error
            return text.strip()  # Return original if cleaning went wrong
        
        return final_cover_letter