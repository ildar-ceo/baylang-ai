import subprocess, json

class MCPClient:
    
    def __init__(self, path, args=[]):
        self.path = path
        self.args = args
        self.process = None
        self.request_id = 0
    
    
    def start_server(self):
        """Start MCP server with stdio"""
        
        try:
            self.process = subprocess.Popen(
                [self.path] + self.args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8"
            )
        except Exception as e:
            raise Exception("Ошибка подключения: " + str(e))
    
    
    def stop_server(self):
        if self.process and self.process.poll():
            self.process.terminate()
            self.process.wait()
    
    
    def connect(self):
        if not self.process or self.process and not self.process.poll():
            self.start_server()
            if not self.process:
                raise Exception("Connection error")
        
            self.initialize()
    
    
    def send_message(self, method_name, params):
        
        self.connect()
        
        self.request_id += 1
        
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params or {}
        }
        
        data = json.dumps(request)
        self.process.stdin.write(data)
        self.process.stdin.write("\n")
        
        response_text = self.process.stdout.readline()
        if not response_text:
            raise Exception("Response error")
        
        try:
            response = json.loads(response_text.strip())
            return response
        
        except Exception as e:
            raise Exception("Json parse error: " + str(e))
    
    
    def getVersion(self):
        return "2025-06-18"
    
    
    def initialize(self):
        return self.send_message("initialize", {
            "protocolVersion": self.getVersion(),
            "capabilities": {},
            "clientInfo": {
                "name": "BayLang AI",
                "version": "1.0.0",
            }
        })
    
    
    def list_tools(self):
        return self.send_message("tools/list")
    
    
    def execute(self, name, params):
        return self.send_message("tools/call", {
            "name": name,
            "arguments": params,
        })
