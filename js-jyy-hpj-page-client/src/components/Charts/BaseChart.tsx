import React from 'react';
import type { CSSProperties } from 'react';
import * as echarts from 'echarts';
import cls from 'classnames';
// import useWindowSize from '../../utils/hooks/use-window-size';

export interface Props {
  chart?: React.MutableRefObject<any>;
  className?: string;
  style?: CSSProperties;
  defaultOptions?: echarts.EChartsOption;
}

function BasicChart(props: Props): JSX.Element {
  const {
    className, style, chart, defaultOptions
  } = props;
  const chartContainer = React.useRef<HTMLDivElement>();
  const selfChart = React.useRef<HTMLDivElement>();
  const finalChart = chart || selfChart;

  React.useEffect(() => {
    if (chartContainer.current) {
      finalChart.current = echarts.init(chartContainer.current, defaultOptions);
    }
    return () => {
      finalChart.current.dispose()
    }
  }, []);

  /* 监听窗口大小改变 */
  // useWindowSize(() => finalChart.current?.resize());

  return <div className={cls('component-chart', className)} style={{height: '300px', ...style}} ref={chartContainer as {current: HTMLDivElement}} />;
}
BasicChart.defaultProps = {
  chart: undefined,
  className: undefined,
  style: undefined,
  defaultOptions: {},
};

export default BasicChart;
