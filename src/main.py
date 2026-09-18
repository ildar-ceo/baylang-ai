from workers import WorkerEntrypoint, Response

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        html = """<!DOCTYPE html>
        <body>
          <h1>Hello World</h1>
        </body>"""

        headers = {"content-type": "text/html;charset=UTF-8"}
        return Response(html, headers=headers)
