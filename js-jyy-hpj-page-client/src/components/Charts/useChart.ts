import React from 'react';
import * as echarts from 'echarts';

export default () => {
  const chart = React.useRef<echarts.ECharts>();
  return {
    chart
  };
};
