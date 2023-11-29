import sys
sys.path.append('../kuroco_api')

from .kuroco_embedding import KurocoEmbedding
from .CONFIG import ACCEPTED_LANGUAGES
# Environment variables

__all__ = [
    "KurocoEmbedding", 
    "ACCEPTED_LANGUAGES",
]