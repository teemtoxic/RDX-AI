import os
from datetime import datetime

class NotesManager:
    def __init__(self):
        # Get the Documents folder path
        self.notes_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'RDX_Notes')
        if not os.path.exists(self.notes_dir):
            os.makedirs(self.notes_dir)
    
    def create_note(self, content, title=None):
        """Create a note in Documents/RDX_Notes folder"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Clean up the title if provided
        if title:
            title = ''.join(c for c in title if c.isalnum() or c in (' ', '-', '_'))
        
        filename = f"{title}_{timestamp}.txt" if title else f"note_{timestamp}.txt"
        filepath = os.path.join(self.notes_dir, filename)
        
        # Add timestamp and formatting to content
        formatted_content = f"""Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'=' * 40}

{content}

{'=' * 40}"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(formatted_content)
        
        return filepath
