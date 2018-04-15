//Constants for the SVG
var width = 600,
    height = 600;

//Set up the colour scale
var color = d3.scale.category20();


//Set up the force layout
var force = d3.layout.force()
    .charge(-10)
    .linkDistance(10)
    .size([width, height]);

//Append a SVG to the graph of the html page. Assign this SVG as an object to svg
var svg = d3.select("#graph").append("svg")
    .attr("preserveAspectRatio", "xMinYMin meet")
    .attr("viewBox", `0 0 ${width} ${height}`)
    .classed("svg-content-responsive", true);
    
//Read the data from the graph_data element 
var graph_data = document.getElementById('graph_data').innerHTML;
graph = JSON.parse(graph_data);
graph["links"] = graph["links"].map(function(object) {
    return {
        source: Number(object.source),
        target: Number(object.target),
        value:  Number(object.value)
    };
});
console.log("JSON loaded!");

//Creates the graph data structure out of the json data
force.nodes(graph.nodes)
    .links(graph.links)
    .start();
console.log("Graph created!");

//Create all the line svgs but without locations yet
var link = svg.selectAll(".link")
    .data(graph.links)
    .enter().append("line")
    .attr("class", "link")
    .style("stroke-width", function (d) {
        return 4 * d.value;
    });
console.log("Links created!");

//Do the same with the circles for the nodes - no 
var node = svg.selectAll(".node")
    .data(graph.nodes)
    .enter().append("g")
    .attr("class", "node")
    .call(force.drag);
console.log("Nodes created!");

// Circle for nodes
node.append("circle")
    .attr("r", function(d) {
        return 8 * d.pubs + 2;
    })
    .style("fill", "black")
    .append("svg:title")
    .text(function(d) { return d.x; });
console.log("Circles created!");

//Now we are giving the SVGs co-ordinates - the force layout is generating the co-ordinates which this code is using to update the attributes of the SVG elements
force.on("tick", function () {
    link.attr("x1", function (d) {
        return d.source.x;
    })
        .attr("y1", function (d) {
        return d.source.y;
    })
        .attr("x2", function (d) {
        return d.target.x;
    })
        .attr("y2", function (d) {
        return d.target.y;
    });

    node.attr("transform", function(d) { 
        return 'translate(' + [d.x, d.y] + ')';
    });
});
console.log("Force!");
