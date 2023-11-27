"""Init and utils."""
from AccessControl import Unauthorized
from plone import api
from Products.Five import BrowserView


class PdbView(BrowserView):
    def __call__(self):
        if api.env.debug_mode():
            locals().update(
                {
                    "context": self.context,
                    "request": self.request,
                    "api": api,
                }
            )
            self.request.response.setHeader("Content-Type", "text/plain")
            self.request.response.write(b"Interactive session started")
            breakpoint()
            "Interactive session started"
        raise Unauthorized
