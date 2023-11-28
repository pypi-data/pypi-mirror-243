from neumai.DataConnectors import WebsiteConnector
from neumai.Shared import Selector
from neumai.Loaders.HTMLLoader import HTMLLoader
from neumai.Chunkers.RecursiveChunker import RecursiveChunker
from neumai.Sources import SourceConnector
from neumai.EmbedConnectors import OpenAIEmbed
from neumai.SinkConnectors import WeaviateSink
from neumai.Pipelines import Pipeline

website_connector =  WebsiteConnector(
    url = "https://www.neum.ai/post/retrieval-augmented-generation-at-scale",
    selector = Selector(
        to_metadata=['url']
    )
)
source = SourceConnector(
  data_connector = website_connector, 
  loader = HTMLLoader(), 
  chunker = RecursiveChunker()
)

openai_embed = OpenAIEmbed(
  api_key = "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",
)

weaviate_sink = WeaviateSink(
  url = "https://2dmk3chdsh2j9ycraueabw.c0.us-west1.gcp.weaviate.cloud",
  api_key = "BWBuJJ6RS7aJE7qInsN8dPMogCjT646eYkXt",
  class_name = "Weaviasdlasd",
)

pipeline = Pipeline(
  sources=[source], 
  embed=openai_embed, 
  sink=weaviate_sink
)
pipeline.run()

results = pipeline.search(
  query="What are the challenges with scaling RAG?", 
  number_of_results=3
)

for result in results:
  print(result.metadata)
