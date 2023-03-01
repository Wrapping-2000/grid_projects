//import React from 'react';
import SummaryCharts from '../Chart';
import Table from '../Table';
import styles from '../../style.less';

function RightContent(props: {
  activeTreeData?: Record<string, any>; // 选中的树目录指标
  type: string;
  chartsData: any;
  chartsType?: HPJ.SummaryChartList;
  setAverageClassification: (value: HPJ.AverageClassification) => void;
  averageClassification: HPJ.AverageClassification,
  setCurrentRow: (v: any) => void; // 设置当前行
  setShowDetail: (v: boolean) => void; // 设置抽屉显示
  [key: string]: any
}) {
  const {
    chartsData, pieData, type, chartsType, activeTreeData,
    averageClassification, setCurrentRow, setShowDetail,
    onSelect,
    selected, setSelected, selectedPieArea, setSelectedPieArea
  } = props;
  console.log(chartsData, 'chartsData')
  // 右侧展示区域
    // 未选择
    if (type === 'not-checked') {
      return <div className={styles['empty-text']}>请先在左侧指标列表中选择指标</div>
    }
    // 无数据
    if (type === 'no-data') {
      return <div className={styles['empty-text']}>无数据</div>
    }


  return (
      <>
      {/* <Spin spinning={type === 'loading'}> */}
        {/* 右上图表展示区 */}
        <SummaryCharts
          activeTreeData={activeTreeData}
          data={chartsData}
          pieData={pieData}
          averageClassification={averageClassification}
          chartsType={chartsType}
          onSelect={onSelect}
          selected={selected}
          setSelected={setSelected}
          selectedPieArea={selectedPieArea}
          setSelectedPieArea={setSelectedPieArea}
          />
        {/* 右下数据表格展示区 */}
        <Table
          isContinuousValues={chartsData?.isContinuousValues}
          activeTreeData={activeTreeData}
          averageClassification={averageClassification}
          chartsType={chartsType}
          setCurrentRow={setCurrentRow}
          setShowDetail={setShowDetail}
          selected={selected}
          selectedPieArea={selectedPieArea}
        />
      {/* </Spin> */}
        </>
    )
}

export default RightContent;
