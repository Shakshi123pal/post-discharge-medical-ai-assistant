from duckduckgo_search import DDGS

def web_search(query:str, max_results:int=3):
    with DDGS() as ddgs:
        hits = ddgs.text(query, max_results=max_results)
        return [{"title":h["title"], "href":h["href"], "snippet":h["body"]} for h in hits]
