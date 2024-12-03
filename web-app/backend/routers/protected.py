from fastapi import APIRouter, HTTPException, Depends, Query
from elasticsearch import Elasticsearch
from auth import decode_access_token
from typing import Optional, List

# Initialize Elasticsearch client
es_client = Elasticsearch(hosts=[{"host": "elasticsearch", "port": 9200, "scheme": "http"}])

# Create a router for protected routes
router = APIRouter()

@router.get("/elasticsearch/{index}")
def get_events(
    index: str,
    page: int = 1,
    size: int = 10,
    state: Optional[str] = None,
    event_type: Optional[str] = None,
    year: Optional[int] = None,
    username: str = Depends(decode_access_token)
):
    """Retrieve paginated events with optional filters: state, event type, or year."""
    try:
        query = {"bool": {"must": []}}
        if state:
            query["bool"]["must"].append({"term": {"STATE.keyword": state}})
        if event_type:
            query["bool"]["must"].append({"term": {"EVENT_TYPE.keyword": event_type}})
        if year:
            query["bool"]["must"].append({"term": {"YEAR": year}})
        
        start = (page - 1) * size
        response = es_client.search(index=index, query=query, from_=start, size=size)
        return {"results": [hit["_source"] for hit in response["hits"]["hits"]]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Elasticsearch query failed: {e}")


@router.get("/elasticsearch/{index}/search")
def search_events(
    index: str,
    field: str,
    keyword: str,
    size: int = 10,
    username: str = Depends(decode_access_token)
):
    """Search events by keyword in a specified field."""
    try:
        response = es_client.search(
            index=index,
            query={"match": {field: keyword}},
            size=size
        )
        return {"results": [hit["_source"] for hit in response["hits"]["hits"]]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Elasticsearch query failed: {e}")


@router.get("/elasticsearch/{index}/aggregate/event_type")
def aggregate_by_event_type(index: str, size: int = 10, username: str = Depends(decode_access_token)):
    """Aggregate events by event type and return counts."""
    try:
        response = es_client.search(
            index=index,
            aggs={
                "event_types": {
                    "terms": {"field": "EVENT_TYPE.keyword", "size": size}
                }
            },
            size=0
        )
        return {"aggregations": response["aggregations"]["event_types"]["buckets"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Elasticsearch aggregation failed: {e}")


@router.get("/elasticsearch/{index}/aggregate/state")
def aggregate_by_state(index: str, size: int = 10, username: str = Depends(decode_access_token)):
    """Aggregate events by state and return counts."""
    try:
        response = es_client.search(
            index=index,
            aggs={
                "states": {
                    "terms": {"field": "STATE.keyword", "size": size}
                }
            },
            size=0
        )
        return {"aggregations": response["aggregations"]["states"]["buckets"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Elasticsearch aggregation failed: {e}")


@router.get("/elasticsearch/{index}/filter/state")
def filter_by_state(
    index: str,
    states: List[str] = Query(...),
    size: int = 10,
    username: str = Depends(decode_access_token)
):
    """Retrieve events filtered by one or multiple states."""
    try:
        response = es_client.search(
            index=index,
            query={"terms": {"STATE.keyword": states}},
            size=size
        )
        return {"results": [hit["_source"] for hit in response["hits"]["hits"]]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Elasticsearch query failed: {e}")
