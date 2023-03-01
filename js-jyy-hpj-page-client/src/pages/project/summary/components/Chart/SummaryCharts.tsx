import React from 'react';
import { Card, Tabs, Button, Select } from 'antd';
import type { SelectProps } from 'antd';
import Icon from '@ant-design/icons';
import { BaseChart, useChart } from '@/components/Charts';
import type { Props as BaseChartProps } from '@/components/Charts';
import { ReactComponent as IconBar} from '@/assets/icon_bar.svg';
import { ReactComponent as IconBarActive} from '@/assets/icon_bar_active.svg';
import { ReactComponent as IconLine} from '@/assets/icon_line.svg';
import { ReactComponent as IconLineActive} from '@/assets/icon_line_active.svg';
import withProps from '@/util/withProps';
import { summaryAverageClassificationSelectorOptions } from '@/util/constants';
import { getSummaryPieData } from '@/services/main';
import { summaryPieDataFormatter } from '@/util/formatter';
import { colors } from '@/util/constants';
import styles from '../../style.less';

const StyledSelect = withProps<SelectProps<any>>(Select, {style: {width: 150, marginRight: 26}});
const StyledBaseChart = withProps<BaseChartProps>(BaseChart, {
  defaultOptions: {
    color: colors,
    barMaxWidth: 40,
    grid: {
      left: '8%',
      right: '8%',
      bottom: 40,
    },
  },
  style: {width: '100%', height: 320}
});
const StyledPieChart = withProps<BaseChartProps>(BaseChart, {
  defaultOptions: {
    // emphasis: {
    //   itemStyle: {
    //     shadowBlur: 10,
    //     shadowOffsetX: 0,
    //     shadowColor: 'rgba(0, 0, 0, 0.5)'
    //   }
    // }
  },
  style: {width: '100%', height: 320, marginTop: 16}
});

const legend = {
  bottom: 0,
  itemWidth: 10,
  itemHeight: 8
}

// 柱状图选中样式
const barProps = {
  tooltip: {
    trigger: 'axis',
    // axisPointer: {
    //   type: 'shadow'
    // }
  },

  series: {
    // 选中样式
    selectedMode: 'single',
    select: {
      label: {
        show: true,
      },
      itemStyle: {
        borderWidth: 0,
        shadowColor: 'rgba(0, 0, 0, 0.65)',
        borderColor: 'transparent',
        shadowBlur: 10,
        shadowOffsetX: 1,
        opacity: 0.85
      },
      labelLine: {
        show: true,
        lineStyle: {
          color: 'red'
        }
      },
    },
    emphasis: {
      // focus: 'series',
      blurScope: 'coordinateSystem'
    },
  }
}

// 折线图选中样式
const lineProps = {
  series: {
    seriesLayoutBy: 'row',
    // 选中样式
    selectedMode: 'single',
    select: {
      label: {
        show: true,
        backgroundColor: '#000',
        padding: 8,
        paddingBottom: 6,
        color: '#fff',
        borderRadius: 2,
      },
      itemStyle: {
        borderWidth: 8,
      },
      labelLine: {
        show: true
      },
    },
    emphasis: {
      focus: 'series',
      blurScope: 'coordinateSystem'
    },
  }
}

// 连续值属性
const continuousProps = {
  grid: {
    left: '8%',
    right: '8%',
    bottom: 80,
  },
  dataZoom: {
    type: 'slider',
    bottom: 36,
    height: 24
  },
  legend
}

