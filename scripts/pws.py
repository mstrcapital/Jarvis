#!/usr/bin/env python3
"""
Playwright API Request - 替代 curl 的 HTTP 客户端
支持: GET, POST, PUT, DELETE, PATCH
"""

from playwright.sync_api import sync_playwright, APIRequestContext

import json as json_lib

class PWS:
    """Playwright HTTP Client - 替代 curl"""
    
    def __init__(self, base_url: str = None, headers: dict = None, timeout: int = 30000):
        self.base_url = base_url
        self.default_headers = headers or {}
        self.timeout = timeout
        self.ctx: APIRequestContext = None
        
    def __enter__(self):
        self.p = sync_playwright().start()
        self.ctx = self.p.request.new_context(
            timeout=self.timeout
        )
        return self
        
    def __exit__(self, *args):
        self.p.stop()
        
    def _url(self, path: str) -> str:
        """构建完整 URL"""
        if self.base_url and not path.startswith('http'):
            return f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        return path
        
    def _prepare_data(self, data, json_data):
        """准备请求数据"""
        if json_data:
            return json_lib.dumps(json_data)
        return data
        
    def _prepare_headers(self, kwargs):
        """准备 headers"""
        h = {**self.default_headers}
        if kwargs.get("headers"):
            h.update(kwargs.pop("headers"))
        if kwargs.get("json"):
            h["Content-Type"] = h.get("Content-Type", "application/json")
        if h:
            kwargs["headers"] = h
        return kwargs
        
    def get(self, path: str, params: dict = None, headers: dict = None, **kwargs):
        """GET 请求"""
        return self._request("get", path, params=params, headers=headers, **kwargs)
        
    def post(self, path: str, data=None, json=None, headers: dict = None, **kwargs):
        """POST 请求"""
        kwargs = self._prepare_headers(kwargs)
        data = self._prepare_data(data, json)
        return self._request("post", path, data=data, headers=headers, **kwargs)
        
    def put(self, path: str, data=None, json=None, headers: dict = None, **kwargs):
        """PUT 请求"""
        kwargs = self._prepare_headers(kwargs)
        data = self._prepare_data(data, json)
        return self._request("put", path, data=data, headers=headers, **kwargs)
        
    def delete(self, path: str, headers: dict = None, **kwargs):
        """DELETE 请求"""
        return self._request("delete", path, headers=headers, **kwargs)
        
    def patch(self, path: str, data=None, json=None, headers: dict = None, **kwargs):
        """PATCH 请求"""
        kwargs = self._prepare_headers(kwargs)
        data = self._prepare_data(data, json)
        return self._request("patch", path, data=data, headers=headers, **kwargs)
        
    def _request(self, method: str, path: str, **kwargs):
        """发送请求"""
        func = getattr(self.ctx, method)
        url = self._url(path)
        return func(url, **kwargs)


# ============ 便捷函数 ============

def get(url: str, **kwargs):
    """GET 请求"""
    with PWS() as pws:
        resp = pws.get(url, **kwargs)
        return resp.json()

def post(url: str, **kwargs):
    """POST 请求"""
    with PWS() as pws:
        resp = pws.post(url, **kwargs)
        return resp.json()

def put(url: str, **kwargs):
    """PUT 请求"""
    with PWS() as pws:
        resp = pws.put(url, **kwargs)
        return resp.json()

def delete(url: str, **kwargs):
    """DELETE 请求"""
    with PWS() as pws:
        resp = pws.delete(url, **kwargs)
        return resp.json()


# ============ 示例 ============

if __name__ == "__main__":
    import json
    
    print("=" * 50)
    print("Playwright API Request 示例")
    print("=" * 50)
    
    # 示例 1: 基础 GET (类似 curl)
    print("\n[1] GET 请求...")
    with PWS() as pws:
        resp = pws.get("https://httpbin.org/get")
        print(f"    状态: {resp.status}")
        print(f"    内容: {resp.json().get('origin')}")
    
    # 示例 2: 带参数
    print("\n[2] GET 带参数...")
    with PWS() as pws:
        resp = pws.get("https://httpbin.org/get", params={"key": "value", "num": 123})
        print(f"    状态: {resp.status}")
        print(f"    参数: {resp.json().get('args')}")
    
    # 示例 3: POST JSON
    print("\n[3] POST JSON...")
    with PWS() as pws:
        resp = pws.post("https://httpbin.org/post", 
                       json={"name": "Jarvis", "role": "AI"})
        print(f"    状态: {resp.status}")
        print(f"    发送: {resp.json().get('json')}")
    
    # 示例 4: 带 Header
    print("\n[4] 带自定义 Header...")
    with PWS() as pws:
        resp = pws.get("https://httpbin.org/headers", 
                       headers={"X-Custom": "Hello", "Authorization": "Bearer token123"})
        print(f"    状态: {resp.status}")
        headers = resp.json().get("headers", {})
        print(f"    X-Custom: {headers.get('X-Custom')}")
    
    # 示例 5: 使用 baseURL
    print("\n[5] 使用 baseURL...")
    with PWS(base_url="https://httpbin.org") as pws:
        resp = pws.get("/get")
        print(f"    状态: {resp.status}")
        print(f"    OK: {resp.ok}")
    
    # 示例 6: 便捷函数
    print("\n[6] 便捷函数...")
    data = get("https://httpbin.org/ip")
    print(f"    IP: {data.get('origin')}")
    
    print("\n" + "=" * 50)
    print("✅ 完成!")
    print("=" * 50)
