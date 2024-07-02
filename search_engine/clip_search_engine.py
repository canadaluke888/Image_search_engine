from transformers import CLIPProcessor, CLIPModel
import torch
from PIL import Image
import os
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SearchEngine:
    def __init__(self, use_cpu=False, model_directory='CLIP/model', processor_directory='CLIP/processor'):
        """
        Initialize the CLIP model and processor.
        """
        self.model_directory = model_directory
        self.processor_directory = processor_directory
        self.device = torch.device('cpu' if use_cpu or not torch.cuda.is_available() else 'cuda')
        self.model = CLIPModel.from_pretrained(self.model_directory).to(self.device)  # openai/clip-vit-base-patch32
        self.processor = CLIPProcessor.from_pretrained(self.processor_directory)  # openai/clip-vit-base-patch32

    def load_and_process_images(self, directory):
        """
        Load and process images from the directory.

        :type directory: os.PathLike | str
        :param directory:
        :return: A tuple containing a list of images and their corresponding paths.
        """
        images = []
        image_paths = []
        for root, dirs, files in os.walk(directory):
            for filename in files:
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    path = os.path.join(root, filename)
                    try:
                        image = Image.open(path).convert('RGB')
                        images.append(image)
                        image_paths.append(path)
                    except Exception as e:
                        logger.error(f"Error loading image {path}: {e}")
        return images, image_paths

    def search_images(self, directory, semantic_search_phrase, top_k=3):
        """
        Search for the top K images that mathc the search phrase.

        :param directory: Path to directory with images.
        :param semantic_search_phrase: A phrase of what the user is looking for inside one of the images
        :param top_k: Number of top matches to return.
        :return: A list of tuples containing image paths and their scores.
        """
        images, image_paths = self.load_and_process_images(directory)
        if not images:
            logger.warning("No images found in the directory.")

        with torch.no_grad():
            inputs = self.processor(text=[semantic_search_phrase], images=images, return_tensors="pt",
                                    padding=True).to(self.device)
            outputs = self.model(**inputs)

        logits_per_image = outputs.logits_per_image
        values, indices = logits_per_image.squeeze().topk(top_k)

        top_image_paths = [image_paths[int(index.cpu().numpy())] for index in indices]
        top_scores = [round(value.cpu().numpy().tolist(), 3) for value in values]

        return list(zip(top_image_paths, top_scores))

    @staticmethod
    def is_cuda_available():
        return torch.cuda.is_available()
