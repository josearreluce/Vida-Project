/* graph.js
 * Basic d3 graph visualization for the flask UI. Creates a basic graph
 * representation based on graph defined in static/js/test.json
 */
const color = d3.rgb('#5051DB');
const graph_box_dims = d3.select('.graph-box').node().getBoundingClientRect();
const height = graph_box_dims.height;
const width = graph_box_dims.width;
const svg = d3.select('.graph-svg');

// An offset value for determining node placement in the graph
const dist_offset = Math.sqrt((height * width)) / 10;

const simulation = d3.forceSimulation()
    .force('link', d3.forceLink().id(function (d) {
        return d.id;
    }).distance(dist_offset - 10).strength(0.5))
    .force('charge', d3.forceManyBody())
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('collision', d3.forceCollide().radius(dist_offset));

d3.json('static/js/test.json', function (error, graph) {
    if (error) throw error;
    create_ui_graph(graph.links, graph.nodes);
});

function create_ui_graph(links, nodes) {
    link = svg.selectAll('.link')
        .data(links)
        .enter()
        .append('line')
        .attr('class', 'link')
        .attr('stroke', color)
        .attr('stroke-width', '4');

    link.append('title')
        .text((d) => d.type);

    edgepaths = svg.selectAll('.edgepath')
        .data(links)
        .enter()
        .append('path')
        .attrs({
            'class': 'edgepath',
            'id': (d, i) => 'edgepath' + i
        })
        .style('pointer-events', 'none');

    edgelabels = svg.selectAll('.edgelabel')
        .data(links)
        .enter()
        .append('text')
        .attrs({
            'class': 'edgelabel',
            'id': (d, i) => 'edgelabel' + i,
        });

    node = svg.selectAll('.node')
        .data(nodes)
        .enter()
        .append('g')
        .attr('class', 'node');

    // Draw 'Node'
    node.append('circle')
        .attr('r', 18)
        .style('fill', color);

    node.append('title')
        .text((d) => d.id);

    simulation
        .nodes(nodes)
        .on('tick', redraw);

    // Draw 'edge' between nodes with a force
    simulation.force('link')
        .links(links);
}

function redraw() {
    link
        .attr('x1', (d) => d.source.x)
        .attr('y1', (d) => d.source.y)
        .attr('x2', (d) => d.target.x)
        .attr('y2', (d) => d.target.y);

    node
        .attr('transform', (d) => 'translate(' + d.x + ', ' + d.y + ')');
}
