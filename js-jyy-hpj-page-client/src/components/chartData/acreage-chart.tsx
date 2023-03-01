/*
堆积面积图
*/
import React, { useState, forwardRef, useImperativeHandle } from 'react';
import { Typography } from 'antd';
import { BaseChart, useChart } from '../Charts';
import { colors } from '@/util/constants';
import { chartDown } from '@/util/common';

const { Paragraph } = Typography;
interface HistogramProps {
  dataValue: any;
  dataTime: any;
  axisX: any;
  type: string;
  chartType: string;
}

const AcreageChart = forwardRef((props: HistogramProps, ref): JSX.Element => {
  const { dataValue, dataTime, axisX, type, chartType } = props;
  const [editableStr, setEditableStr] = useState('未命名图表');
  const onChange = (value) => {
    setEditableStr(value || '未命名图表');
  };
  const { chart } = useChart();
  const energyChartData = {
    norm: {
      value: dataValue?.map((item) => ({
        ...item,
        resultList: item?.resultList?.filter((it) => it !== null && it !== undefined),
      })),
    },
    time: {
      value: dataTime?.map((item) => {
        if (item?.indicator === undefined) {
          return null;
        }
        return item;
      }),
    },
  };
  const data = energyChartData?.[type]?.value?.filter((it) => it !== null && it !== undefined);
  const downData = [
    ...dataValue?.map((item) => ({
      indicator: item?.indicator,
      region: item?.region,
      source: item?.source,
      resultList: item?.resultList?.filter((it) => it !== null && it !== undefined),
    })),
  ];
  const downChart = async () => {
    if (chartType === 'Accumulation') {
      chartDown(chart, downData, editableStr);
    }
  };
  useImperativeHandle(ref, () => ({
    downChart,
  }));

  /* 更新图表格数据 */
  React.useEffect(() => {
    if (!chart || !chart.current) return;
    chart.current.clear();
    chart.current.resize();
    chart.current.setOption({
      color: colors,
      title: {
        text: editableStr,
        textStyle: {
          //  color: 'rgba(255,255,255,0.85)',
        },
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow',
        },
        textStyle: {
          fontSize: 12,
        },
        confine: true,
      },
      grid: {
        top: '15%',
        left: '10%',
        right: '10%',
        bottom: 100,
        containLabel: true,
      },
      yAxis: {
        type: 'value',
        axisLabel: {
          textStyle: {
            //  color: 'rgba(255,255,255,0.65)',
          },
          show: true,
          interval: 'auto',
        },
        splitLine: {
          show: true,
          lineStyle: {
            type: [2, 2],
            dashOffset: 5,
            //  color: 'none',
          },
        },
        nameTextStyle: {
          align: 'left',
        },
      },
      legend: {
        data: data?.map((item) => {
          // if (type === 'norm') {
          //   const tu = item?.indicator && `${item?.indicator} - ${item?.region} - ${item?.source}`;
          //   return tu;
          // }
          return item?.indicator;
        }),
        bottom: 'bottom',
        itemWidth: 32,
        itemHeight: 16,
        textStyle: {
          //  color: 'rgba(255,255,255,0.65)',
        },
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: type === 'norm' ? axisX : axisX.map((item) => `${item.split('+')[0]}`),
        axisTick: {
          show: false,
        },
        axisLabel: {
          textStyle: {
            //  color: 'rgba(255,255,255,0.65)',
          },
        },
      },
      dataZoom: [
        {
          textStyle: {
            //  color: '#8392A5',
          },
          dataBackground: {
            areaStyle: {
              //  color: '#8392A5',
            },
            lineStyle: {
              opacity: 0.6,
              //  color: '#8392A5',
            },
          },
          brushSelect: true,
          moveHandleSize: 5,
          height: 20,
          bottom: 75,
          left: 35,
          right: 38,
        },
        {
          type: 'inside',
        },
      ],
      series: data?.map((d) => ({
        name: d?.indicator,
        data: d?.resultList?.map((dv) => dv?.value),
        type: 'line',
        stack: 'Total',
        areaStyle: {},
        emphasis: {
          focus: 'series',
        },
      })),
    });
  }, [chart, data]);

  return (
    <div className="charts-container" style={{ width: '100%' }}>
      <div className="title-container" style={{ paddingTop: 5 }}>
        <Paragraph editable={{ onChange }} style={{ width: 500 }} />
      </div>
      <BaseChart chart={chart} className="chart-type" style={{ height: 680, width: '100%' }} />
    </div>
  );
});

export default AcreageChart;
