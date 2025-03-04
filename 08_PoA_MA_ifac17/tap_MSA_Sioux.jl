using Graphs

function create_graph(start_node, end_node)
    @assert Base.length(start_node)==Base.length(end_node)

    no_node = max(maximum(start_node), maximum(end_node))
    no_arc = Base.length(start_node)

    graph = simple_inclist(no_node)
    for i=1:no_arc
        add_edge!(graph, start_node[i], end_node[i])
    end
    return graph
end

function get_vector(state, origin, destination, link_dic)
    current = destination
    parent = -1
    x = zeros(Int, maximum(link_dic))

    while parent != origin
        parent = state.parents[current]
        link_idx = link_dic[parent,current]
        if link_idx != 0
            x[link_idx] = 1
        end
        current = parent
    end
    return x
end

# preparing a graph
graph = create_graph(start_node, end_node)
link_dic = sparse(start_node, end_node, 1:numLinks)

function BPR(flowVec, fcoeffs)
    bpr = similar(flowVec)
    for a = 1:length(bpr)
        bpr[a] = free_flow_time[a] * sum([fcoeffs[i] * (flowVec[a]/capacity[a])^(i-1) for i = 1:length(fcoeffs)])
    end
    return bpr
end

function all_or_nothing(travel_time, demands)
    state = []
    path = []
    x = zeros(size(start_node))

    for r=1:numNodes
        # for each origin node r, find shortest paths to all destination nodes
        state = dijkstra_shortest_paths(graph, travel_time, r)

        for s=1:numNodes
            # for each destination node s, find the shortest-path vector
            # load travel demand
            x = x + demands[(r,s)] * get_vector(state, r, s, link_dic)
        end
    end

    return x
end

function tapMSA(demands, fcoeffs, numIter=500, tol=1e-6)
    # Finding a starting feasible solution
    travel_time = BPR(zeros(numLinks), fcoeffs)
    xl = all_or_nothing(travel_time, demands)

    l = 1

    while l < numIter
        l += 1

        xl_old = xl

        # Finding yl
        travel_time = BPR(xl, fcoeffs)

        yl = all_or_nothing(travel_time, demands)

        assert(yl != xl)

        xl = xl + (yl - xl)/l

        xl_new = xl

        relative_gap = norm(xl_new - xl_old, 1) / norm(xl_new, 1)

        if relative_gap < tol 
            break
        end

    end

    tapFlows = Dict{(Int64,Int64),Float64}()

    for i = 1:length(ta_data.start_node)
        key = (ta_data.start_node[i], ta_data.end_node[i])
        tapFlows[key] = xl[i]
    end
    
    tapFlowVect = xl

    return tapFlows, tapFlowVect
end
