import cloudinary
import cloudinary.uploader
from django_rest.settings import CLOUDINARY_UPLOAD_FOLDER


def uploadFile(file):
  try:
    result = cloudinary.uploader.upload(file, folder=CLOUDINARY_UPLOAD_FOLDER, resource_type="auto")
    return result['url']
  except Exception as err:
    print(err)
    return None


def deleteFile(file):
  try:
    parts = file.name.split('.')
    content_type = file.content_type.split('/')[0]
    file_name = file.name
    if content_type == 'image':
      file_name = parts[0]
    result = cloudinary.uploader.destroy(file_name)
    if result['result'] == 'ok':
      return True
    return False
  except Exception as err:
    print(err)
    return False