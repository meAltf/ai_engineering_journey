## Two important properties:
    - Filters
    - HNSW (hierarchical Navigable small world)

## HSNW : 
    - The main intution of HNSW is- start search only when reach as close as possible.
    - It is a graph-based approximate nearest neighbor (ANN) index.
    - It finds similar vectors by navigating a multi-layer graph instead of scanning everything
    - Result: fast but approximate search

## Filters
    - EX: category- vacation, is_active- true
    - must [ fetch only if category is vacation and is_active true ] | "AND" operator
    - must_not [ if we wrote category-vacation i.e fetch only which doesn't belongs to category vacation] | "NOT" operator
    - should [ if any one have falls under then fetch that data] | "OR" operator
