import React from 'react';
// import ProTable from '@ant-design/pro-table';
import ProTable from '@ant-design/pro-table';
import type { ActionType, ProTableProps } from '@ant-design/pro-table';
import { getSummaryData } from '@/services/main';
import { summaryDataFormatter, valueEnumFormatter } from '@/util/formatter';
import getPagination from '@/util/getPagination';
import styles from '../../style.less';

function TableList<U>(props: {
  activeTreeData?: Record<string, any>; // 选中的树目录指标
  chartsType?: HPJ.SummaryChartList;
  isContinuousValues?: boolean; // 是否连续值
  averageClassification?: HPJ.AverageClassification; // 下拉参数
  setCurrentRow: (v: any) => void; // 设置当前行
  setShowDetail: (v: boolean) => void; // 设置抽屉显示
  selectedPieArea: Record<string, any>; // 选中饼图区域
  selected: Record<string, any>; // 选中柱状图条
} & ProTableProps<API.Project, U>) {
  const {
    // columns,
    activeTreeData,
    chartsType,
    averageClassification: defaultAverageClassification,
    setCurrentRow,
    setShowDetail,
    isContinuousValues,
    selected: defaultSelected,
    selectedPieArea: defaultSelectedPieArea,
  } = props;

  // 无图表数据需要去除图表上带来的参数
  const {
    averageClassification,
    selected,
    selectedPieArea,
  } = React.useMemo(() => {
    let finalAverageClassification;
    let finalSelected;
    let finalSelectedPieArea;
    // 有折线或者柱状
    if ((chartsType||[]).some(item => item === 'bar' || item === 'line')) {
      finalSelected = defaultSelected;
      finalAverageClassification = defaultAverageClassification;
    }

    // 有饼图
    if ((chartsType||[]).some(item => item === 'pie')) {
      finalSelectedPieArea = defaultSelectedPieArea;
    }
    return {
      averageClassification: finalAverageClassification,
      selected: finalSelected,
      selectedPieArea: finalSelectedPieArea,
    }
  }, [defaultAverageClassification, defaultSelected, defaultSelectedPieArea, chartsType])
  const actionRef = React.useRef<ActionType>();

  // 表头
  const [columns, setColumns] = React.useState<Record<string, any>[]>();

  // 加工表头
  const formattedColumns = React.useMemo(() => {
    const newColumns = columns?.map((c: Record<string, any>) => {
      const safeColumn = c || {}
      if (safeColumn?.order) {
        delete safeColumn.order;
      }
      const commonProps: Record<string, any> = {
        ...safeColumn,
        colSize: 2,
        ellipsis: true,
        title: safeColumn.cn_name,
        dataIndex: safeColumn.en_name,
        valueType: ({
          select: 'select',
          string: undefined,
          year: 'customDateYear',
        })[c?.type],
        hideInSearch: !c?.type,
        valueEnum: c?.value ? valueEnumFormatter(c.value) : undefined,
        fieldProps: {
        }
      };

      if (commonProps?.value) {
        delete commonProps.value;
      }

      // 固定
      const currentProps = ['project_name', 'component_name'].includes(safeColumn.en_name) ? ({
        ...commonProps,
        fixed: 'left'
      }) : commonProps;

      // 表头
      if (safeColumn.en_name === 'project_name') {
        return {
          ...currentProps,
          render: (dom: React.ReactNode, entity: Record<string, any>) => {
            return (
              <a
                className={styles.link}
                onClick={() => {
                  setCurrentRow(entity);
                  setShowDetail(true);
                }}
              >
                {dom}
              </a>
            );
          },
        }
      }

      // 状态指标
      if (safeColumn.en_name === 'status_msg') {
        return {
          ...currentProps,
          valueType: 'statusIndicator',
          ellipsis: undefined,
          dataIndex: 'status'
        }
      }

      // 改疼痛

      return currentProps;
    });
    return newColumns?.sort((prev: Record<string, any>, next: Record<string, any>) => prev?.order - next?.order)
  }, [columns, setShowDetail, setCurrentRow]);

  // 切换左侧树指标时，重置表单页码
  React.useEffect(() => {
    if (actionRef.current?.reload) {
      actionRef.current?.reload(true);
    }
  }, [activeTreeData]);

  // table 数据请求参数 指标：name, 连续纸年：target_year, 单值：下拉值作为key
  const params = React.useMemo(() => {
    const sParams: Record<string, any> = {
      name: activeTreeData?.type?.selectedKeys?.[0],
    }
    // 带上左图数据
    if ((chartsType||[]).some(item => item === 'bar' || item === 'line')) {
      // 下拉数据
      sParams.contrast_filed = averageClassification;

      // 点击某个图表数据
      const paramKey = isContinuousValues ? 'target_year' : (averageClassification||''); // 柱状图参数，如是连续值传target_year：value，否则[下拉值]：点击值
      sParams[paramKey] = selected?.name;
    }

    // 带上饼图数据
    if ((chartsType||[]).some(item => item === 'pie')) {
      sParams.start = selectedPieArea?.data?.start;
      sParams.end = selectedPieArea?.data?.end;
    }
    return sParams;
  }, [isContinuousValues, activeTreeData, selectedPieArea, selected, chartsType, averageClassification]);

  // 根据显示图表类型决定是否展示搜索
  const tableInfo: {
    search: ProTableProps<API.Project, any>['search'];
  } = React.useMemo(() => {
    const safeCharts = chartsType || [];
    const showPie = safeCharts.includes('pie');
    const showLine = safeCharts.includes('line');
    const showBar= safeCharts.includes('bar');
    return {
      search: (!showPie && !showLine && !showBar) ? ({
        className: styles.search,
        defaultCollapsed: false,
        collapseRender: () => null,
        labelWidth: 100,
        span: {
          xs: 24,
          sm: 24,
          md: 12,
          lg: 12,
          xl: 6,
          xxl: 4,
        },
      }) : false
    }
  }, [chartsType]);

  const postData = (v: Record<string, any>) => {
    const value = summaryDataFormatter(v);
    setColumns(value?.columns);
    console.log(value?.dataSource.map((d: { project_name: any; component_name: any; }) => `${d.project_name}_${d.component_name}`), 'value?.dataSource')
    return value?.dataSource;
  }

  return (
    <ProTable<any, any>
      headerTitle="项目列表"
      actionRef={actionRef}
      rowKey={(row) => {
        console.log(`${row.project_name}_${row.component_name}`, 2222)
        return `${row.project_name}_${row.component_name}`
      }}
      search={tableInfo.search}
      options={false}
      params={params}
      // @ts-ignore
      request={getSummaryData}
      postData={postData}
      columns={[...formattedColumns||[]]}
      pagination={getPagination()}
      scroll={{
        x: 'max-content'
      }}
      style={{marginTop: 1}}
    />
  );
}

export default TableList;
