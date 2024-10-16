import Plot from 'react-plotly.js';

function Graph({ graphData }) {
  const { xs, ys, xt, yt } = graphData;

  return (
    <Plot
      data={[
        {
          x: xs.map((item) => item[0]), // X values for source
          y: xs.map((item) => item[1]), // Y values for source
          mode: 'markers',
          type: 'scatter',
          marker: { color: 'cyan' },
          name: 'Source Domain'
        },
        {
          x: xt.map((item) => item[0]), // X values for target
          y: xt.map((item) => item[1]), // Y values for target
          mode: 'markers',
          type: 'scatter',
          marker: { color: 'purple' },
          name: 'Target Domain'
        }
      ]}
      layout={{ title: 'Source domain and target domain blobs data' }}
    />
  );
}

export default Graph;
