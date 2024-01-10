import React from 'react';
import { MarkerType } from 'react-flow-renderer';


// This is an example node
export const nodes = [
  {
    id: '1',
    type: 'input',
    data: {
      label: (
        <>
          <strong>CIS*1300</strong>
        </>
      ),
    },
    position: { x: 250, y: 0 },
  },
  {
    id: '2',
    data: {
      label: (
        'CIS*2500'
      ),
    },
    position: { x: 100, y: 100 },
  },
  {
    id: '3',
    data: {
      label: (
        'CIS*1910'
      ),
    },
    position: { x: 400, y: 100 },
    style: {
      background: '#D6D5E6',
      color: '#333',
      border: '1px solid #222138',
      width: 180,
    },
  },
  {
    id: '4',
    position: { x: 250, y: 200 },
    data: {
      label: 'CIS*2430',
    },
  },
  {
    id: '5',
    data: {
      label: 'CIS*2750',
    },
    position: { x: 250, y: 325 },
  },
  {
    id: '6',
    type: 'output',
    data: {
      label: (
        'CIS*3750'
      ),
    },
    position: { x: 100, y: 480 },
  }
];

// This is example edges for the nodes
export const edges = [
  { id: 'e1-2', source: '1', target: '2', label: 'this is a mandatory prereq', markerEnd:{type: MarkerType.ArrowClosed} },
  { id: 'e1-3', source: '1', target: '3', markerEnd:{type: MarkerType.ArrowClosed}},
  {
    id: 'e3-4',
    source: '3',
    target: '4',
    animated: true,
    label: 'this is an optional prereq',
	markerEnd: {
		type: MarkerType.ArrowClosed,
	}
  },
  {
    id: 'e4-5',
    source: '4',
    target: '5',
    markerEnd: {
      type: MarkerType.ArrowClosed,
    },
  },
  {
    id: 'e5-6',
    source: '5',
    target: '6',
    type: 'step',
    style: { stroke: '#f6ab6c' },
  	markerEnd : { 
		type: MarkerType.ArrowClosed,
	}
  },
];

