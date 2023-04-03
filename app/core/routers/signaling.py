from fastapi.responses import HTMLResponse, Response
from pathlib import Path
from fastapi import APIRouter, Depends, Request, status
import json

router = APIRouter(include_in_schema=False)

data = {}

@router.get("/")
def ok():
    return Response(content='{"status":"ok"}', status_code=200, media_type='application/json')

@router.post("/offer")
async def offer(request: Request) -> Response:
    """ Offer post

    Args:
        request (Request): request from offer

    Returns:
        Response: status_code
    """
    if request.form["type"] == "offer":
        data["offer"] = {"id": request.form["id"], "type": request.form["type"], "sdp": request.form["sdp"]}
        return Response(status_code=200)
    else:
        return Response(status_code=400)
    
@router.post("/answer")
async def answer(request: Request) -> Response:
    """_summary_

    Args:
        request (Request): request from answer

    Returns:
        Response: status_code
        
        이 부분 자용이랑 얘기해봐야댈듯. 어떤 데이터가 오가는지 이해 잘 안됨.
    """
    req = request.form.to_dict()
    req_key = list(req.keys())
    req_key = req_key[0]
    
    req_result = json.loads(req_key)
    
    if req_result["type"] == "Answer":
        data["answer"] = {"id" : req_result['id'], "type" : req_result['type'], "sdp":req_result['sdp']}
        return Response(status_code= 200)
    else: 
        return Response(status_code= 400)        
    
@router.get("/get_offer")
def get_offer():
    # 카메라 데이터 확인
    if "offer" in data:
        # 카메라 데이터 json객체로 저장
        j = json.dumps(data["offer"])
        # json객체로 저장한 데이터 삭제
        del data["offer"]
        # 상태 코드 및 json파일 반환
        return Response(j, status=200, media_type='application/json')
    else: 
        return Response(status=503)    
    
@router.get("/get_answer")
def get_answer():
    if "answer" in data:
        j = json.dumps(data["answer"])
        del data["answer"]
        return Response(j, status = 200, media_type='application/json')
    else:
        return Response(status = 503)    
