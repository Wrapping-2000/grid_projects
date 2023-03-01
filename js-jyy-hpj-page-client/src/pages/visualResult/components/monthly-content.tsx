import React, { useState, useEffect, useRef, forwardRef, useImperativeHandle } from 'react';
import { Table, Checkbox, Tabs } from 'antd';
import cls from 'classnames';
// import {httpIndicatorModal} from '../../../service/http_request';
import { tableHanded, dataFormatter, chooseDataFormatter } from '../../../util/common';
import HistogramIcon from '../../../assets/icon/histogram.svg';
import LineIcon from '@/assets/icon/lineChart.svg';
import ModalComponent from './modal';
import AccumulationIcon from '@/assets/icon/accumulation.svg';
import Remind from '@/assets/icon/remind.svg';
import PieIcon from '@/assets/icon/pie.svg';
import DoughnutIcon from '@/assets/icon/doughnut.svg';
import {
  HistogramChart,
  AcreageChart,
  LineChart,
  PieChart,
  DoughnutChart,
} from '../../../components/chartData';
import styles from '../visualResult.less';

interface typeProps {
  id: string;
  name: string;
}
interface InsideProps {
  dataTable: any;
  type: typeProps;
  dateType: string;
}

const { TabPane } = Tabs;

const ChartResult = forwardRef((props: InsideProps, ref): JSX.Element => {
  const { dataTable, type, dateType } = props;
  console.log(dataTable, type, dateType);
  const histogramRef = useRef<any>(null);
  const lineChartRef = useRef<any>(null);
  const AccumulationRef = useRef<any>(null);
  const pieChartRef = useRef<any>(null);
  const doughnutRef = useRef<any>(null);
  // 弹窗
  const [visible, setVisible] = useState(false);
  // const [indicatorDetail, setIndicatorDetail] = useState({});
  // // 表格总数据
  console.log(dataTable);
  const monthData = dataTable[0].indicatorDataVoList;
  // 图表类型
  const [chartType, setChartType] = useState<string>('histogram');
  /* 选中行数据 */
  const [selectedRows, setSelectedRows] = useState();
  // 图表全部数据
  const chartAll = [...monthData];
  console.log(chartAll);
  // 数据处理checkX为列，checkY为行，过滤选中数据
  const chartAllChange = (checkX: any, checkY: any) =>
    chartAll.map((item) => {
      const nameValue = `${item.indicator}+${item.database}+${item.type}`;
      if (checkX.includes(nameValue)) {
        return {
          ...item,
          resultList: item?.resultList.map((it: any) => {
            if (checkY.includes(it.time)) {
              return it;
            }
            return null;
          }),
        };
      }
      return null;
    });
  // 点击下载
  const onClickDown = () => {
    histogramRef.current?.downChart();
    lineChartRef.current?.downChart();
    AccumulationRef.current?.downChart();
    pieChartRef.current?.downChart();
    doughnutRef.current?.downChart();
  };
  // 方法传递给父组件
  useImperativeHandle(ref, () => ({
    onClickDown,
  }));
  // 获取表头
  const headData = tableHanded(dataTable);
  // 选中前几个
  const headCheck = (count: any) => [
    ...headData?.map((item: any, index: number) => ({
      name: item,
      check: index < count,
    })),
  ];

  // 表头多选框处理
  const chartAllHeadData = headCheck(5);
  // 初始化默认table行，如果超过5个默认选中前5个，不超过5个全部选中
  const defaultRow =
    monthData[0]?.resultList.map((item: any) => item.time).length <= 5
      ? monthData[0]?.resultList.map((item: any) => item.time)
      : monthData[0]?.resultList.map((item: any) => item.time).slice(0, 5);

  /* 选中行数据key */
  const [selectedRowKeys, setSelectedRowKeys] = useState(defaultRow);
  // 默认table列，如果超过5个默认选中前5个，不超过5个全部选中
  const defaultKey =
    chartAllHeadData?.map((item) => item.name).length <= 5
      ? chartAllHeadData?.map((item) => item.name)
      : chartAllHeadData?.map((item) => item.name).slice(0, 5);

  // 初始化图表
  const [columnsHead, setColumnsHead] = useState(chartAllChange(defaultKey, selectedRowKeys));
  // 初始化表头选中
  const [chartHeadData, setChartHeadData] = useState(chartAllHeadData);

  // 列表头是否选中
  const selectedHeadColumnKeys = React.useMemo(() => {
    if (!chartHeadData) return [];
    return chartHeadData?.map((c) => c?.check);
  }, [chartHeadData]);

  // table行时间排序
  const timeSort = monthData[0]?.resultList
    ?.map((item: any) => item.time)
    ?.map((item: any) => {
      if (selectedRowKeys.includes(item)) {
        return item;
      }
      return null;
    })
    ?.filter((item: any) => item !== null);

  // table时间类型数据处理
  const columnsHeadTable = [
    {
      period: dateType,
      indicatorDataVoList: columnsHead,
    },
  ];
  console.log(columnsHeadTable);
  const timeLists = chooseDataFormatter(columnsHeadTable);

  // 图表axisX数据
  const chartHeadDataList = [...chartHeadData];
  const newChartHead = chartHeadDataList
    .map((item) => {
      if (item.check) {
        return item.name;
      }
      return null;
    })
    .filter((item) => item !== null);

  const columnsAll = type?.id === 'norm' ? timeSort : newChartHead;

  console.log(columnsHead, timeLists, chartType, columnsAll, type?.id);
  // 图表
  const chartData = [
    {
      name: '柱状图',
      component: (
        <HistogramChart
          ref={histogramRef}
          dataValue={columnsHead}
          dataTime={timeLists}
          chartType={chartType}
          axisX={columnsAll}
          type={type?.id}
        />
      ),
      id: 'histogram',
      icon: <img src={HistogramIcon} style={{ width: 100, height: 80 }} />,
    },
    {
      name: '折线图',
      component: (
        <LineChart
          ref={lineChartRef}
          dataValue={columnsHead}
          chartType={chartType}
          dataTime={timeLists}
          axisX={columnsAll}
          type={type?.id}
        />
      ),
      id: 'lineChart',
      icon: <img src={LineIcon} style={{ width: 100, height: 80 }} />,
    },
    {
      name: ' 堆积面积图',
      component: (
        <AcreageChart
          ref={AccumulationRef}
          dataValue={columnsHead}
          chartType={chartType}
          dataTime={timeLists}
          axisX={columnsAll}
          type={type?.id}
        />
      ),
      id: 'Accumulation',
      icon: <img src={AccumulationIcon} style={{ width: 100, height: 80 }} />,
    },
    {
      name: '饼状图',
      component: (
        <PieChart
          ref={pieChartRef}
          dataValue={columnsHead}
          chartType={chartType}
          dataTime={timeLists}
          axisX={columnsAll}
          type={type?.id}
        />
      ),
      id: 'pieChart',
      icon: <img src={PieIcon} style={{ width: 100, height: 80 }} />,
    },
    {
      name: ' 环形图',
      component: (
        <DoughnutChart
          ref={doughnutRef}
          dataValue={columnsHead}
          chartType={chartType}
          dataTime={timeLists}
          axisX={columnsAll}
          type={type?.id}
        />
      ),
      id: 'doughnut',
      icon: <img src={DoughnutIcon} style={{ width: 100, height: 80 }} />,
    },
  ];

  // 前三种图表
  const valueRow = defaultRow;
  const MultiColumn = chartAllChange(defaultKey, defaultRow);
  // 饼图
  const valueOneRow = type.id === 'norm' ? defaultRow.slice(0, 1) : defaultRow;
  const oneColumn = chartAllChange(
    type.id === 'norm' ? defaultKey : defaultKey.slice(0, 1),
    type.id === 'norm' ? defaultRow.slice(0, 1) : defaultRow,
  );
  const energyChartData = {
    histogram: {
      valueData: MultiColumn,
      valueRow,
    },
    lineChart: {
      valueData: MultiColumn,
      valueRow,
    },
    Accumulation: {
      valueData: MultiColumn,
      valueRow,
    },
    pieChart: {
      valueData: oneColumn,
      valueRow: valueOneRow,
    },
    doughnut: {
      valueData: oneColumn,
      valueRow: valueOneRow,
    },
  };
  // 指标时间切换
  useEffect(() => {
    if (chartType === 'pieChart' || chartType === 'doughnut') {
      if (type.id === 'norm') {
        setColumnsHead(energyChartData?.[chartType]?.valueData);
        setSelectedRowKeys(energyChartData?.[chartType]?.valueRow);
        setChartHeadData(headCheck(5));
      } else {
        setSelectedRowKeys(defaultRow);
        setColumnsHead(
          chartAllChange(type.id === 'norm' ? defaultKey : defaultKey.slice(0, 1), defaultRow),
        );
        setChartHeadData(headCheck(1));
      }
    }
  }, [type]);

  // table行多选
  const onSelectChange = (selectedRowKey: React.SetStateAction<unknown[]>, selectedRow: any) => {
    const pitchCheck = chartHeadData
      ?.filter((item) => item.check === true)
      .map((item) => item.name);
    const selectedRowLists =
      (chartType === 'pieChart' || chartType === 'doughnut') && type.id === 'norm'
        ? selectedRowKey.slice(-1)
        : selectedRowKey;
    // 如果还剩一个不可操作
    if (selectedRowLists.length === 0) {
      return;
    }
    setColumnsHead(chartAllChange(pitchCheck, selectedRowLists));
    setSelectedRowKeys(selectedRowLists);
    setSelectedRows(selectedRow);
  };
  /* 行选择配置 */
  const rowSelection = {
    selectedRowKeys,
    selectedRows,
    hideSelectAll: true,
    onChange: onSelectChange,
  };

  // table获取内容
  const lists = dataFormatter(dataTable);
  // 单行选中处理
  const onChange = (e: any, value: any, index: number) => {
    const filterData = chartHeadData?.filter((item) => item.check === true);
    if (filterData.length === 1 && filterData[0] === value) {
      return;
    }
    const selectData = chartHeadData?.map((item, ind) => {
      if (index === ind) {
        return {
          ...item,
          check: e.target.checked,
        };
      }
      if ((chartType === 'pieChart' || chartType === 'doughnut') && type.id === 'time') {
        return {
          ...item,
          check: false,
        };
      }
      return item;
    });
    const pitchCheck = selectData?.filter((item) => item.check === true)?.map((item) => item.name);
    setChartHeadData(selectData);
    setColumnsHead(chartAllChange(pitchCheck, selectedRowKeys));
  };

  // 图表类型切换
  const onTabsChange = (value: string) => {
    setChartType(value);
    setColumnsHead(energyChartData?.[value]?.valueData);
    setSelectedRowKeys(energyChartData?.[value]?.valueRow);
    if (value === 'pieChart' || value === 'doughnut') {
      if (type.id === 'norm') {
        setChartHeadData(headCheck(5));
      } else {
        setChartHeadData(headCheck(1));
      }
    } else {
      setChartHeadData(headCheck(5));
    }
  };
  // 点击详情图标
  // const clickIcon = (e: any, item: any) => {
  //   e.stopPropagation();
  //   setVisible(true);
  //   httpIndicatorModal({
  //     db: item.split('+')[3],
  //     type: item.split('+')[4],
  //     indicator: item.split('+')[0],
  //     region: item.split('+')[1],
  //     period: item.split('+')[6],
  //   }).then((res: any) => {
  //     if (res?.flag) {
  //       setIndicatorDetail({
  //         indicator: item.split('+')[0],
  //         indicatorTransaction: item.split('+')[5],
  //         description: res?.data?.description,
  //         destinationTranslation: res?.data?.destinationTranslation,
  //       });
  //     }
  //   });
  // };
  const columns = chartHeadData?.map((item, index) => ({
    title: (
      <div key={item.name} style={{ display: 'flex' }}>
        <Checkbox checked={item.check} onChange={(e) => onChange(e, item, index)} />
        <div style={{ marginLeft: 5 }}>
          <p>
            {item.name.split('+')[0]}
            <img
              src={Remind}
              style={{ fill: 'skyblue', margin: '-10px 5px' }}
              //  onClick={(e) => { clickIcon(e, item.name); }}
            />
          </p>
          {/* <span>{item.name.split('+')[1]}</span>-<span>{item.name.split('+')[2]}</span> */}
        </div>
      </div>
    ),
    width: 300,
    dataIndex: `${item.name}`,
    render: (v: any, record: any) => {
      // 是否行列选中
      const active = selectedRowKeys.includes(record.time) && selectedHeadColumnKeys[index];
      return <div className={cls(['table-cell', active && 'is-active'])}>{v}</div>;
    },
  }));

  columns.unshift({
    title: <span>时间</span>,
    width: 300,
    dataIndex: 'time',
    fixed: 'left',
  });

  return (
    <div style={{ position: 'relative' }}>
      <p style={{ position: 'absolute', fontSize: 18, fontWeight: 700, margin: 10 }}>图表类型</p>
      <Tabs
        className={styles['tabs-style']}
        defaultActiveKey="1"
        type="card"
        tabPosition="left"
        onChange={onTabsChange}
        tabBarGutter={20}
      >
        {chartData?.map((item) => (
          <TabPane
            tab={
              <div
                style={{
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'center',
                  // border: '1px solid black',
                  alignItems: 'center',
                  padding: '10 20',
                }}
              >
                {item.icon}
                <p>{item.name}</p>
              </div>
            }
            key={item.id}
          >
            {chartType === item.id ? <div style={{ width: '100%' }}>{item.component}</div> : null}
          </TabPane>
        ))}
      </Tabs>
      <Table
        style={{ paddingTop: 30 }}
        rowKey="time"
        rowSelection={rowSelection}
        columns={columns}
        dataSource={lists}
        scroll={{ x: 1000, y: '67vh' }}
      />
      <ModalComponent
        setVisible={setVisible}
        visible={visible}
        // indicatorDetail={indicatorDetail}
      />
    </div>
  );
});
export default ChartResult;
