import cloudinary
import cloudinary.uploader
from django_rest.settings import CLOUDINARY_UPLOAD_FOLDER


def uploadFile(file):
  try:
    result = cloudinary.uploader.upload(file, folder=CLOUDINARY_UPLOAD_FOLDER, resource_type="auto")
    return {
      'id': result['public_id'],
      'url': result['url']
    }
  except Exception as err:
    print(err)
    return None


def deleteFile(public_id):
  try:
    cloudinary.uploader.destroy(public_id)
    return True
  except Exception as err:
    print(err)
    return False