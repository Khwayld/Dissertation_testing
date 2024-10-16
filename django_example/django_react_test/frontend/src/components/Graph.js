// src/components/Graph.js
import React from 'react';
import { Scatter } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, Legend, Tooltip } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, Legend, Tooltip);

const Graph = ({ graphData }) => {
  const getScatterData = () => {
    if (!graphData) return null;

    const sourceData = graphData.source;
    const targetData = graphData.target;

    return {
      datasets: [
        {
          label: 'Source Positive',
          data: sourceData.x.map((xVal, index) => ({
            x: xVal,
            y: sourceData.y[index],
          })).filter((_, index) => sourceData.labels[index] === 1),
          borderColor: 'rgba(0, 255, 255, 0.7)', // Light cyan for positive
          pointStyle: 'circle',
        },
        {
          label: 'Source Negative',
          data: sourceData.x.map((xVal, index) => ({
            x: xVal,
            y: sourceData.y[index],
          })).filter((_, index) => sourceData.labels[index] === 0),
          borderColor: 'rgba(255, 99, 132, 0.7)', // Red for negative
          pointStyle: 'cross',
        },
        {
          label: 'Target Positive',
          data: targetData.x.map((xVal, index) => ({
            x: xVal,
            y: targetData.y[index],
          })).filter((_, index) => targetData.labels[index] === 1),
          borderColor: 'rgba(153, 102, 255, 0.7)', // Purple for positive
          pointStyle: 'circle',
        },
        {
          label: 'Target Negative',
          data: targetData.x.map((xVal, index) => ({
            x: xVal,
            y: targetData.y[index],
          })).filter((_, index) => targetData.labels[index] === 0),
          borderColor: 'rgba(255, 165, 0, 0.7)', // Orange for negative
          pointStyle: 'cross',
        },
      ],
    };
  };

  return (
    <div style={{ width: '100%', height: '300px' }}>
      <Scatter 
        data={getScatterData()} 
        options={{ 
          maintainAspectRatio: false,
          scales: { 
            x: { type: 'linear', beginAtZero: true }, 
            y: { type: 'linear', beginAtZero: true } 
          } 
        }} 
      />
    </div>
  );
};

export default Graph;
