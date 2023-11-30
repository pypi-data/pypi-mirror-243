"""Defines the API object; xcube convention."""

from xcube.server.api import Api

from xcube_4d_viewer.context import FourDContext

api = Api("4d-viewer",
          create_ctx=FourDContext,
          required_apis=["datasets"],
          description="4D Viewer by Earthwave")
