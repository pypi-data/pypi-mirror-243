from typing import List, Tuple, Union, Dict

import pandas as pd
import asyncio
from kuroco_api import KurocoAPI, KurocoContent

from .kuroco_retriever import KurocoRetriever

from .CONFIG import QUERY_KW, SCORE_DISTANCE_COLUMN_NAME, VECTOR_SEARCH_MODIFIER, LABEL_SCORE_COLUMN_NAME, KEYWORDS_SCORE_COLUMN_NAME, SENTIMENTS_DEFINITIONS, APPRECIATION_DEFINITIONS
from .tools import send_queries


class KurocoEmbedding:
    """
    A class used to represent a KurocoEmbedding object

    Attributes:
    _kuroco_handler (KurocoAPI): The KurocoAPI object used for Kuroco API requests
    _content (KurocoContent): The KurocoContent object used for embedding requests

    Examples:
    >>> # Embedding Instantiated on a single endpoint

    >>> k_emb = KurocoEmbedding(content="test", kuroco_handler= KurocoAPI())

    >>> k_emb.similarity_search("test query")
    """
    _kuroco_embedding_endpoint: str
    _kuroco_handler: KurocoAPI
    _content: List[KurocoContent]

    def __init__(self, 
                content: Union[Tuple[str], List[str], str],
                kuroco_handler: Union[KurocoAPI, 
                                    str, 
                                    None, 
                                    Tuple[str, str, Union[str, int]], 
                                    Dict[str, Union[str, int]]] = None,) -> None:  
        """
        Constructor for the KurocoEmbedding class.

        Parameters:
            content (str, list, tuple): The content to embed
            kuroco_handler (KurocoAPI): The KurocoAPI object used for Kuroco API requests

        Raises:
            AssertionError: If the types of the parameters are not correct
        """
        self.kuroco_handler = kuroco_handler
        self.content = content

    @property
    def content(self):
        """
        The content to embed

        Returns:
            list: The content to embed
        """
        return self._content
    
    @content.setter
    def content(self, value : Union[Tuple[str], List[str], str]):
        """
        Setter for the content to embed

        Parameters:
            value (str, list, tuple): The content to embed

        Raises:
            AssertionError: If the types of the parameters are not correct
        """
        if isinstance(value, str):
            value = (value,)
        assert isinstance(value, (tuple, list)), "Content must be a list or a tuple (of strings) or a single string"
        if isinstance(value, (list, tuple)):
            assert all(isinstance(x, str) for x in value), "Content must be a list or a tuple of strings"
        assert len(set(value)) == len(value), "Content must be a list of unique strings"
        self._content = [KurocoContent(x, x, self.kuroco_handler) for x in value]

    @property
    def kuroco_handler(self):
        """ 
        The KurocoAPI object used for Kuroco API requests

        Returns:
            KurocoAPI: The KurocoAPI object used for Kuroco API requests
        """
        return self._kuroco_handler
    
    @kuroco_handler.setter
    def kuroco_handler(self, value: Union[KurocoAPI, 
                                          str, 
                                          Tuple, 
                                          List, 
                                          Dict[str, Union[str, int]], None]):
        """
        Setter for the KurocoAPI object used for Kuroco API requests

        Parameters:
            value (KurocoAPI, str, tuple, list, dict, None): The KurocoAPI object used for Kuroco API requests

        Raises:
            AssertionError: If the types of the parameters are not correct
        """
        if isinstance(value, KurocoAPI):
            pass
        elif isinstance(value, str):
            value = KurocoAPI.load_from_file(path=value)
        elif value is None:
            value = KurocoAPI()
        elif isinstance(value, (tuple, list)):
            value = KurocoAPI(*value)
        elif isinstance(value, dict):
            value = KurocoAPI(**value)
        else:
            raise AssertionError("KurocoAPI object must be provided as an argument (str, tuple or list) or as an environment variable")
        self._kuroco_handler = value

    def as_retriever(self, relevant: Union[str, List[str], Tuple[str]] = "subject", threshold: float = 0.8, limit: Union[int, None] = None, processing_type: str = "query"):
        """
        Return a KurocoRetriever object from the KurocoEmbedding object

        Parameters:
            relevant (str, list, tuple): The relevant columns to search for
            threshold (float): The threshold score for the similarity search
            limit (int): The maximum number of results to return
            processing_type (str): The processing type of the retriever, one of PROCESSING_TYPES

        Returns:
            KurocoRetriever: The KurocoRetriever object

        Raises:
            AssertionError: If the types of the parameters are not correct
            AssertionError: If the processing type is not one of PROCESSING_TYPES
        """
        return KurocoRetriever(self, relevant=relevant, threshold=threshold, limit=limit, processing_type=processing_type)

    @property
    def paths(self):
        """
        The registered paths to the Kuroco API

        Returns:
            list: The paths to the Kuroco API
        """
        return [content.path for content in self.content]
    
    # Methods for indirect query search
    async def similarity_search(self, query: str, context: str = "", limit: int = 10, filter: dict = {}, with_score: bool = False, threshold: float = 0.0):
        """
        Search for similar entries to a query

        Parameters:
        query (str): The query to search for similar entries to
        context (str): The context to attach to the query for related value, default to empty string
        limit (int): The maximum number of entries to return, 0 for all
        filter (str): The filter to apply to the query
        with_score (bool): Whether to return the similarity score or not
        threshold (float): The similarity threshold to apply to the query

        Returns:
        dataframe: A dataframe of similar entries to the query, with their similarity score as last column if needed and limited to limit passed as parameter and by respecting the threshold provided

        Note:
        This method is asynchronous.

        TODO: Implement Document search
        """
        values = await self.similarity_search_by_query(query=query,
                                                        context=context,
                                                        limit=limit,
                                                        filter=filter,
                                                        threshold=threshold) if not with_score else await self.similarity_search_by_query_with_score(query=query, 
                                                                                                                                                     context=context,
                                                                                                                                                        limit=limit, 
                                                                                                                                                        filter=filter, 
                                                                                                                                                        threshold=threshold)
        return values

    async def similarity_search_by_query(self, query: str, context: str = "", limit: int = 10, filter: dict = {}, threshold: float = 0.0):
        """
        Search for similar entries to a query

        Parameters:
        query (str): The query to search for similar entries to
        limit (int): The maximum number of entries to return, 0 for all
        filter (dict): The filter to apply to the query
        threshold (float): The similarity threshold to apply to the query

        Returns:
        dataframe: A dataframe of similar entries to the query

        Note:
        This method is asynchronous.
        """
        result = await self.similarity_search_by_query_with_score(query=query, context=context, limit=limit, filter=filter, threshold=threshold)
        return result.drop(columns=[SCORE_DISTANCE_COLUMN_NAME], errors='ignore')

    async def similarity_search_by_query_with_score(self, query: str, context: str = "", limit: int = 10, filter: dict = {}, threshold: float = 0.0):
        """
        Search for similar entries to a query and return the similarity score

        Parameters:
        query (str): The query to search for similar entries to
        context (str): The context to attach to the query for related value
        limit (int): The maximum number of entries to return, 0 for all
        filter (dict): The filter to apply to the query
        threshold (float): The similarity threshold to apply to the query

        Returns:
        dataframe: A dataframe of similar entries to the query with their similarity score for last column

        Note:
        This method is asynchronous.
        """
        if context:
            if isinstance(context, str):
                query = """
                Subject: {query}
                
                Context: {context}
                """.format(query=query, context=context)
            elif isinstance(context, (list, tuple)):
                query = """
                Subject: {query}
                
                Context: {context}
                """.format(query=query, context="\n".join(context))
            elif isinstance(context, dict):
                query = """
                Subject: {query}
                
                {context}
                """.format(query=query, context="\n".join([f"{key}: {value}" for key, value in context.items()]))
        query = query.strip().encode('utf-8', 'ignore').decode('utf-8')
        params = { QUERY_KW: query, "filter": filter }
        return (await send_queries(paths=self.paths, 
                                   kuroco_handler=self.kuroco_handler, 
                                   params=params, 
                                   limit=limit, 
                                   threshold=threshold))

    async def recommend_topics(self, topics_id: Union[str, int], limit: int = 10, threshold: float = 0.0, with_score: bool = False):
        """
        Get topic recommendation from topic id provided

        Parameters:
        topics_id (str, int): The topic id to search for similar entries to
        limit (int): The maximum number of entries to return, 0 for all
        threshold (float): The similarity threshold to apply to the query
        
        Returns:
        dataframe: A dataframe of similar entries to the topic id
        """
        return await self.similarity_search_by_topic_id(topics_id=topics_id, limit=limit, threshold=threshold, with_score=with_score)

    async def similarity_search_by_topic_id(self, topics_id: Union[str, int], limit: int = 10, filter: dict ={}, threshold: float = 0.0, with_score: bool = False):
        """
        Search for similar entries to a topic id

        Parameters:
        topics_id (str, int): The topic id to search for similar entries to
        limit (int): The maximum number of entries to return, 0 for all
        threshold (float): The similarity threshold to apply to the query
        with_score (bool): Whether to return the similarity score or not

        Returns:
        dataframe: A dataframe of similar entries to the topic id

        Note:
        This method is asynchronous.
        """
        assert isinstance(topics_id, int) or isinstance(topics_id, str) and topics_id.isdigit(), "topics_id must be a valid integer" 
        params = { QUERY_KW: str(topics_id), VECTOR_SEARCH_MODIFIER: 'topics_id', "filter": filter }
        results = (await send_queries(paths=self.paths, 
                                   kuroco_handler=self.kuroco_handler, 
                                   params=params, 
                                   limit=limit, 
                                   threshold=threshold))
        if not with_score:
            results = results.drop(columns=[SCORE_DISTANCE_COLUMN_NAME], errors='ignore')
        return results

    async def get_labels_score(self, 
                               labels: Union[str, List[str], Tuple[str]], 
                               contexts: Union[str, List[str], Tuple[str]] = "", 
                               limit: int = 10, 
                               threshold: float = 0.0):
        """
        Get the score of the labels provided

        Parameters:
        labels (str, list, tuple): The labels to search for similar entries to
        contexts (str, list, tuple): The contexts to attach to the labels for related value
        limit (int): The maximum number of entries to return, 0 for all
        threshold (float): The similarity threshold to apply to the query

        Returns:
        dataframe: A dataframe containing the labelled data
        """
        #  First we check if the labels are valid
        if isinstance(labels, str):
            labels = (labels,)
        if isinstance(contexts, str):
            contexts = (contexts,)
        assert isinstance(labels, (tuple, list)), "Labels must be a list or a tuple (of strings) or a single string"
        assert isinstance(contexts, (tuple, list)), "Contexts must be a list or a tuple (of strings) or a single string"
        assert all(isinstance(x, str) for x in labels), "Labels must be a list or a tuple of strings"
        assert all(isinstance(x, (str, dict)) for x in contexts), "Contexts must be a list or a tuple of strings"

        if len(contexts) == 1 and len(labels) > 1:
            contexts = list(contexts) * len(labels)
        # Check that the number of labels and contexts are the same
        assert len(labels) == len(contexts), "The number of labels and contexts must be the same"

        # We get the score for each label with multiple queries async
        results = await asyncio.gather(*[self.similarity_search_by_query_with_score(label, context, limit=0, threshold=0.0) for label, context in zip(labels, contexts)])
        # Add the column of the label id
        for i, result in enumerate(results):
            result['label_name'] = labels[i] 
        concated = pd.concat(results)
        concated.rename(columns={'index': 'topics_id', SCORE_DISTANCE_COLUMN_NAME: LABEL_SCORE_COLUMN_NAME}, inplace=True)

        # Transform to readable score
        concated[LABEL_SCORE_COLUMN_NAME] = 1 - concated[LABEL_SCORE_COLUMN_NAME]
        concated.reset_index(inplace=True)

        return concated

    async def zero_shot_topics_classification(self, 
                                              labels: Union[str, List[str], Tuple[str]], 
                                              contexts: Union[str, List[str], Tuple[str]] = "",
                                              with_score: bool = False):
        """
        Get classification from labels provided

        Parameters:
        labels (str, list, tuple): The labels to search for similar entries to
        contexts (str, list, tuple): The contexts to attach to the labels for related value
        with_score (bool): Whether to return the similarity score or not, default to False

        Returns:
        dataframe: A dataframe containing the labelled data
        """
        concated = await self.get_labels_score(labels=labels, contexts=contexts)
        # Get the max score for each topics_id
        max_indices = concated.groupby(concated.topics_id).apply(lambda x: x[LABEL_SCORE_COLUMN_NAME].idxmax())
        result_df = concated.loc[max_indices]
        result_df.set_index('topics_id', inplace=True)
        if not with_score:
            result_df = result_df.drop(columns=[LABEL_SCORE_COLUMN_NAME], errors='ignore')
        return result_df  

    async def sentiment_analysis(self, with_score: bool = False, language: str = "eng"):
        sentiment_def = SENTIMENTS_DEFINITIONS[language]
        # Get the sentiments results
        classification = await self.zero_shot_topics_classification(labels=list(sentiment_def.keys()), contexts=list([{"Definition:" : " ".join(v)} for v in sentiment_def.values()]), with_score=True)

        classification.rename(columns={'label_name': 'sentiment', LABEL_SCORE_COLUMN_NAME: 'sentiment_score'}, inplace=True)
        
        if not with_score:
            classification.drop(columns=['sentiment_score'], inplace=True)
        else:
            classification['sentiment_score'] = classification['sentiment_score'].apply(lambda x: 1 - x)
        return classification

    async def appreciation_analysis(self, with_score: bool = False, language: str = "eng"):
        """
        Get appreciation from labels provided
        
        Parameters:
        with_score (bool): Whether to return the similarity score or not, default to False
        language (str): The language to use for the appreciation analysis, default to "eng"
        
        Returns:
        dataframe: A dataframe containing the labelled data
        
        Note:
        This method is asynchronous.
        """
        # Get the appreciation results
        appreciation_def = APPRECIATION_DEFINITIONS[language]
        classification = await self.zero_shot_topics_classification(labels=list(appreciation_def.keys()), contexts=list([{"Definition:" : " ".join(v)} for v in appreciation_def.values()]), with_score=True)
        classification.rename(columns={'label_name': 'appreciation', LABEL_SCORE_COLUMN_NAME: 'appreciation_score'}, inplace=True)
        if not with_score:
            classification.drop(columns=['appreciation_score'], inplace=True)
        else:
            classification['appreciation_score'] = classification['appreciation_score'].apply(lambda x: 1 - x)
        return classification

    async def keywords_search_global(self, 
                                     keywords: Union[str, List[str], Tuple[str]], 
                                     contexts: Union[str, List[str], Tuple[str]],
                                     with_score: bool = False):
        """
        Search for the relevance of the provided keywords for the defined content of the KurocoEmbedding object

        Parameters:
        keywords (str, list, tuple): The keywords to search for relevance
        contexts (str, list, tuple): The contexts to attach to the keywords for related value
        with_score (bool): Whether to return the relevance score or not


        Returns:
        dataframe: A dataframe containing the relevance score of the keywords per content defined in the KurocoEmbedding object
        """
        concated = await self.keywords_search_per_topics(keywords=keywords, contexts=contexts, with_score=True)
        score_per_label = concated.groupby(['keywords']).agg({KEYWORDS_SCORE_COLUMN_NAME: 'mean'})
        if not with_score:
            score_per_label = score_per_label.drop(columns=[KEYWORDS_SCORE_COLUMN_NAME], errors='ignore')        
        return score_per_label

    async def keywords_search_per_topics(self, 
                                         keywords: Union[str, List[str], Tuple[str]], 
                                         contexts: Union[str, List[str], Tuple[str]],
                                         with_score: bool = False):
        """
        Search for the relevance of the provided keywords for the defined content of the KurocoEmbedding object

        Parameters:
        keywords (str, list, tuple): The keywords to search for relevance
        contexts (str, list, tuple): The contexts to attach to the keywords for related value
        with_score (bool): Whether to return the relevance score or not


        Returns:
        dataframe: A dataframe containing the relevance score of the keywords per content defined in the KurocoEmbedding object
        """
        concated = await self.get_labels_score(labels=keywords, contexts=contexts)
        concated.rename(columns={'label_name': 'keywords', LABEL_SCORE_COLUMN_NAME: KEYWORDS_SCORE_COLUMN_NAME}, inplace=True)
        score_per_label = concated.groupby(['keywords', 'topics_id', 'subject']).agg({KEYWORDS_SCORE_COLUMN_NAME: 'mean'})
        if not with_score:
            score_per_label = score_per_label.drop(columns=[KEYWORDS_SCORE_COLUMN_NAME], errors='ignore')        
        return score_per_label

    async def similarity_search_with_score(self, query: str, limit: int = 10, threshold: float = 0.0):
        """
        Search for similar entries to a query and return the similarity score

        Parameters:
        query (str): The query to search for similar entries to
        limit (int): The maximum number of entries to return, 0 for all

        Returns:
        dataframe: A dataframe of similar entries to the query with their similarity score for last column 
        
        Note:
        This method is asynchronous. Use similarity_search_with_score_sync for a synchronous version
        """
        return await self.similarity_search_by_query_with_score(query, limit, threshold)
