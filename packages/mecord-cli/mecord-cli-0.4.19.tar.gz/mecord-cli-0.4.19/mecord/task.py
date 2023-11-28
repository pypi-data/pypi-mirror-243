import requests
import os
import json
from urllib.parse import *
from PIL import Image

from mecord import xy_pb
from mecord import store
from mecord import taskUtils
from mecord import utils
from pathlib import Path

def needChangeValue(taskUUID, data, type, key):
    if "type" not in data:
        taskUtils.taskPrint(taskUUID, "result is not avalid")
        return False
    if data["type"] != type:
        return False
    if "extension" not in data or key not in data["extension"] or len(data["extension"][key]) == 0:
        return True
    return False
            
def checkResult(taskUUID, data):
    for it in data["result"]:
        if needChangeValue(taskUUID, it, "text", "cover_url"):
            it["extension"]["cover_url"] = ""
        if needChangeValue(taskUUID, it, "audio", "cover_url"):
            it["extension"]["cover_url"] = ""
        if needChangeValue(taskUUID, it, "image", "cover_url"):
            it["extension"]["cover_url"] = ""
        if needChangeValue(taskUUID, it, "video", "cover_url"):
            it["extension"]["cover_url"] = ""
            
        if "extension" in it and "cover_url" in it["extension"] and len(it["extension"]["cover_url"]) > 0:
            cover_url = str(it["extension"]["cover_url"])
            parsed_url = urlparse(cover_url)
            params = parse_qs(parsed_url.query)
            #add width & height if need
            if "width" not in params and "height" not in params:
                w, h = utils.getOssImageSize(cover_url)
                if w > 0 and h > 0:
                    params["width"] = w
                    params["height"] = h
                    it["extension"]["width"] = w
                    it["extension"]["height"] = h
            #remove optional parameters
            for k in ["Expires","OSSAccessKeyId","Signature","security-token"]:
                params.pop(k, None)
            if "width" in it["extension"]:
                if isinstance(it["extension"]["width"], str):
                    it["extension"]["width"] = int(it["extension"]["width"])
            if "height" in it["extension"]:
                if isinstance(it["extension"]["height"], str):
                    it["extension"]["height"] = int(it["extension"]["height"])
            updated_query_string = urlencode(params, doseq=True)
            final_url = parsed_url._replace(query=updated_query_string).geturl()
            it["extension"]["cover_url"] = final_url
        
def updateProgress(data, progress=50, taskUUID=None):
    realTaskUUID = taskUUID
    country = None
    if store.is_multithread() or taskUUID != None:
        country = taskUtils.taskCountryWithUUID(taskUUID)
    else:
        firstTaskUUID, country = taskUtils.taskInfoWithFirstTask()
        if realTaskUUID == None:
            realTaskUUID = firstTaskUUID
    if country == None:
        country = "test"
    return xy_pb.TaskUpdateProgress(country, realTaskUUID, progress, json.dumps(data))
    