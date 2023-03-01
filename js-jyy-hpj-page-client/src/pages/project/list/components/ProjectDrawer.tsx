import React from 'react';
import { Drawer, Tag, Tabs } from 'antd';
import ProTable, { EditableProTable } from '@ant-design/pro-table';
import type { ActionType } from '@ant-design/pro-table';
import type { ProTableProps } from '@ant-design/pro-table';
import ProCard from '@ant-design/pro-card';
import _, { isArray } from 'lodash';
import {
  getProjectDetail,
  getProjectEvaluateConstructionProcess,
  getProjectEvaluateOperationEffect,
  getProjectEvaluateFinancialBenefits
} from '@/services/main';
import  * as tablePostData from '@/util/tablePostData';
import  Chart from './Chart';
import useTabColumns from './useTabColumns';
import Selectors, { useSelectors } from './Selectors';
import styles from '../style.less';

const tabs: HPJ.ProjectEvaluateType[] = ['construction_process', 'operation_effect', 'financial_benefits'];

export default (props: {
  currentRow?: API.Project;
  visible: boolean;
  setCurrentRow: (v: any) => void;
  setShowDetail: (v: boolean) => void;
  initTabIndex?: number, // 默认选中的tab index
  initEvaluateType?: Record<string, any>
}) => {
  const {currentRow, visible, initTabIndex, initEvaluateType} = props;

  // 编辑行
  const [editableKeys, setEditableRowKeys] = React.useState<React.Key[]>([]);

  // 详情动态列
  const [columnDetail, setColumnDetail] = React.useState<API.ProjectDetailList>();

  // 项目可编辑详情信息表格key
  const editingData = React.useRef<Record<string, any>[]>([]);

  // 图表弹窗显示
  const [chartModalVisible, toggleModal] = React.useState<boolean>(false);

  // 图表
  const [chartRecord, setChartRecord] = React.useState<Record<string, any>>();

  // 图表数据-用于查找默认展开
  const [initTabData, setInitTabData] = React.useState<Record<string, any>>();

  // 第一次请求是否结束
  const [firstFetching, setFirstFetching] = React.useState<boolean>();
  const set1stFetching = (v: boolean) => {
    if (firstFetching === undefined) {
      setFirstFetching(v)
    }
  }

  // 当前tab是需要默认选中的，存储当前请求到的数据用于生产
  const setInitTabDataWhenRequest = (type: string, data?: Record<string, any>) => {
    if (!_.isNil(initTabIndex) && tabs[initTabIndex] && tabs[initTabIndex] === type) {
      setInitTabData(data);
    }
  }

  // 默认展开keys
  const [defaultExpandable, setDefaultExpandable] = React.useState<string[]>();

  // 受控展开keys
  const [expandable, setExpandable] = React.useState<string[]>();

  // 获取默认展开keys
  React.useEffect(() => {
    if (!initEvaluateType) return;
    if (!initTabData) return;
    // 从initTabData中寻找initEvaluateType项， 生产table所需要的expandable字段
    const selectedKey = initEvaluateType?.type?.selectedKeys?.[0];
    let targetKey: string|undefined = undefined;
    Object.entries((initTabData||{})).some(([key, value]: [string, Record<string, any>[]]) => {
      if (!isArray(value)) {
        return false;
      }
      const t = (value||[]).find(v => v?.name === selectedKey)
      if (t) {
        targetKey = key;
        return true;
      }
      return false;
    })
    const expandKeys = targetKey ? [targetKey] : undefined
    setExpandable(expandKeys);
    setDefaultExpandable(expandKeys);
  }, [initEvaluateType, initTabData]);

  // 滚动到指定项目
  React.useEffect(() => {
    setTimeout(() => {
      const selectedKey = initEvaluateType?.type?.selectedKeys?.[0];

      const targetRow = document.querySelector(`tr[data-row-key='${selectedKey}']`);

      if (targetRow && targetRow.scrollIntoView) {
        targetRow.scrollIntoView({behavior: "smooth"});
        (targetRow as HTMLDivElement).style.backgroundColor = 'rgba(42,253,154,0.1)';
      }
    }, 10);
  }, [defaultExpandable, initEvaluateType, initTabData]);

  // 是否在编辑
  // const [isEditing, setEditing] = React.useState(false);

  const columns = React.useMemo(() => {
    return columnDetail?.map(d => {
      return d
    })
  }, [columnDetail]);

  // tags
  const tags = React.useMemo(() => {
    if (!currentRow) {
      return null;
    }

    const list = [
      {
        key: 'voltage_level',
        getValue: () => currentRow.voltage_level,
        format: (v: string|number|undefined|null) => _.isNil(v) ? null : `${v}kV`,
      },
      {
        key: 'classification',
        getValue: () => currentRow.classification,
        format: (v: string|number|undefined|null) => _.isNil(v) ? null : `${v}`,
      },
      {
        key: 'operation_year',
        getValue: () => currentRow.operation_year,
        format: (v: string|number|undefined|null) => _.isNil(v) ? null : `${v}年投运`,
      },
      {
        key: 'company_province',
        getValue: () => currentRow.company_city || currentRow.company_province,
        format: (v: string|number|undefined|null) => _.isNil(v) ? null : `${v}`,
      },
    ];

    const tagsWithData = list.map(item => {
      const value = item.getValue();
      return {
        key: item.key,
        value: _.isNil(value) ? null : item.format(value)
      }
    });

    const finalTagsList = tagsWithData.filter(t => !_.isNil(t?.value));
    return finalTagsList.map(t => (
      <Tag key={t?.key} color="processing" className={styles.tag}>{t?.value}</Tag>
    ));
  }, [currentRow])

  // projectInfoRef
  const projectInfoRef = React.useRef<ActionType>();

  // 表单编辑临时数据
  const editedInfoRef = React.useRef<Record<string, any>|null>();

  // 评价参数下拉选择
  const selectors = useSelectors({
    wbsCode: currentRow?.wbs_code
  });

  // 当前显示图表属于哪个评价指标
  const [currentTab, setCurrentTab] = React.useState<HPJ.ProjectEvaluateType>(initTabIndex ? tabs[initTabIndex] : 'construction_process');

  const toggleTabs = (v: string) => {
    setCurrentTab(v as HPJ.ProjectEvaluateType)
  }

  const tabColumns = useTabColumns({
    selectorValues: selectors.values,
    toggleModal: (name, record) => {
      toggleModal(v => !v);
      setChartRecord(record);
    }
  });

  const fetchDetail = async (wbsCode?: string): Promise<API.ProjectDetail> => {
    if (!wbsCode) return [];

    return getProjectDetail(wbsCode)
      // @ts-ignore
      .then((r) => {
        if (r?.code === 'SUCCESS') {
          const cl = Object.entries(r?.data?.columns || []).map(([dataIndex, title]) => ({
            dataIndex,
            title,
            editable: () => dataIndex !== 'wbs_code',
          }))
          setColumnDetail(cl);
          return Promise.resolve({
            data: r?.data?.data_source ? [r.data.data_source] : []
          });
        }
        return [];
      })
  }

  const tabTableProps: Partial<ProTableProps<any, any>> = {
    rowKey: 'key',
    pagination: false,
    search: false,
    toolBarRender: false,
    scroll: {x: 'max-content'}
  }

  // 评价表格tab信息
  const projectEvaluateTabs: {
    key: HPJ.ProjectEvaluateType;
    name: string;
    expandable?: ProTableProps<any, any>['expandable'];
    [key: string]: any;
  }[] = [
    {
      name: '建设过程',
      key: 'construction_process',
      postData: tablePostData.construction_process,
      params: {
        construction_process_average: selectors.values?.construction_process_average?.value
      },
      request: async(params: Record<string, string>) => {
        set1stFetching(true);
        const res = await getProjectEvaluateConstructionProcess({
          wbsCode: currentRow?.wbs_code,
          ...params,
        });
        setInitTabDataWhenRequest('construction_process', res?.data);
        set1stFetching(false);
        return res;
      },
    },
    {
      name: '运行效果',
      key: 'operation_effect',
      postData: tablePostData.operation_effect,
      params: {
        operation_effect_average: selectors.values?.operation_effect_average?.value,
        operation_effect_type: selectors.values?.operation_effect_type?.value,
        operation_effect_year: selectors.values?.operation_effect_year?.value
      },
      request: async(params: Record<string, string>) => {
        if (!params.operation_effect_type) return; // operation_effect_type是接口请求来的，所以初始undefined时不请求
        set1stFetching(true);
        const res = await getProjectEvaluateOperationEffect({
          wbsCode: currentRow?.wbs_code,
          ...params,
        });
        setInitTabDataWhenRequest('operation_effect', res?.data);
        set1stFetching(false);
        return res;
      },
    },
    {
      name: '投资管控',
      key: 'financial_benefits',
      postData: tablePostData.financial_benefits,
      params: {
        financial_benefits_average: selectors.values?.financial_benefits_average?.value,
        financial_benefits_year: selectors.values?.financial_benefits_year?.value
      },
      request: async(params: Record<string, string>) => {
        set1stFetching(true);
        const res = await getProjectEvaluateFinancialBenefits({
          wbsCode: currentRow?.wbs_code,
          ...params,
        });
        setInitTabDataWhenRequest('financial_benefits', res?.data);
        set1stFetching(false);
        return res;
      },
    }
  ]

  const onValuesChange = (v: Record<string, any>) => {
    editedInfoRef.current = v;
  }

  return (
    <>
      <Drawer
        className={styles.drawer}
        extra={<span className={styles['wbs-code']}>项目详情</span>}
        width="78%"
        visible={visible}
        onClose={() => {
          props.setCurrentRow(undefined);
          props.setShowDetail(false);
        }}
        closable
        destroyOnClose
        bodyStyle={{background: '#f0f2f5', paddingTop: 0, borderBottom: '0'}}
      >
        {/* 头部 */}
        <div className={styles['header-info']}>
          <div><span>{currentRow?.project_name}</span><span>{currentRow?.wbs_code}</span></div>
          <div style={{marginTop: 16}}>
            {tags}
          </div>
        </div>

        {/* 基本信息 */}
        <EditableProTable<API.TableProjectInfoType>
          actionRef={projectInfoRef}
          headerTitle="项目基本信息"
          columns={columns}
          request={async () => {
            const res = await fetchDetail(currentRow?.wbs_code);
            editingData.current = (res?.data||[]);
            return res;
          }}
          rowKey="wbs_code"
          // 编辑需求临时关闭
          // toolBarRender={() => {
          //   if (isEditing) {
          //     return [
          //       <Button
          //         onClick={() => {
          //           setEditing(false);
          //           setEditableRowKeys([]);
          //         }}
          //       >
          //         取消
          //       </Button>,
          //       <Button
          //         type="primary"
          //         onClick={() => {
          //           setEditing(false);
          //           setEditableRowKeys([]);
          //           putProjectDetail(editedInfoRef.current)
          //             .then((r: any) => {
          //               if (r?.code === 'SUCCESS') {
          //                 message.success('更新成功!')
          //                 editedInfoRef.current = null;
          //               }
          //             })
          //             .finally(() => {
          //               projectInfoRef.current?.reload();
          //             });
          //         }}
          //       >
          //         保存
          //       </Button>
          //     ]
          //   }
          //   return [
          //     <Button
          //       onClick={() => {
          //         setEditableRowKeys((editingData.current||[]).map((v: Record<string, string>) => v.wbs_code));
          //         setEditing(true);
          //       }}
          //     >
          //       编辑
          //     </Button>
          //   ]
          // }}
          editable={{
            editableKeys,
            onChange: setEditableRowKeys,
            onValuesChange
          }}
          recordCreatorProps={{
            style: {display: 'none'}
          } as any}
          scroll={{x: 'max-content'}}
        />

        {/* tabs */}
        <ProCard
          tabs={{
            type: 'card',
            activeKey: currentTab,
            onChange: toggleTabs
          }}
        >
          {
            projectEvaluateTabs.map((item, index) => {
              if (initEvaluateType && firstFetching !== false) {
              }
              const controlledExpandable = initEvaluateType && !_.isNil(initTabIndex) && tabs[initTabIndex] === item.key;
              return (
                <Tabs.TabPane key={item.key} tab={item.name}>
                  <Selectors {...selectors} currentTab={item.key} />
                  <ProTable
                    {...tabTableProps}
                    params={item.params}
                    columns={tabColumns[index].columns}
                    request={item.request}
                    postData={item.postData}
                    expandable={controlledExpandable ? {
                      expandedRowKeys: expandable,
                      onExpand: (expanded: boolean, record: any) => {
                        setExpandable((exp) => {
                          if (expanded) {
                            return [...(exp||[]), record?.key]
                          };
                          const v = _.dropWhile(exp, (o) => {
                            return o === record?.key
                          });
                          return v;
                        })
                      }
                    } : undefined}
                    style={{padding: '0 24px 24px 24px'}}
                  />
                </Tabs.TabPane>
              )
            })
          }
        </ProCard>
        {/* 趋势图表 */}
        <Chart onCancel={() => toggleModal(false)} record={chartRecord} visible={chartModalVisible} averageName={selectors.values?.[`${currentTab}_average`]?.label || '对比均值 '} />
      </Drawer>
    </>
  )
}
