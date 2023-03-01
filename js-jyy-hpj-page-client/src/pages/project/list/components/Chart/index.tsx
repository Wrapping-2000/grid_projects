import React from 'react';
import { Modal } from 'antd';
import * as echarts from 'echarts';
import { BaseChart, useChart } from '@/components/Charts';
import { colors } from '@/util/constants';

const defaultOptions: echarts.EChartsOption = {
  color: colors,
  xAxis: {
    type: 'category',
    axisTick: {
      show: false
    },
  },
  yAxis: {
    type: 'value',
    splitLine: {
      lineStyle: {
        type: 'dashed',
        dashOffset: 10
      }
    }
  },
  series: [
    {
      data: [],
      type: 'line',
      smooth: true
    }, {
      data: [],
      type: 'line',
      smooth: true
    }
  ],
  legend: {
    bottom: 0
  },
  dataZoom: [
    {
      textStyle: {
      color: '#8392A5',
    },
    dataBackground: {
      areaStyle: {
        color: '#8392A5',
      },
      lineStyle: {
        opacity: 0.6,
        color: '#8392A5',
      },
    },
    brushSelect: true,
    moveHandleSize: 5,
    bottom: 36
  },
  ],
  grid:{
    top: 24,
    bottom: 100,
      // containLabel: true
  },
};

function ChartModal(props: {
  record?: Record<string, any>;
  visible?: boolean;
  onCancel: () => void;
  averageName: string
}) {
  const {record, visible, onCancel, averageName} = props;
  const {average_list, value_list} = record || {};
  const { chart } = useChart();
  const {name, component_name} = props.record || {};
  const title = [name, component_name].reduce((prev, next) => `${prev}${(prev && next) ? '-' : ''}${next || ''}`, '');

  React.useEffect(() => {
    const xAxisData = [...(average_list||[]), ...(value_list||[])]
      .map((l: Record<string, string>) => l?.year);

    const xAxisDataSet = new Set(xAxisData);
    const uniqueXAxisData = Array.from(xAxisDataSet).sort();
    const series =
      [value_list, average_list]
        .map((list, index) => {
          const data = new Array(uniqueXAxisData.length).fill(undefined);
          (list || []).forEach((l: Record<string, string>) => {
            if (!l) {
              return;
            }
            const i = uniqueXAxisData.indexOf(l.year); // 查找数据所在的索引位置
            if (index >= 0) {
              data[i] = l.value
            }
          });
          return {
            name: index ? averageName : title,
            data,
            type: 'line',
            smooth: true
          }
        });

    // console.log(series, 'series')
    // console.log(xAxisData, 'xAxisData')
    // console.log(uniqueXAxisData, 'uniqueXAxisData')

    chart.current?.setOption({
      series,
      xAxis: {
        data: uniqueXAxisData
      },
      yAxis: {
        type: 'value'
      },
      legend: {
        bottom: 0
      },
      dataZoom: [
        {
          textStyle: {
          color: '#8392A5',
        },
        dataBackground: {
          areaStyle: {
            color: '#8392A5',
          },
          lineStyle: {
            opacity: 0.6,
            color: '#8392A5',
          },
        },
        brushSelect: true,
        moveHandleSize: 5,
        bottom: 36
      },
      ],
    });
  }, [average_list, value_list, chart, averageName, title]);

  return (
    <Modal
      centered
      title="指标趋势图"
      visible={visible}
      onCancel={onCancel}
      footer={null}
      zIndex={1001}
      width={740}
    >
      <BaseChart chart={chart} defaultOptions={defaultOptions} style={{width: 690, height: 400}} />
    </Modal>
  );
}

export default ChartModal;
