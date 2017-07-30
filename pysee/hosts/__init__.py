class ImageHost:
    def __init__(self):
        pass

    def upload(self, *args, **kwargs):
        raise NotImplementedError('Unable to upload from base class without overridden method.')


from pysee.hosts import imgur, slimg, uploadsim
