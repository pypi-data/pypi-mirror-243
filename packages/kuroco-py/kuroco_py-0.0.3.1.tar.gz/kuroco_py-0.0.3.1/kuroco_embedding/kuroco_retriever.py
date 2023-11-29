import asyncio

from dataclasses import dataclass
from typing import List, Union, Tuple
from pydantic import Extra
from langchain.schema.retriever import BaseRetriever
from langchain.schema.document import Document
from langchain.docstore.document import Document
import pandas as pd

THRESHOLD = 0.8

PROCESSING_TYPES: tuple = ("query", "topics_recommandation", "classification", "keywords_global", "keywords_per_topics", "sentiments_analysis", "appreciation_analysis")
@dataclass
class KurocoRetriever (BaseRetriever, extra=Extra.allow):
    """
    KurcoRetriever is a retriever that uses KurocoEmbedding to search for similar documents, topics recommendations, classifications or keywords search.
    It is designed to be used in Langchain.

    It requires a KurocoEmbedding instance and a list of relevant columns to search for.

    Extra Attributes:
        _embedder (KurocoEmbedding): The KurocoEmbedding object used for embedding requests
        _relevant (list): The list of relevant columns to search for
        _threshold (float): The threshold score for the similarity search
        _processing_type (str): The processing type of the retriever, one of PROCESSING_TYPES
        _limit (int): The maximum number of results to return

    Examples:
        >>> from kuroco import KurocoAPI, KurocoEmbedding
        >>> k_api = KurocoAPI.load_from_file(path='kuroco.json')
        >>> k_emb = KurocoEmbedding(('Shops', 'Zones'), k_api)
        >>> k_retriever = KurocoRetriever(k_emb, 'subject')
        >>> def format_docs(docs):
        >>>     return "\n\n".join([d.page_content for d in docs])
        >>> chain = (
        >>>     {"context": k_retriever | format_docs, "question": RunnablePassthrough()}
        >>>     | prompt
        >>>     | model
        >>>     | StrOutputParser()
        >>> )
        >>> chain.invoke("query")

    """
    _embedder: 'KurocoEmbedding'
    _relevant: list
    _threshold: float
    _limit: Union[int, None]

    def __init__(self, 
                 k_emb: 'KurocoEmbedding', 
                 relevant: Union[List[str], Tuple[str], str], 
                 threshold: float = THRESHOLD, 
                 limit: Union[int, None] = None, 
                 processing_type: str = "query"):
        """
        Constructor for the KurocoRetriever class.

        Parameters:
            k_emb (KurocoEmbedding): The KurocoEmbedding object used for embedding requests
            relevant (list | tuple | str): The list of relevant columns to search for
            threshold (float): The threshold score for the similarity search
            limit (int): The maximum number of results to return
            processing_type (str): The processing type of the retriever, one of PROCESSING_TYPES

        Raises:
            AssertionError: If the types of the parameters are not correct
            AssertionError: If the processing type is not one of PROCESSING_TYPES
        """
        BaseRetriever.__init__(self)

        self.embedder = k_emb

        assert isinstance(relevant, (list, tuple, str)), "Relevant must be a list, tuple or string"
        self.relevant = relevant
        
        assert isinstance(threshold, float) and 0 <= threshold <= 1, "Threshold must be a float between 0 and 1"
        self.threshold = threshold

        assert isinstance(limit, int) or limit is None, "Limit must be an integer or None"
        self.limit = limit

        self._processing_type = processing_type

    @property
    def processing_type(self):
        """
        Getter for the processing type of the retriever.

        Returns:
            str: The processing type of the retriever
        """
        return self._processing_type
    
    @processing_type.setter
    def processing_type(self, value):
        """
        Setter for the processing type of the retriever.

        Parameters:
            value (str): The processing type to set

        Raises:
            AssertionError: If the processing type is not one of PROCESSING_TYPES
        """
        assert value in PROCESSING_TYPES, f"Processing type must be one of {PROCESSING_TYPES}"
        self._processing_type = value

    def _get_relevant_documents(
        self, query: str, *, run_manager, return_as_df: bool = False
    ) -> List[Document]:
        """
        Returns a list of `Document` objects that are relevant to the given `query`.
        The relevance is determined by a similarity search performed by the `embedder`
        object stored in the `metadata` dictionary. The search is limited to `limit`
        results and a `threshold` score. Only the columns specified in the `relevant`
        list of the `metadata` dictionary are considered for the search. The resulting
        `Document` objects have their `page_content` set to the relevant text and their
        `metadata` set to a dictionary containing the source of the document (`kuroco`)
        and the name of the relevant column.
        
        Parameters:
            query (str): The query to search for.
            run_manager (RunManager): The run manager.
            return_as_df (bool): Whether to return the results as a dataframe or not.
            
        Returns:
            List[Document]: A list of `Document` objects that are relevant to the query.


        Notes:
            The `run_manager` parameter is not used in this method, but is required by the
            `BaseRetriever` class.
            Depending on the `processing_type` of the retriever, the query can be a string, a list of strings or a dictionary.

            
        Raises:
            ValueError: If the processing type is not supported

        """
        loop = asyncio.new_event_loop()
        if self.processing_type == "topics_recommandation":
            if not isinstance(query, list):
                query = [query]
            query = list(set(query))
            results:dict = dict()
            for q in query:
                results_df = loop.run_until_complete(self.embedder.recommend_topics(int(q), limit=self.limit, with_score=False, threshold=self.threshold))
                results_df["subject to recommend"] = q
                results[q] = results_df
            # Concat the dict of Dataframes as a single one by grouping by topics to recommend
            results = pd.concat(results.values(), ignore_index=True).set_index("subject to recommend")
        elif self.processing_type == "classification":
            if isinstance(query, dict):
                subjects, query = query["subjects"], query["labels"]
            else:
                subjects = None
            results = loop.run_until_complete(self.embedder.zero_shot_topics_classification(query, with_score=False))
            if subjects:
                results = results[results["subject"].isin(subjects)]
        elif self.processing_type == "keywords_global":
            results = loop.run_until_complete(self.embedder.keywords_search_global(query, with_score=False))
        elif self.processing_type == "keywords_per_topics":
            results = loop.run_until_complete(self.embedder.keywords_search_per_topics(query, with_score=False))
        elif self.processing_type == "query":
            results = loop.run_until_complete(self.embedder.similarity_search(query, limit=self.limit, with_score=False, threshold=self.threshold))
        elif self.processing_type == "sentiments_analysis":
            results = loop.run_until_complete(self.embedder.sentiment_analysis(with_score=False))
        elif self.processing_type == "appreciation_analysis":
            results = loop.run_until_complete(self.embedder.appreciation_analysis(with_score=False))
        else:
            raise ValueError(f"Processing type {self.processing_type} is not supported")
        loop.close()
        # If no relevant column is asked, then transform all the dataframe into a list of documents
        selected_columns = [col for col in self.relevant if col in results.columns] if self.relevant else results.columns
        return [Document(page_content=w, 
                         metadata={"source": "kuroco", 
                                    "field": selected_columns[i]})
                        for v in results.loc[:, selected_columns].values.tolist()
                        for i, w in enumerate(v) if w
                ] if return_as_df is False else results.loc[:, selected_columns]
    