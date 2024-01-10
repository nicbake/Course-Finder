import * as React from 'react'
import Stack from 'react-bootstrap/Stack'
import Button from 'react-bootstrap/Button'
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  ReactFlowProvider,
} from 'react-flow-renderer'
import Navbar from "./navbar"
import dagre from 'dagre';

const row = {
  display: 'flex'
}

const column = {
  float: 'left'
}

const left = {
  width: '15%',
  background: '#EEEEEE'
}

const right = {
  width: '85%'
}

const dagreGraph = new dagre.graphlib.Graph();
dagreGraph.setDefaultEdgeLabel(() => ({}));
const nodeWidth = 172;
const nodeHeight = 36;

const Graph = () => {

  // This is a work in progress for cascading
  const onNodeClick = (event, clickNode) => {
    event.preventDefault();
    if (nodes === []) return;

    if (Program === '' || University === '') return;
    const queryString = '/api/graph?type=program'
      + '&school=' + University.toString()
      + '&programName=' + Program.toString().replaceAll('&', '')
      + '&majorName=';

    const searchRequest = new Request(queryString, {
      method: 'GET',
      headers: queryHeaders,
    });
    // This is the call to the api for the graph info
    fetch(searchRequest)
      .then(response => response.json())
      .then(results => {
        let coloredNodes = recursion(results['nodes'], edges, clickNode.id, 'white');
        const { nodes: layoutedNodes, edges: layoutedEdges } = setLayoutedElements(
          coloredNodes,
          results['edges']
        );
        // Set the nodes and the edges of the graph
        setNodes(layoutedNodes);
        setEdges(layoutedEdges);
      })

    return;
  }

  const recursion = (nodes, edges, id, color) => {
    let j = 0;
    // Get the number of the node id and store it in j
    for (j; nodes[j].id !== id; j++);
    nodes[j].style = { ...nodes[j].style, background: color };

    // Find the source node and its corresponding target nodes and changes their colors
    for (let i = 0; i < edges.length; i++) {
      if (edges[i].source === id) {
        for (j = 0; nodes[j].id !== edges[i].target; j++);
        if (edges[i].animated) {
          nodes = recursion(nodes, edges, nodes[j].id, '#d3d3d3');
        }
        else {
          nodes = recursion(nodes, edges, nodes[j].id, 'grey');
        }
      }
    }
    return nodes;
  };

  // This will get the layout of the graph
  const setLayoutedElements = (nodes, edges) => {
    dagreGraph.setGraph({ rankdir: 'LR' });

    nodes.forEach((node) => {
      dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight });
    });

    edges.forEach((edge) => {
      dagreGraph.setEdge(edge.source, edge.target);
    });

    dagre.layout(dagreGraph);

    nodes.forEach((node) => {
      const nodeWithPosition = dagreGraph.node(node.id);
      node.targetPosition = 'left';
      node.sourcePosition = 'right';

      // We are shifting the dagre node position (anchor=center center) to the top left
      // so it matches the React Flow node anchor point (top left).
      node.position = {
        x: nodeWithPosition.x - nodeWidth / 2,
        y: nodeWithPosition.y - nodeHeight / 2,
      };
      return node;
    });
    return { nodes, edges };
  };

  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  // Query Headers
  const queryHeaders = { 'Accept': 'application/json', 'Content-Type': 'application/json' }

  const [University, setUniversity] = React.useState('');
  const [Program, setProgram] = React.useState('');

  // Depending on university onchange event, populate the programs table
  const changeUniversity = (event) => {
    event.preventDefault();

    let university = event.target.value;
    if (university === "University of Guelph") {
      university = "uog";
    }
    if (university === "McGill University") {
      university = "mcg";
    }

    if (university === University) return;
    //if (university === "McGill University" && University == 'mcg') return;

    setProgram("");

    //Set the university
    setUniversity(university);

    //Clear the programs and credits drop down
    let programs = document.getElementById('ProgramSelector')
    for (let i = programs.options.length - 1; i > 0; i--)
      programs.remove(i);

    if (university === "") return;

    // Create query string with method and headers
    // Parameters are school
    const queryString = '/api/search/university?school=' + university;
    const searchRequest = new Request(queryString, {
      method: 'GET',
      headers: queryHeaders,
    });
    // Fetch request to api/search which deals with using the parameters to use program to search
    fetch(searchRequest)
      .then(response => response.json())
      .then(results => {
        for (const prog in results) {
          programs.options[programs.options.length] = new Option(results[prog], results[prog]);
        }
      })
    // Dynamic change of Credits based on University
  };
  // This is the get call to the api to get the information to put into the graph
  const generateGraph = (e) => {
    e.preventDefault();

    if (Program === '' || University === '') return;
    const queryString = '/api/graph?type=program'
      + '&school=' + University.toString()
      + '&programName=' + Program.toString().replaceAll('&', '')
      + '&majorName=';

    const searchRequest = new Request(queryString, {
      method: 'GET',
      headers: queryHeaders,
    });
    // This is the call to the api for the graph info
    fetch(searchRequest)
      .then(response => response.json())
      .then(results => {
        const { nodes: layoutedNodes, edges: layoutedEdges } = setLayoutedElements(
          results['nodes'],
          results['edges']
        );
        // Set the nodes and the edges of the graph
        setNodes(layoutedNodes);
        setEdges(layoutedEdges);
      })
    return;
  }

  const schools = [
    "University of Guelph",
    "McGill University",
  ];
  return (
    <div>
      {Navbar('/programGraph')}
      <div style={row}>

        <div style={column && left}>
          <Stack gap={3}>
            <h1 className="text-center">Program Graph Generator</h1>
            <div className="input-group mb-3">
              <select className="form-select" id="SchoolSelector" title="School" onChange={changeUniversity}>
                <option value=''>School</option>
                {schools.map((school) => (<option key={school}>{school}</option>))}
              </select>
            </div>
            <div className="input-group mb-3">
              <select className="form-select" id="ProgramSelector" title="Program" onChange={(e) => setProgram(e.currentTarget.value)}>
                <option value=''>Programs</option>
              </select>
            </div>
            <div className="text-center d-grid">
              <Button variant="info" type="submit" onClick={generateGraph}>Create Graph</Button>{' '}
            </div>
          </Stack>
          <div class="legend-div">
            <h3 className="text-center">Legend</h3>
            <ul class="legend">
              <li><span class="superawesome"></span>First Year Course</li>
              <li><span class="awesome"></span>Second Year Course</li>
              <li><span class="kindaawesome"></span>Third Year Course</li>
              <li><span class="notawesome"></span>Fourth Year Course</li>
              <li>┅Mandatory Course</li>
              <li>━Optional Course (OR, 1 OF)</li>
            </ul>
          </div>
        </div>
        <div style={column && right} className="layoutFlow">
          <ReactFlowProvider>
            <ReactFlow
              nodes={nodes}
              edges={edges}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              onNodeClick={onNodeClick}
              connectionLineType="smoothstep"
              style={{ width: '100%', height: 'calc(100vh - 86px)' }}
              fitView
            >
              <MiniMap
                nodeStrokeColor={(n) => {
                  if (n.style?.background) return n.style.background;
                  if (n.type === 'input') return '#0041d0';
                  if (n.type === 'output') return '#ff0072';
                  if (n.type === 'default') return '#1a192b';
                  return '#eee';
                }}
                nodeColor={(n) => {
                  if (n.style?.background) return n.style.background;
                  return '#fff';
                }}
                nodeBorderRadius={2}
              />
              <Controls />
              <Background color="#aaa" gap={16} />
            </ReactFlow>
          </ReactFlowProvider>
        </div>
      </div>
    </div>
  );
};

export default Graph;
