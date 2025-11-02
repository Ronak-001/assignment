"""
Google Docs Manager
Handles fetching and listing Google Docs from user's account
"""

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from auth_manager import AuthManager


class GoogleDocsManager:
    """Manages Google Docs operations"""
    
    def __init__(self, credentials):
        """
        Initialize with authenticated credentials
        
        Args:
            credentials: OAuth 2.0 credentials object
        """
        self.service = build('drive', 'v3', credentials=credentials)
        self.docs_service = build('docs', 'v1', credentials=credentials)
    
    def list_documents(self):
        """
        Fetch all Google Docs from user's account
        
        Returns:
            List of dictionaries containing document info (id, name, modified_time)
        """
        try:
            documents = []
            
            # Query for Google Docs files
            query = "mimeType='application/vnd.google-apps.document' and trashed=false"
            
            # Fetch documents
            results = self.service.files().list(
                q=query,
                pageSize=100,
                fields="files(id, name, modifiedTime)",
                orderBy="modifiedTime desc"
            ).execute()
            
            items = results.get('files', [])
            
            for item in items:
                documents.append({
                    'id': item['id'],
                    'name': item['name'],
                    'modified_time': item.get('modifiedTime', '')
                })
            
            return documents
        
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []
    
    def get_document_content(self, document_id):
        """
        Fetch full content of a Google Doc
        
        Args:
            document_id: ID of the Google Doc
            
        Returns:
            Text content of the document
        """
        try:
            doc = self.docs_service.documents().get(documentId=document_id).execute()
            
            # Extract text content
            text_content = []
            
            def extract_text(element):
                """Recursively extract text from document elements"""
                if 'paragraph' in element:
                    para = element['paragraph']
                    if 'elements' in para:
                        for elem in para['elements']:
                            if 'textRun' in elem:
                                text_content.append(elem['textRun'].get('content', ''))
                elif 'table' in element:
                    # Handle tables
                    table = element['table']
                    if 'tableRows' in table:
                        for row in table['tableRows']:
                            if 'tableCells' in row:
                                for cell in row['tableCells']:
                                    if 'content' in cell:
                                        for content_elem in cell['content']:
                                            extract_text(content_elem)
            
            # Process document body
            if 'body' in doc and 'content' in doc['body']:
                for element in doc['body']['content']:
                    extract_text(element)
            
            return ''.join(text_content).strip()
        
        except HttpError as error:
            print(f"An error occurred while fetching document: {error}")
            return ""


