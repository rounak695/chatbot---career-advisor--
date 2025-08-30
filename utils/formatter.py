import re
import markdown
from typing import Dict, List, Any
import html

def format_message(content: str) -> str:
    """
    Format message content for display in Streamlit
    Handles markdown, links, and special formatting
    """
    if not content:
        return ""
    
    # Escape HTML to prevent XSS
    content = html.escape(content)
    
    # Convert markdown-style formatting to HTML
    content = _process_markdown_formatting(content)
    
    # Process bullet points and lists
    content = _process_lists(content)
    
    # Process links
    content = _process_links(content)
    
    # Add line breaks
    content = _process_line_breaks(content)
    
    return content

def _process_markdown_formatting(text: str) -> str:
    """Process basic markdown formatting"""
    
    # Bold text (**text** or __text__)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'__(.*?)__', r'<strong>\1</strong>', text)
    
    # Italic text (*text* or _text_)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    text = re.sub(r'_(.*?)_', r'<em>\1</em>', text)
    
    # Inline code (`code`)
    text = re.sub(r'`(.*?)`', r'<code style="background-color: #f0f0f0; padding: 2px 4px; border-radius: 3px;">\1</code>', text)
    
    # Headers
    text = re.sub(r'^### (.*?)$', r'<h3 style="color: #2c3e50; margin-top: 1rem; margin-bottom: 0.5rem;">\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*?)$', r'<h2 style="color: #2c3e50; margin-top: 1rem; margin-bottom: 0.5rem;">\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.*?)$', r'<h1 style="color: #2c3e50; margin-top: 1rem; margin-bottom: 0.5rem;">\1</h1>', text, flags=re.MULTILINE)
    
    return text

def _process_lists(text: str) -> str:
    """Process bullet points and numbered lists"""
    
    lines = text.split('\n')
    processed_lines = []
    in_ul_list = False
    in_ol_list = False
    
    for line in lines:
        stripped_line = line.strip()
        
        # Check for bullet points
        if re.match(r'^[-*+]\s+', stripped_line):
            if not in_ul_list:
                processed_lines.append('<ul style="margin: 0.5rem 0; padding-left: 1.5rem;">')
                in_ul_list = True
            if in_ol_list:
                processed_lines.append('</ol>')
                in_ol_list = False
            
            content = re.sub(r'^[-*+]\s+', '', stripped_line)
            processed_lines.append(f'<li style="margin-bottom: 0.25rem;">{content}</li>')
            
        # Check for numbered lists
        elif re.match(r'^\d+\.\s+', stripped_line):
            if not in_ol_list:
                processed_lines.append('<ol style="margin: 0.5rem 0; padding-left: 1.5rem;">')
                in_ol_list = True
            if in_ul_list:
                processed_lines.append('</ul>')
                in_ul_list = False
            
            content = re.sub(r'^\d+\.\s+', '', stripped_line)
            processed_lines.append(f'<li style="margin-bottom: 0.25rem;">{content}</li>')
            
        else:
            # Close any open lists
            if in_ul_list:
                processed_lines.append('</ul>')
                in_ul_list = False
            if in_ol_list:
                processed_lines.append('</ol>')
                in_ol_list = False
            
            processed_lines.append(line)
    
    # Close any remaining open lists
    if in_ul_list:
        processed_lines.append('</ul>')
    if in_ol_list:
        processed_lines.append('</ol>')
    
    return '\n'.join(processed_lines)

def _process_links(text: str) -> str:
    """Process links and make them clickable"""
    
    # Markdown style links [text](url)
    text = re.sub(
        r'\[([^\]]+)\]\(([^)]+)\)',
        r'<a href="\2" target="_blank" style="color: #1f77b4; text-decoration: underline;">\1</a>',
        text
    )
    
    # Auto-link URLs
    url_pattern = r'(?<!href=")(?<!src=")(https?://[^\s<>"]+)'
    text = re.sub(
        url_pattern,
        r'<a href="\1" target="_blank" style="color: #1f77b4; text-decoration: underline;">\1</a>',
        text
    )
    
    return text

def _process_line_breaks(text: str) -> str:
    """Process line breaks and paragraphs"""
    
    # Convert double line breaks to paragraph breaks
    text = re.sub(r'\n\n+', '</p><p style="margin: 0.5rem 0;">', text)
    
    # Wrap the entire content in a paragraph if it doesn't start with a block element
    if not text.startswith(('<h1', '<h2', '<h3', '<ul', '<ol', '<p')):
        text = f'<p style="margin: 0.5rem 0;">{text}</p>'
    
    # Convert single line breaks to <br> tags within paragraphs
    text = re.sub(r'(?<!>)\n(?!<)', '<br>', text)
    
    return text

