from geoserver.support import ResourceInfo
from geoserver.catalog import Catalog


class Coverage(ResourceInfo):
    def __init__(self, catalog: Catalog, store_name, work_space):
        super().__init__()
        self.catalog = catalog
        self.store_name = store_name
        self.work_space = work_space
        self.gs_version = self.catalog.get_short_version()

    @property
    def href(self):
        return f"{self.catalog}/workspaces/{self.work_space}/coveragestores/{self.store_name}/coverages"
