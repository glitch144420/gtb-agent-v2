import re
import os
from typing import List

class FileExtractor:
    """Extracts files from LLM responses."""
    
    def __init__(self):
        self.pattern = r'`?([\w\/\.-]+\.\w+)`?\s*\n```(?:\w+)?\n([\s\S]+?)\n```'
    
    def extract_files(self, response: str, project_path: str) -> List[str]:
        """Extract files from LLM response and save them to project path."""
        created_files = []
        
        # Find all file blocks in the response
        matches = re.findall(self.pattern, response)
        
        for filename, content in matches:
            # Clean filename
            filename = filename.strip()
            
            # Create full path
            full_path = os.path.join(project_path, filename)
            
            # Create directories if needed
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            # Save file
            try:
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                created_files.append(filename)
                print(f"✅ Created: {filename}")
            except Exception as e:
                print(f"❌ Error creating {filename}: {str(e)}")
        
        return created_files
    
    def extract_file_blocks(self, response: str) -> List[dict]:
        """Extract file blocks without saving them."""
        files = []
        matches = re.findall(self.pattern, response)
        
        for filename, content in matches:
            files.append({
                "filename": filename.strip(),
                "content": content
            })
        
        return files