def format_career_advice(advice_data: Dict[str, Any]) -> str:
    """
    Format structured career advice data into readable HTML
    """
    if not advice_data:
        return ""
    
    formatted_content = []
    
    # Add title if present
    if 'title' in advice_data:
        formatted_content.append(f'<h3 style="color: #2c3e50; margin-bottom: 1rem;">🎯 {advice_data["title"]}</h3>')
    
    # Add main content
    if 'content' in advice_data:
        formatted_content.append(f'<p style="margin-bottom: 1rem;">{advice_data["content"]}</p>')
    
    # Add structured sections
    if 'sections' in advice_data:
        for section in advice_data['sections']:
            if 'title' in section:
                formatted_content.append(f'<h4 style="color: #34495e; margin: 1rem 0 0.5rem 0;">📌 {section["title"]}</h4>')
            
            if 'items' in section:
                formatted_content.append('<ul style="margin: 0.5rem 0; padding-left: 1.5rem;">')
                for item in section['items']:
                    formatted_content.append(f'<li style="margin-bottom: 0.25rem;">{item}</li>')
                formatted_content.append('</ul>')
            elif 'content' in section:
                formatted_content.append(f'<p style="margin-bottom: 0.5rem;">{section["content"]}</p>')
    
    # Add action items if present
    if 'action_items' in advice_data:
        formatted_content.append('<h4 style="color: #e67e22; margin: 1rem 0 0.5rem 0;">🚀 Next Steps</h4>')
        formatted_content.append('<ol style="margin: 0.5rem 0; padding-left: 1.5rem;">')
        for action in advice_data['action_items']:
            formatted_content.append(f'<li style="margin-bottom: 0.25rem; font-weight: 500;">{action}</li>')
        formatted_content.append('</ol>')
    
    # Add resources if present
    if 'resources' in advice_data:
        formatted_content.append('<h4 style="color: #9b59b6; margin: 1rem 0 0.5rem 0;">📚 Helpful Resources</h4>')
        formatted_content.append('<ul style="margin: 0.5rem 0; padding-left: 1.5rem;">')
        for resource in advice_data['resources']:
            if isinstance(resource, dict) and 'url' in resource:
                formatted_content.append(f'<li style="margin-bottom: 0.25rem;"><a href="{resource["url"]}" target="_blank" style="color: #1f77b4; text-decoration: underline;">{resource.get("title", resource["url"])}</a></li>')
            else:
                formatted_content.append(f'<li style="margin-bottom: 0.25rem;">{resource}</li>')
        formatted_content.append('</ul>')
    
    return ''.join(formatted_content)

def format_skills_list(skills: List[str], category: str = None) -> str:
    """Format a list of skills with proper styling"""
    if not skills:
        return ""
    
    formatted_content = []
    
    if category:
        formatted_content.append(f'<h4 style="color: #2c3e50; margin: 1rem 0 0.5rem 0;">💡 {category}</h4>')
    
    # Create skill badges
    skill_badges = []
    for skill in skills:
        badge = f'<span style="display: inline-block; background-color: #3498db; color: white; padding: 4px 8px; margin: 2px; border-radius: 12px; font-size: 0.9em;">{skill}</span>'
        skill_badges.append(badge)
    
    formatted_content.append('<div style="margin: 0.5rem 0;">')
    formatted_content.extend(skill_badges)
    formatted_content.append('</div>')
    
    return ''.join(formatted_content)

def format_error_message(error_msg: str) -> str:
    """Format error messages with appropriate styling"""
    return f'''
    <div style="background-color: #ffe6e6; border-left: 4px solid #e74c3c; padding: 1rem; margin: 0.5rem 0; border-radius: 4px;">
        <strong style="color: #c0392b;">⚠️ Error:</strong>
        <p style="margin: 0.5rem 0 0 0; color: #c0392b;">{error_msg}</p>
    </div>
    '''

def format_success_message(success_msg: str) -> str:
    """Format success messages with appropriate styling"""
    return f'''
    <div style="background-color: #e8f5e8; border-left: 4px solid #27ae60; padding: 1rem; margin: 0.5rem 0; border-radius: 4px;">
        <strong style="color: #229954;">✅ Success:</strong>
        <p style="margin: 0.5rem 0 0 0; color: #229954;">{success_msg}</p>
    </div>
    '''

def format_info_message(info_msg: str) -> str:
    """Format info messages with appropriate styling"""
    return f'''
    <div style="background-color: #e6f3ff; border-left: 4px solid #3498db; padding: 1rem; margin: 0.5rem 0; border-radius: 4px;">
        <strong style="color: #2980b9;">ℹ️ Info:</strong>
        <p style="margin: 0.5rem 0 0 0; color: #2980b9;">{info_msg}</p>
    </div>
    '''

def truncate_text(text: str, max_length: int = 200, suffix: str = "...") -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    
    # Try to break at word boundary
    truncated = text[:max_length - len(suffix)]
    last_space = truncated.rfind(' ')
    
    if last_space > max_length * 0.7:  # Only break at word if it's not too early
        truncated = truncated[:last_space]
    
    return truncated + suffix

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file operations"""
    # Remove or replace unsafe characters
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    
    # Limit length
    if len(filename) > 100:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        max_name_length = 95 - len(ext)
        filename = name[:max_name_length] + ('.' + ext if ext else '')
    
    return filename
