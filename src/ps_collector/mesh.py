from __future__ import print_function

import requests
import json
from urlparse import urlparse


class Mesh:
    def __init__(self, base_url = "https://psconfig.opensciencegrid.org/pub/config"):
        self.base_url = base_url

    def get_nodes(self):
        """
        Get all the nodes we should collect statistics

        :returns list: List of nodes in the mesh
        """
        # Get the top level config, with list of URLs
        meshes = self._download_toplevel()
        nodes = set()
        for mesh_url in meshes:
            nodes.update(self._download_nodes(mesh_url))

        return nodes
    

    def _download_nodes(self, mesh_url):
        """
        Download the nodes from a single mesh
        """
        nodes = set()

        response = requests.get(mesh_url)
        response_json = response.json()

        for org in response_json.get('organizations', []):
            for site in org.get('sites', []):
                for host in site.get('hosts', []):
                    for url in host.get('measurement_archives', []):
                        parsed = urlparse(url['read_url'])
                        nodes.update([parsed.netloc])
        return nodes

    def _download_toplevel(self):
        """
        Download the list of URLs for the meshes
        """
        to_return = []
        response = requests.get(self.base_url)
        for sub_mesh in response.json():
            to_return.append(sub_mesh['include'][0])
        return to_return


if __name__ == "__main__":
    mesh = Mesh()
    print(mesh.get_nodes())


