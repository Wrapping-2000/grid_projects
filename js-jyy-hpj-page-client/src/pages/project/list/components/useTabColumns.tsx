import type { ProColumns } from '@ant-design/pro-table';
import { InfoCircleOutlined } from '@ant-design/icons';
import { Tooltip } from 'antd';
import type { OptionLabels } from './Selectors/useSelectors';

const isTitleRow = (record: Record<string, any>) => record.children;
const titleRender = (colSpan: number = 4, showChildren = true) =>
  (value: string, record: Record<string, any>) => {
    if (isTitleRow(record)) {
      return {
        children: value,
        props: {
          colSpan
        },
      }
    }
    const finalShow = record.isSingle || showChildren;
    return {
      children: finalShow ? value : null,
      props: {},
    }
  }

export default ({
  selectorValues,
  toggleModal
}: {
  selectorValues?: Record<OptionLabels, { label: string; value: string; }|undefined>;
  toggleModal: (name: OptionLabels, record: Record<string, any>) => void
}) => {
  // 生产render
  const renderFn = () =>
    (value: string, record: Record<string, any>) => {
      if (isTitleRow(record)) {
        return {
          children: value,
          props: {
            colSpan: 0
          },
        }
      }
      return {
        children: value,
        props: {},
      }
    }

  const renderTipFn = (tipName: string) =>
    (value: string, record: Record<string, any>) => {
      const children = [
        <span key="v1">{value}</span>,
        ( record[tipName] && value !== '-' ? (
          <Tooltip key="v2" placement="topRight" title={record?.[tipName]}>
            <InfoCircleOutlined style={{marginLeft: 8}} />
          </Tooltip>
          ) : null
        )
      ];

      return isTitleRow(record) ? {
          children,
          props: {
            colSpan: 0
          },
        } : {
          children,
          props: {
            record
          },
        }
    }

  // 建设过程columns
  const buildingProcessColumns: ProColumns<any>[] = [
    {
      title: '指标名称',
      dataIndex: 'name',
      render: titleRender(4),
      ellipsis: true,
    },
    {
      title: '指标状态',
      valueType: 'statusIndicator',
      render: renderTipFn('rule'),
    },
    {
      title: '指标值',
      dataIndex: 'value',
      render: renderTipFn('data_raw_string'),
    },
    {
      title: selectorValues?.construction_process_average?.label || '对比均值 ',
      dataIndex: 'average',
      filters: true,
      render: renderFn(),
      ellipsis: true,
    },
  ];

  // 运营效果
  const operationEffectColumns: ProColumns<any>[] = [
    {
      title: '指标名称',
      dataIndex: 'name',
      render: titleRender(7, false)
    },
    {
      title: '主变/线路',
      dataIndex: 'component_name',
      render: renderFn()
    },
    {
      title: '年份',
      dataIndex: 'year',
      render: renderFn()
    },
    {
      title: '指标状态',
      valueType: 'statusIndicator',
      render: renderTipFn('rule')
    },
    {
      title: '指标值',
      dataIndex: 'value',
      render: renderTipFn('rule')
    },
    {
      title: selectorValues?.operation_effect_average?.label || '对比均值 ',
      dataIndex: 'average',
      filters: true,
      render: renderFn()
    },
    {
      title: '指标趋势图',
      dataIndex: 'average',
      filters: true,
      render: renderFn(),
      renderText: (text, record) => (
        record.hasChartData ? <a onClick={() => toggleModal('operation_effect_average', record)}>点击查看</a> : '-'
      )
    },
  ];

  // 投资管控
  const investmentControlColumns: ProColumns<any>[] = [
    {
      title: '指标名称',
      dataIndex: 'name',
      render: titleRender(6)
    },
    {
      title: '年份',
      dataIndex: 'year',
      render: renderFn(),
      filters: true,
    },
    {
      title: '指标状态',
      valueType: 'statusIndicator',
      render: renderTipFn('rule')
    },
    {
      title: '指标值',
      dataIndex: 'value',
      render: renderTipFn('data_raw_string')
    },
    {
      title: selectorValues?.financial_benefits_average?.label || '对比均值 ',
      dataIndex: 'average',
      render: renderFn(),
      filters: true
    },
    {
      title: '指标趋势图',
      dataIndex: 'average',
      render: renderFn(),
      renderText: (text, record) => (
        record.hasChartData ? <a onClick={() => toggleModal('financial_benefits_average', record)}>点击查看</a> : '-'
      )
    },
  ];

  return [
    {
      columns: buildingProcessColumns,
    },
    {
      columns: operationEffectColumns,
    },
    {
      columns: investmentControlColumns,
    }
  ]
}
