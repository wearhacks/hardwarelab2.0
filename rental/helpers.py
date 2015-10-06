import os
def get_image_filename(instance, old_filename):
  folder = ''
  if hasattr(instance, 'MEDIA_URL'):
    folder = instance.MEDIA_URL

  filename = os.path.join(
    os.path.dirname(old_filename),
    folder,
    old_filename
  )
  return filename
