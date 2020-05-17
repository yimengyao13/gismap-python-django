# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
import requests
# 接收get请求数据
def get(request):
    request.encoding = 'utf-8'
    if 'q' in request.GET and request.GET['q']:
        message = '你搜索的内容为: ' + request.GET['q']
    else:
        message = '你提交了空表单'
    return HttpResponse(message)
# 接收POST请求数据
def posthtml(request):
    ctx ={}
    if request.POST:
        ctx['rlt'] = request.POST['q']
    return render(request, "post.html", ctx)
# 渲染表单
def gethtml(request):
    return render(request, 'get.html')
# 获取wmts服务
def wmts(request):
    url='http://localhost:8080/geoserver/wms?SERVICE=WMS&VERSION=1.1.0&'+\
        'REQUEST=GetMap&FORMAT=image%2Fpng&TRANSPARENT=true&tiled=true&'+\
        'LAYERS='+request.GET['LAYERS']+'&exceptions=application%2Fvnd.ogc.se_inimage&singleTile=true&SRS=EPSG%3A4326&STYLES=&WIDTH='+\
        request.GET['WIDTH']+'&HEIGHT='+request.GET['HEIGHT']+'&BBOX='+request.GET['BBOX']
    print(url)
    image_data=requests.get(url=url,stream=True)
    return HttpResponse(image_data,content_type='image/png')
# 获取要素服务
def getfeature(request):
    url='http://localhost:8080/geoserver/wms?SERVICE=WMS&VERSION=1.1.1&REQUEST=GetFeatureInfo&FORMAT=image%2Fpng&'+\
        'TRANSPARENT=true&QUERY_LAYERS='+request.GET['QUERY_LAYERS']+'&LAYERS='+request.GET['LAYERS']+\
        '&exceptions=application%2Fvnd.ogc.se_inimage&INFO_FORMAT=application/json&FEATURE_COUNT=50&X=50&Y=50'+\
        '&SRS=EPSG%3A4326&STYLES=&WIDTH=101&HEIGHT=101&BBOX='+request.GET['BBOX']
    json_data=requests.get(url=url)
    return HttpResponse(json_data,content_type='application/json')
# 提交 gml到geoserver
def postgml(request):
    ctx ={}
    if request.POST:
        head = {"Content-Type": "text/xml; charset=UTF-8", "Connection": "close"}
        r = requests.post('http://localhost:8080/geoserver/wfs', data=request.POST['gml'], headers=head)
        ctx['rlt'] = r.text
    return render(request, "postgml.html", ctx)

# 渲染geoserver页面
def geoserverget(request):
    return render(request, 'GeoserverOL.HTML')

# 提交 gml到geoserver
def geoserverpost(request):
    if request.POST:
        head = {"Content-Type": "text/xml; charset=UTF-8", "Connection": "close"}
        r = requests.post('http://localhost:8080/geoserver/wfs', data=request.POST['gml'], headers=head)
    return HttpResponse(r.text)
