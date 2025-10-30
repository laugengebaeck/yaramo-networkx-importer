# yaramo-networkx-importer
This importer uses a [networkx](https://github.com/networkx/networkx) graph to create a corresponding topology with [yaramo](https://github.com/simulate-digital-rail/yaramo) objects.
The resulting topology only contains junctions and end nodes from the original graph, while intermediate nodes are only saved as geo nodes belonging to the respective topological edge.
Node coordinates are taken from the node IDs and must be Euclidean coordinates (i.e., a tuple of integers).
Other parts of the yaramo data model (e.g. signals) are not yet supported, but might be in the future.

## Setup
1. Create a virtual environment with `python3 -m venv .venv` (macOS/Linux) or `py -3 -m venv .venv`
2. Activate the virtual environment with `source .venv/bin/activate` (macOS/Linux) or `.venv\Scripts\activate.bat`
3. Run `poetry install`

## Usage
```` python
import networkx
from networkx_importer import NetworkxImporter

# graph must represent a railway station topology (nodes of degree 1 to 3), node IDs should be as given above
graph = networkx.Graph()
topology = NetworkxImporter(graph).run()
````
