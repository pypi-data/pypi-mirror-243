"""
pollinations.types.ImageModel

Classes:
    ImageModel (types.ImageModel): Text-to-image generative AI model.
    ImageObject (types.ImageObject): Image object.
"""

import requests
from .. import abc
from .ImageObject import ImageObject


@abc.resource(deprecated=False)
class ImageModel:
    """
    pollinations.ai.types.ImageModel

    Paremeters:
        save_file (str): File to save the image to.

    Variables:
        save_file (str): File to save the image to.
        prompt (str): The last prompt used. (If any)
        filter (list): List of words for the ai not to generate with.
        default_filter (list): List of general inappropriate words. (abc.BANNED_WORDS)
        data (object): types.ImageObject or list of types.ImageObject
        self.is_filtered (bool): Whether the ai is filtered or not.

    Functions:
        set_filter(object, filter: list): Set the filter for the ai.
        generate(ImageObject, prompt: str): Generate an image.
        generate_batch(list, prompts: list): Generate a batch of images.
        save(ImageObject, save_file: str=None): Save the image.
        load(bin, save_file: str): Load the image. (returns binary)
        image(ImageObject): Returns self.data
    """

    def __init__(self, save_file: str = "tkr-Image.jpg", *args, **kwargs) -> None:
        self.__base: str = "image.pollinations"
        self.save_file: str = save_file
        self.prompt: str = None
        self.default_filter: list = abc.BANNED_WORDS
        self.filter: list = default_filter
        self.data: object = object
        self.is_filtered: bool = False

    def __repr__(self, *args, **kwargs) -> str:
        return f"ImageModel(save_file={self.save_file})"

    @abc.resource(deprecated=False)
    def set_filter(self, filter: list, *args, **kwargs) -> object:
        """
        pollinations.ai.types.ImageModel.set_filter

        Parameters:
            filter (list): List of words for the ai not to generate with.

        Return:
            self (ImageModel): Returns self.
        """ ""
        self.filter: list = filter
        return self

    @abc.resource(deprecated=False)
    def generate(self, prompt: str, *args, **kwargs) -> str:
        """
        pollinations.ai.types.ImageModel.generate

        Parameters:
            prompt (str): The prompt for the image.

        Return:
            ImageObject (class): Returns the ImageObject for the generated image.
        """
        words: list = prompt.split(" ")

        for word in words:
            if word in self.filter:
                self.is_filtered: bool = True
                return Exception(f"types.ImageModel >>> InvalidPrompt (filtered)")

        self.prompt: str = prompt
        request = requests.get(f"{abc.proto}{self.__base}{abc.ai}{prompt}")
        self.data: ImageObject = ImageObject(
            prompt, request.url, request.headers["Date"], content=request.content
        )
        self.data.save: object = self.save

        return self.data

    @abc.resource(deprecated=False)
    def generate_batch(
        self,
        prompts: list,
        save: bool = False,
        path: str = None,
        naming: str = "counter",
        *args,
        **kwargs,
    ) -> list:
        """
        pollinations.ai.types.ImageModel.generate_batch

        Parameters:
            prompts (list): List of prompts for the images.
            save (bool): Whether to save the images or not.
            path (str): Path to save the images to.
            naming (str): Naming convention for the images. (counter or prompt)

        Return:
            ImageObject (list): Returns a list of ImageObjects for the generated images.
        """
        self.prompts: list = prompts
        self.data: list = []
        counter: int = 1

        for prompt in prompts:
            words: list = prompt.split(" ")
            for word in words:
                if word in self.filter:
                    self.is_filtered: bool = True
                    return Exception(f"types.ImageModel >>> InvalidPrompt (filtered)")
            request = requests.get(f"{abc.proto}{self.__base}{abc.ai}{prompt}")
            image: ImageObject = ImageObject(
                prompt, request.url, request.headers["Date"], content=request.content
            )
            image.save: object = self.save
            self.data.append(image)

            if save:
                if naming == "counter":
                    file_name: str = counter
                else:
                    file_name: str = prompt
                with open(
                    f'{path if path else ""}/batch{file_name}-pollinations.jpg', "wb"
                ) as handler:
                    handler.write(image.content)

            counter += 1
        return self.data

    @abc.resource(deprecated=False)
    def save(self, save_file: str = None, *args, **kwargs) -> ImageObject:
        """
        pollinations.ai.types.ImageModel.save

        Parameters:
            save_file (str): File name to save the image to.

        Return:
            ImageObject (class): Returns the ImageObject for the saved image.
        """
        if not self.is_filtered:
            if save_file is None:
                save_file = self.save_file

            with open(save_file, "wb") as handler:
                handler.write(self.data.content)

            return self.data
        else:
            return Exception(f"types.ImageModel >>> Cannot Save (filtered)")

    @abc.resource(deprecated=False)
    def load(self, load_file: str = None, *args, **kwargs) -> str:
        """
        pollinations.ai.types.ImageModel.load

        Parameters:
            load_file (str): File name to load the image from.

        Return:
            str (binary): Returns the binary info of the image.
        """
        if load_file is None:
            load_file = self.save_file

        with open(load_file, "rb") as handler:
            return handler.read()

    @abc.resource(deprecated=False)
    def image(self, *args, **kwargs) -> ImageObject:
        """
        pollinations.ai.types.ImageModel.image

        Return:
            ImageObject (class): Returns the ImageObject for the image.
        """
        return self.data
