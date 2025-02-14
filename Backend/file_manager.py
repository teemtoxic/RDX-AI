import os
import shutil
from datetime import datetime
import subprocess

class FileManager:
    def __init__(self):
        self.extensions = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'],
            'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.xlsx', '.pptx', '.csv'],
            'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
            'Music': ['.mp3', '.wav', '.flac', '.m4a', '.aac', '.ogg'],
            'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.json'],
            'Executables': ['.exe', '.msi', '.bat', '.cmd'],
            'Others': []  # For unknown extensions
        }
        
        # Common directory paths
        self.common_paths = {
            'downloads': os.path.join(os.path.expanduser('~'), 'Downloads'),
            'documents': os.path.join(os.path.expanduser('~'), 'Documents'),
            'desktop': os.path.join(os.path.expanduser('~'), 'Desktop'),
            'pictures': os.path.join(os.path.expanduser('~'), 'Pictures')
        }
        
        self.reports_dir = "Reports"
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)
    
    def get_directory_path(self, directory):
        """Convert common directory names to full paths"""
        if directory.lower() in self.common_paths:
            return self.common_paths[directory.lower()]
        return directory
    
    def save_and_show_report(self, content, report_type="file_organization"):
        """Save report to file and open in notepad"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.reports_dir, f"{report_type}_report_{timestamp}.txt")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Open report in notepad
        subprocess.Popen(['notepad.exe', filename])
        return filename
    
    def organize_files(self, directory):
        """Organize files by extension into folders"""
        # Convert common directory names to full paths
        directory = self.get_directory_path(directory)
        
        if not os.path.exists(directory):
            return f"Directory '{directory}' does not exist. Available directories: {', '.join(self.common_paths.keys())}"
            
        stats = {
            'total_files': 0,
            'organized_files': 0,
            'errors': 0,
            'by_type': {}
        }
        
        try:
            # Walk through directory
            for root, dirs, files in os.walk(directory):
                for file in files:
                    stats['total_files'] += 1
                    try:
                        file_path = os.path.join(root, file)
                        ext = os.path.splitext(file)[1].lower()
                        
                        # Find appropriate folder
                        target_folder = 'Others'
                        for folder, extensions in self.extensions.items():
                            if ext in extensions:
                                target_folder = folder
                                break
                        
                        # Create folder if doesn't exist
                        folder_path = os.path.join(directory, target_folder)
                        if not os.path.exists(folder_path):
                            os.makedirs(folder_path)
                        
                        # Move file
                        shutil.move(file_path, os.path.join(folder_path, file))
                        
                        # Update stats
                        stats['organized_files'] += 1
                        stats['by_type'][target_folder] = stats['by_type'].get(target_folder, 0) + 1
                        
                    except Exception as e:
                        stats['errors'] += 1
                        print(f"Error processing {file}: {str(e)}")
            
            # Generate report
            report = f"""File Organization Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
==================================
Directory: {directory}
==================================
Total files found: {stats['total_files']}
Files organized: {stats['organized_files']}
Errors encountered: {stats['errors']}

Files organized by type:
----------------------"""
            
            for folder, count in stats['by_type'].items():
                report += f"\n{folder}: {count} files"
                
            # Save and show report
            self.save_and_show_report(report, "file_organization")
            return report
            
        except Exception as e:
            return f"Error organizing files: {str(e)}"

    def get_directory_stats(self, directory):
        """Get statistics about a directory"""
        stats = {
            'total_size': 0,
            'file_count': 0,
            'folder_count': 0,
            'last_modified': None
        }
        
        try:
            for root, dirs, files in os.walk(directory):
                stats['folder_count'] += len(dirs)
                stats['file_count'] += len(files)
                
                for file in files:
                    file_path = os.path.join(root, file)
                    stats['total_size'] += os.path.getsize(file_path)
                    
                    # Track last modified
                    mtime = os.path.getmtime(file_path)
                    if not stats['last_modified'] or mtime > stats['last_modified']:
                        stats['last_modified'] = mtime
            
            report = f"""Directory Statistics Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
==================================
Location: {directory}
==================================
Total Size: {stats['total_size'] / (1024*1024):.2f} MB
Total Files: {stats['file_count']}
Total Folders: {stats['folder_count']}
Last Modified: {datetime.fromtimestamp(stats['last_modified']).strftime('%Y-%m-%d %H:%M:%S')}
"""
            # Save and show report
            self.save_and_show_report(report, "directory_stats")
            return report
            
        except Exception as e:
            return f"Error getting directory stats: {str(e)}"

if __name__ == "__main__":
    fm = FileManager()
   
    fm.organize_files("downloads")