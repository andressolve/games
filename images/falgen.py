import os, sys, json, time, urllib.request
KEY = os.environ["FAL_KEY"]; MODEL = "fal-ai/flux/dev"
def post(u,b):
    r=urllib.request.Request(u,data=json.dumps(b).encode(),headers={"Authorization":f"Key {KEY}","Content-Type":"application/json"})
    return json.load(urllib.request.urlopen(r,timeout=120))
def get(u):
    r=urllib.request.Request(u,headers={"Authorization":f"Key {KEY}"})
    return json.load(urllib.request.urlopen(r,timeout=120))
def gen(p,s,o):
    j=post(f"https://queue.fal.run/{MODEL}",{"prompt":p,"image_size":s,"num_inference_steps":34,"guidance_scale":3.5,"num_images":1,"enable_safety_checker":True})
    su,ru=j["status_url"],j["response_url"]
    while True:
        st=get(su).get("status")
        if st=="COMPLETED":break
        if st in("FAILED","ERROR"):raise SystemExit("failed")
        time.sleep(4)
    res=get(ru); url=res["images"][0]["url"]
    d=urllib.request.urlopen(url,timeout=120).read(); open(o,"wb").write(d)
    print(f"OK {o} {len(d)}")
if __name__=="__main__": gen(sys.argv[1],sys.argv[2],sys.argv[3])
