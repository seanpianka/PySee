class ImageHost:
    SUPPORTED_HOSTS = ()

    def upload(self, *args, **kwargs):
        raise NotImplementedError('Unable to upload from base class without overridden method.')

    @staticmethod
    def get_image_host_by_name(image_host_name):
        for image_host in ImageHost.SUPPORTED_HOSTS:
            if image_host.HOST_NAME.lower() == image_host_name.lower():
                return image_host()
        return None


from pysee.hosts.imgur import ImgurHost
from pysee.hosts.slimg import SlimgHost
from pysee.hosts.uploadsim import UploadsimHost


ImageHost.SUPPORTED_HOSTS = (ImgurHost, SlimgHost, UploadsimHost)
