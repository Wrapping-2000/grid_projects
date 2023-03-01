// 环形图
import React, { useState, forwardRef, useImperativeHandle } from 'react';
import { Typography } from 'antd';
import { colors } from '@/util/constants';
import { BaseChart, useChart } from '../Charts';
import { chartDown } from '@/util/common';

const { Paragraph } = Typography;
interface HistogramProps {
  dataValue: any;
  dataTime: any;
  axisX: any;
  type: string;
  chartType: string;
}

const doughnutChart = forwardRef((props: HistogramProps, ref): JSX.Element => {
  const { dataValue, dataTime, axisX, type, chartType } = props;
  const [editableStr, setEditableStr] = useState('未命名图表');
  const onChange = (value) => {
    setEditableStr(value || '未命名图表');
  };
  const { chart } = useChart();
  const energyChartData = {
    norm: {
      value: dataTime?.map((item) => {
        if (item?.indicator === undefined) {
          return null;
        }
        return item;
      }),
    },

    time: {
      value: dataValue?.map((item) => ({
        ...item,
        resultList: item?.resultList?.filter((it) => it !== null && it !== undefined),
      })),
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
    if (chartType === 'doughnut') {
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
          // color: 'rgba(255,255,255,0.85)',
        },
      },
      tooltip: {
        trigger: 'item',
      },
      grid: {
        top: '15%',
        left: '10%',
        right: '10%',
        bottom: 100,
        containLabel: true,
      },
      legend: {
        bottom: 'bottom',
        itemWidth: 32,
        itemHeight: 16,
        textStyle: {
          // color: 'rgba(255,255,255,0.65)',
        },
      },
      series: data?.map((d) => ({
        name: d.indicator,
        data: d?.resultList?.map((dv) => ({
          value: dv?.value,
          name: type === 'norm' ? `${dv.name.split('+')[0]}` : dv.time,
        })),
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          // borderColor: '#fff',
          borderWidth: 2,
        },
        label: {
          show: false,
          position: 'center',
        },
        emphasis: {
          label: {
            show: true,
            fontSize: '40',
            fontWeight: 'bold',
          },
        },
        labelLine: {
          show: false,
        },
      })),
    });
  }, [chart, data]);
  return (
    <div className="charts-container" style={{ width: '100%' }}>
      <div className="title-container" style={{ paddingTop: 5 }}>
        <Paragraph editable={{ onChange }} style={{ width: 500 }} />
      </div>
      <BaseChart chart={chart} style={{ height: 680, width: '100%' }} />
    </div>
  );
});
export default doughnutChart;
