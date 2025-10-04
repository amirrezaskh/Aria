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
        """Extract LaTeX skills section from LLM response"""
        text = LaTeXExtractor.clean_markdown_blocks(text)
        
        # Pattern to match \\begin{itemize} ... \\end{itemize} block
        pattern = r'(\\begin\{itemize\}\[leftmargin=[^\]]*\].*?\\end\{itemize\})'
        match = re.search(pattern, text, re.DOTALL)
        
        if match:
            return match.group(1)
        
        # Fallback: look for \\small{\\item{ ... }} pattern
        fallback_pattern = r'(\\small\{\\item\{.*?\}\})'
        fallback_match = re.search(fallback_pattern, text, re.DOTALL)
        
        if fallback_match:
            return f"\\begin{{itemize}}[leftmargin=0.15in, label={{}}]\n{fallback_match.group(1)}\n\\end{{itemize}}"
        
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
    def extract_highlights(text: str) -> str:
        """Extract LaTeX highlights/qualifications from LLM response"""
        text = LaTeXExtractor.clean_markdown_blocks(text)
        
        def extract_resume_items(text: str) -> List[str]:
            items = []
            lines = text.split('\n')
            current_item = ''
            brace_count = 0
            in_resume_item = False
            
            for line in lines:
                line = line.strip()
                if line.startswith('\\resumeItem{'):
                    if current_item and in_resume_item:
                        items.append(current_item.strip())
                    current_item = line
                    brace_count = line.count('{') - line.count('}')
                    in_resume_item = True
                elif in_resume_item:
                    current_item += ' ' + line
                    brace_count += line.count('{') - line.count('}')
                    
                if in_resume_item and brace_count <= 0:
                    items.append(current_item.strip())
                    current_item = ''
                    in_resume_item = False
                    brace_count = 0
            
            # Add any remaining item
            if current_item and in_resume_item:
                items.append(current_item.strip())
            
            return items
        
        resume_items = extract_resume_items(text)
        
        if resume_items:
            return '\n'.join(resume_items)
        
        # Fallback: try simple regex for single-line items
        simple_pattern = r'\\resumeItem\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
        simple_matches = re.findall(simple_pattern, text)
        
        if simple_matches:
            return '\n'.join(simple_matches)
        
        # Ultimate fallback: return cleaned text
        return text.strip()
    
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