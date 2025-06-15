from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SERVICE_ACCOUNT_FILE = 'carbide-theme-463017-g6-d07fccde9f5e.json'
FOLDER_ID = '1-C8jZikgSEI42-caiRcPCniRi1zneEdO'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=["https://www.googleapis.com/auth/drive"]
)
service = build("drive", "v3", credentials=credentials)

def upload_to_gdrive(filepath):
    file_metadata = {"name": filepath.split("/")[-1], "parents": [FOLDER_ID]}
    media = MediaFileUpload(filepath, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    return f"https://drive.google.com/file/d/{file.get('id')}/view?usp=sharing"