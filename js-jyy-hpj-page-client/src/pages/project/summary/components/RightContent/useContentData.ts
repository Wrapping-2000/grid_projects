/* 汇总右侧数据 */
import React from 'react';
import { getSummaryChartsData, getSummaryPieData } from '@/services/main';
import { summaryPieDataFormatter, summaryChartsDataFormatter } from '@/util/formatter';

type RightContentType =
  'loading'| // 加载中
  'not-checked'| // 未选择
  'no-data'| // 已选择-无数据
  'has-data' // 有数据
  // HPJ.SummaryShowType // 图表类型

export default ({
  params,
  chartsType
}: {
  params?: Record<string, any>;
  chartsType?: HPJ.SummaryChartList;
}) => {
  // 右侧 展示形式
  const [type, setType] = React.useState<RightContentType>('not-checked');

  // 均值分类
  const [averageClassification, setAverageClassification] = React.useState<HPJ.AverageClassification>('classification');

  // 选中的柱子
  const [selected, setSelected] = React.useState<Record<string, any>>();

  // 选中的区域
  const [selectedPieArea, setSelectedPieArea] = React.useState<Record<string, any>>();

  // 图表
  const [chartsData, setChartsData] = React.useState<Record<string, any>>();
console.log(chartsData, 'setChartsData');
  // 饼图数据
  const [pieData, setPieData] = React.useState<Record<string, any>>();

  // 获取数据
  const getData = React.useCallback((tParams) => {
    (async (p) => {
      const {
        value, averageClassification: averageClassificationParam, chartsType: cType
      } = p;

      const name = value?.type?.selectedKeys?.[0]

      const promises = (cType||[]).includes('pie') ? [
        getSummaryChartsData(averageClassificationParam, {name}),
        // 获取饼图
        getSummaryPieData({
          name,
          contrast_filed: undefined,
          contrast_value: undefined,
          target_year: undefined,
        })
      ] : [
        getSummaryChartsData(averageClassificationParam, {name})
      ];

      setType('loading');
      Promise.all(promises)
        .then(([chartsDataRes, pieDataRes]) => {
          if (chartsDataRes?.code === 'SUCCESS') {
            setChartsData(summaryChartsDataFormatter(chartsDataRes.data));
          }
          if (pieDataRes?.code === 'SUCCESS') {
            setPieData(summaryPieDataFormatter(pieDataRes.data));
          }
          const t = chartsDataRes?.code === 'SUCCESS' || pieDataRes?.code === 'SUCCESS' ? 'has-data' : 'no-data';
          setType(t);
        })
        .catch((error) => {
          console.error(error);
          setType('no-data');
        })
        .finally();
    })(tParams)
  }, []);

  // 选中值变化，修改展示类型并尝试请求数据
  React.useEffect(() => {
    // 有选中指标， 请求并根据有无数据设置type
    if (params) {
      setType('loading');
      getData({
        averageClassification,
        value: params,
        chartsType
      });
      return;
    }
    // 无选中指标， 设置type成未选择
    setType('not-checked');
  }, [averageClassification, params, chartsType, getData]);

  const onSelect = (v: HPJ.AverageClassification) => {
    setAverageClassification(v);
    // 请求饼图
    getData({
      averageClassification,
      value: params,
      chartsType
    });
  };

  // 选中值变化，重置下拉
  React.useEffect(() => {
    console.log(params)
    setAverageClassification('classification');
  }, [setAverageClassification, params]);

  // console.log(averageClassification, 'useContentData_averageClassification')
  // console.log(params, 'useContentData_params')
  // console.log(type, 'useContentData_type')
  console.log(chartsType, '图表类型');
  console.log(chartsData, '柱状、折线数据');
  console.log(pieData, '饼图数据');
  // console.log(selected, 'useContentData_selected')
  // console.log(selectedPieArea, 'useContentData_selectedPieArea')

  return {
    chartsData,
    pieData,
    type,
    averageClassification,
    setAverageClassification,
    onSelect,
    selected,
    setSelected,
    selectedPieArea,
    setSelectedPieArea
  }
}