function SummaryCharts(props: {
  activeTreeData?: Record<string, any>; // 选中的树目录指标
  type: HPJ.SummaryChartType; // ?
  data: Record<string, any>; // 总数据，柱状、折线
  pieData: Record<string, any>; // 饼图数据
  secondaryData: any[], // 次级数据，点击柱状/折线后饼图或者table展示的数据
  thirdlyData: any[], // 三级数据，点击饼图部分块后table展示的数据
  title: string;
  chartsType?: HPJ.SummaryChartList;
  onSelect?: (value: HPJ.AverageClassification) => void;
  averageClassification: HPJ.AverageClassification; // 同类均值等指标
  selected?: Record<string, any>; // 选中的柱状、折线区域,
  setSelected: (v?: Record<string, any>) => void; // 选择柱状、折线区域
  selectedPieArea: Record<string, any>; // 选中的饼图区域
  setSelectedPieArea: (v?: Record<string, any>) => void; // 选择饼图区域
}) {
  const {
    data, pieData, activeTreeData, chartsType,
    onSelect, averageClassification,
    selected, setSelected, selectedPieArea, setSelectedPieArea
  } = props;

  const title = React.useMemo(() => {
    return `${activeTreeData?.type?.selectedKeys?.[0] || ''}指标均值`;
  }, [activeTreeData]);

  // 是否是连续值
  const isContinuousValues = React.useMemo(() => {
    return data?.isContinuousValues;
  }, [data]);

  // 图表实例句柄
  const {chart: chartBar} = useChart();
  const {chart: chartLine} = useChart();
  const {chart: chartPie} = useChart();

  // 柱状图、折线数据
  const mainData = React.useMemo(() => {
    return data?.data || []
  }, [data]);

  const dimensions = React.useMemo(() => {
    if (!isContinuousValues) {
      return;
    }
    let map: Record<string, any> = {};
    mainData.forEach((newMap: Record<string, any>) => {
      map = {...map, ...newMap||{}}
    });
    let r: string[] = [];
    if (map.year) {
      delete map.year;
      r = Object.keys(map)
      r.unshift('year');
    }
    return r;
  }, [mainData, isContinuousValues]);

  // 二级饼图数据(点击柱状图)
  const [secondaryPieData, setSecondaryPieData] = React.useState<Record<string, any>[]>();

  // 尝试获取二级饼图数据
  const try2getSecondaryPieData = React.useCallback((params) => {
    if (!chartPie.current) return;
    getSummaryPieData(params)
      .then(r => {
        if (r?.code === 'SUCCESS') {
          setSecondaryPieData(summaryPieDataFormatter(r?.data));
        }
      })
      .catch(console.error);
  }, [chartPie]);

  // 图表是否展示信息
  const chartsShowInfo = React.useMemo(() => {
    const safeCharts = chartsType || [];
    const showPie = safeCharts.includes('pie');
    const showLine = safeCharts.includes('line');
    const showBar= safeCharts.includes('bar');

    return {
      bar: {
        show: showBar,
        style: {
          width: showPie ? '61%' : '100%'
        },
      },
      line: {
        show: showLine,
        style: {
          width: showPie ? '61%' : '100%'
        },
      },
      pie: {
        show: showPie,
        style: {
          width: showBar||showLine ? 'calc(39% - 16px)' : '100%',
          marginLeft: showBar||showLine ? 16 : 0,
        }
      }
    }
  }, [chartsType]);

  // 当前选各种tab
  const [activeKey, setActiveKey] = React.useState('bar');

  // 图表
  const chartsBar = React.useMemo(() => {
    return (
      {
        ref: chartBar,
        options: {
          title: {
            text: title,
            left: '3%',
            // textStyle: {
            //   overflow: 'break'
            // }
          },
          series: isContinuousValues ? (dimensions||[]).slice(1).map(() => ({
            type: 'bar',
            ...barProps.series,
          })) : [{
            type: 'bar',
            ...barProps.series,
          }],
          dataset: {
            dimensions,
            source: mainData
          },
          xAxis: {
            type: 'category',
          },
          yAxis: {
            // type: 'value',
          },
          tooltip: barProps.tooltip,
          // 连续值额外属性
          ...(
            isContinuousValues ? continuousProps : {}
          ),
        }
      }
    )
  }, [mainData, chartBar, isContinuousValues, title, dimensions]);
  // 图表
  const chartsLine = React.useMemo(() => {
    return (
      {
        ref: chartLine,
        options: {
          title: {
            text: title,
            left: '3%',
          },
          series: isContinuousValues ? (dimensions||[]).slice(1).map(() => ({
            type: 'line',
            smooth: true,
            ...lineProps.series
          })) : [{
            type: 'line',
            smooth: true,
            ...lineProps.series
          }],
          dataset: {
            dimensions,
            source: mainData
          },
          xAxis: {
            type: 'category',
          },
          yAxis: {
            type: 'value',
          },
          // 连续值额外属性
          ...(
            isContinuousValues ? continuousProps : {}
          ),
        }
      }
  )
  }, [mainData, chartLine, isContinuousValues, title, dimensions]);

  // 图表
  const chartsPie = React.useMemo(() => (
    {
      ref: chartPie,
      options: {
        tooltip: {
          trigger: 'item',
        },
        legend,
        title: {
          text: '各区间指标值数量占比情况',
          left: 20,
        },
        series: [{
          type: 'pie',
          data: secondaryPieData || pieData, // 有二级数据就显示二级，否则显示一级数据
          radius: '55%',
          selectedMode: 'single',
          select: {
          }
        }],
      }
    }
  ), [secondaryPieData, pieData, chartPie]);

  // 当前柱状or折线图
  const currentChartRef = activeKey === 'bar' ? chartBar : chartLine;
  const currentChart = activeKey === 'bar' ? chartsBar : chartsLine;

  // 更新图表方法
  const updateChart = React.useCallback((chart: typeof chartBar, option: Record<string, any>) => {
    if (!chart || !chart.current) return;
    chart.current.clear();
    chart.current.resize();
    chart.current.setOption(option);
  }, []);

  // 更新柱状图、折线图数据
  React.useEffect(() => {
    updateChart(currentChart.ref, currentChart.options);
  }, [currentChart, updateChart, data]);

  // 更新饼图
  React.useEffect(() => {
    updateChart(chartsPie.ref, chartsPie.options);
  }, [chartsPie, updateChart, pieData, secondaryPieData]);

  // 取消饼图选中
  const unselectPie = React.useCallback((clearSelectedArea = true) => {
    if (!selectedPieArea) return;
    chartPie.current?.dispatchAction({
      type: 'unselect',
      seriesIndex: selectedPieArea?.seriesIndex,
      dataIndex: selectedPieArea?.dataIndex
    });
    if (clearSelectedArea) {
      setSelectedPieArea();
    }
  }, [chartPie, selectedPieArea, setSelectedPieArea]);

  // 取消柱状和折线选中
  const unselectBarLine = React.useCallback((clearSelected = true) => {
    if (!selected) return;
    currentChartRef.current?.dispatchAction({
      type: 'unselect',
      seriesIndex: selected?.seriesIndex,
      dataIndex: selected?.dataIndex
    });
    if (clearSelected) {
      setSelected();
    }
  }, [currentChartRef, selected, setSelected]);

  // 监听柱状图、折线图点击事件
  React.useEffect(() => {
    const clickHandler = (info: Record<string, any>) => {
      console.log(info,'info');
      // 记录这次的选中
      setSelected(info);

      // 取消原来选中的
      if (selected) {
        unselectBarLine(false);
      }

      // 选中的不是已选的，则选中当前点击的
      if (selected?.seriesIndex !== info?.seriesIndex || selected?.dataIndex !== info?.dataIndex) {
        currentChartRef.current?.dispatchAction({
          type: 'select',
          seriesIndex: info?.seriesIndex,
          dataIndex: info?.dataIndex
        })

        // 请求数据
        const key = isContinuousValues ? 'target_year' : 'contrast_value';
        if (activeTreeData && info?.name) {
          try2getSecondaryPieData({
            name: activeTreeData?.type.selectedKeys?.[0],
            contrast_filed: averageClassification,
            [key]: info?.name
          });
        }

      } else {
        // 选中时已选的 取消
        setSelected();
      }

      // 取消饼图的选中
      unselectPie();
    };

    [chartBar, chartLine].forEach((item) => {
      item?.current?.on('click', clickHandler);
      item?.current?.on('legendselectchanged', unselectBarLine);
    });

    return () => {
      [chartBar, chartLine].forEach((item) => {
        item?.current?.off('click', clickHandler)
        item?.current?.off('legendselectchanged', unselectBarLine);
      })
    }
  }, [chartBar, chartLine, currentChartRef, selected, unselectPie, unselectBarLine, averageClassification, activeTreeData, try2getSecondaryPieData, isContinuousValues, setSelected]);

  // 监听柱饼图点击事件
  React.useEffect(() => {
    const clickHandler = (info: Record<string, any>) => {
    console.log(info)
      // 记录这次的选中
      setSelectedPieArea(info);

      // 取消原来选中的
      if (selected) {
        unselectPie(false)
      }

      // 选中的不是已选的，则选中当前点击的
      if (selectedPieArea?.seriesIndex !== info?.seriesIndex || selectedPieArea?.dataIndex !== info?.dataIndex) {
        chartPie.current?.dispatchAction({
          type: 'select',
          seriesIndex: info?.seriesIndex,
          dataIndex: info?.dataIndex
        })
      } else {
        // 选中时已选的 取消
        setSelectedPieArea();
      }
    };

    chartPie?.current?.on('click', clickHandler);

    return () => {
      chartPie?.current?.off('click', clickHandler);
    }
  }, [chartPie, selectedPieArea, selected, unselectPie, setSelectedPieArea]);

  // 选中时，更改同类指标参数时，获取平涂数据
  const handleSelect = (v: HPJ.AverageClassification) => {
    if (onSelect) {
      onSelect(v);
    }

    // 设置空
    unselectPie();
    unselectBarLine(undefined);
    setSecondaryPieData(undefined);
  }

  return (
    <div className={styles.charts}>
      {
        // 是否展示柱状图、折线图的tab
        chartsShowInfo.bar.show || chartsShowInfo.line.show ? (
          <Card
            style={{height: 360, width: chartsShowInfo.pie.show ? '61%' : '100%', position: 'relative', marginBottom: 16}}
            bodyStyle={{padding: 8}}
          >
            <Tabs activeKey={activeKey}>
              <Tabs.TabPane key="bar" tab="bar">
                <StyledBaseChart chart={chartBar} />
              </Tabs.TabPane>
              <Tabs.TabPane key="line" tab="line">
                <StyledBaseChart chart={chartLine} />
              </Tabs.TabPane>
            </Tabs>
            <div className={styles['tabs-tools']}>
              <StyledSelect
                options={summaryAverageClassificationSelectorOptions || []}
                defaultValue={summaryAverageClassificationSelectorOptions?.[0]?.value}
                value={averageClassification}
                onSelect={handleSelect}
              />
              <Button type="link" onClick={() => setActiveKey('bar')}>
                <Icon component={activeKey === 'bar' ? IconBarActive : IconBar} />
              </Button>
              <Button type="link" onClick={() => setActiveKey('line')}>
                <Icon component={activeKey === 'line' ? IconLineActive : IconLine} size={32} />
              </Button>
            </div>
          </Card>
        ) : null
      }
      {
        chartsShowInfo.pie.show ? (
          <Card style={{height: 360, ...chartsShowInfo.pie.style}} bodyStyle={{padding: 8}}>
            <StyledPieChart chart={chartPie} />
          </Card>
        ) : null
      }
    </div>
  );
}

export default SummaryCharts;
