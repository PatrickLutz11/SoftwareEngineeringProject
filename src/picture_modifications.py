import cv2

class PictureModifications:
    
    def resize_the_picture(img:cv2.typing.MatLike) -> cv2.typing.MatLike:
        """Scaling the picture to a suitable size

        Args:
            img (cv2.typing.MatLike): Original image

        Returns:
            cv2.typing.MatLike: Resized image
        """
        
        scale = 70
        width = int(img.shape[1] * scale / 100)
        height = int(img.shape[0] * scale / 100)

        resized_img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
        return resized_img