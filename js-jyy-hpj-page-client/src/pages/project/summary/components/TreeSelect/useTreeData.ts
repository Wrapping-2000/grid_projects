/* 汇总左侧树状数据 */
import React from 'react';
import { getSummaryTree } from '@/services/main';
import { summaryTreeFormatter } from '@/util/formatter';

// 默认展开第二级
const getDefaultOpenKeys = (list?: Record<string, any>[], deep = false) => {
  if (!list) return [];
  const deepKeys: string[] = [];
  const keys = list.map(item => {
    if (item.children) {
      const titleArray = item.children.map((d: Record<string, any>) => {
        if (deep && d?.children) {
          const key = (d.children || []).reduce((p: any, v: { key: any; }) => `${p}${v?.key ? `${v.key},` : ''}`, '')
          deepKeys.push(key);
        }
        return d?.title;
      });
      return titleArray.join(',') + ',';
    }
    return null;
  });

  const swallowList = keys.filter(v => !!v) as string[];
  return deep ? [...swallowList||[], ...deepKeys] : swallowList;
}

export default () => {
  // tab选中项
  const [activeKey, setActiveKey] = React.useState<HPJ.SummaryEvaluateType>('construction_control');

  // 树目录数据
  const [treeData, setTreeData] = React.useState<Record<HPJ.SummaryEvaluateType, any>>();

  // 当前选中的目录指标
  const [activeTreeData, setActiveTreeData] = React.useState<Record<HPJ.SummaryEvaluateType, any>>();

  const currentActiveTreeData = React.useMemo(() => {
    return activeTreeData?.[activeKey];
  }, [activeTreeData, activeKey])

  // 展开目录
  const [openKeys, setOpenKeys] = React.useState<Record<HPJ.SummaryEvaluateType, string[]>>();

  // 树目录显示类型
  const [treeDataTypes, setTreeDataTypes] = React.useState<Record<HPJ.SummaryEvaluateType, Record<HPJ.SummaryEvaluateType, HPJ.SummaryChartList>>>();

  // 当前指标图表显示类型
  const currentTreeDataType: HPJ.SummaryChartList | undefined = React.useMemo(() => {
    if (!treeDataTypes || !activeTreeData) return;
    const key = activeTreeData[activeKey]?.type?.selectedKeys?.[0];
    return treeDataTypes[activeKey]?.[key];
  }, [treeDataTypes, activeKey, activeTreeData]);

  // console.log(treeDataTypes, 'treeDataTypes')
  console.log(currentTreeDataType, '图表类型')

  // 初始请求数据
  React.useEffect(() => {
    Promise.all((['construction_control', 'operation_effect', 'investment_control'] as HPJ.SummaryEvaluateType[]).map((t: HPJ.SummaryEvaluateType) => getSummaryTree(t)))
      .then(([r1, r2, r3]) => {
        if (r1?.code === 'SUCCESS' && r2?.code === 'SUCCESS' && r3?.code === 'SUCCESS') {
          const [constructionControlTree, constructionControlTreeType] = summaryTreeFormatter(r1.data);
          const [operationEffectTree, operationEffectTreeType] = summaryTreeFormatter(r2.data);
          const [investmentControlTree, investmentControlTreeType] = summaryTreeFormatter(r3.data);
          // 设置数据
          setTreeData({
            'construction_control': constructionControlTree,
            'operation_effect': operationEffectTree,
            'investment_control': investmentControlTree,
          })
          // 设置展开
          setOpenKeys({
            'construction_control': getDefaultOpenKeys(constructionControlTree),
            'operation_effect': getDefaultOpenKeys(operationEffectTree),
            'investment_control': getDefaultOpenKeys(investmentControlTree),
          });
          // 设置目录数据展示类型
          setTreeDataTypes({
            'construction_control': constructionControlTreeType,
            'operation_effect': operationEffectTreeType,
            'investment_control': investmentControlTreeType,
          } as Record<HPJ.SummaryEvaluateType, Record<HPJ.SummaryEvaluateType, HPJ.SummaryChartList>>)
        }
      })
      .catch(console.error)
      .finally();
  }, []);

  // 搜索
  const getTreeData = (search: string) => {
    if (!activeKey) {
      return;
    }
    getSummaryTree(activeKey, {search})
      .then((r) => {
        if (r?.code === 'SUCCESS') {
          // 设置树数据
          const [data] = summaryTreeFormatter(r.data);
          console.log(data, 'datttt设置树数据')
          console.log(getDefaultOpenKeys(data, true), '展开项目')
          setTreeData((state) => ({
              ...state,
              [activeKey]: data,
            }) as Record<HPJ.SummaryEvaluateType, string[]|undefined>,
          )
          // 设置展开项
          setOpenKeys((oldStates) => ({
            ...(oldStates||{}) as Record<HPJ.SummaryEvaluateType, string[]>,
            [activeKey]: getDefaultOpenKeys(data, true)
          }))
        }
      })
      .catch()
      .finally();
  }

  // 选择树目录，
  const onSelect = (v: Record<string, any>) => {
    setActiveTreeData((state) => ({
        ...(state||{}),
        [activeKey]: v
      }) as Record<HPJ.SummaryEvaluateType, any>
    );
  }

  // 生产设置展开项函数
  const makeSetOpenKeys = (type: HPJ.SummaryEvaluateType): (v: HPJ.SummaryEvaluateType[]) => void =>
    (v: HPJ.SummaryEvaluateType[]) => {
      if (!type) return;
      setOpenKeys((oldStates) => ({
        ...(oldStates||{}) as Record<HPJ.SummaryEvaluateType, string[]>,
        [type]: v
      }))
    }

  // active tab的index
  const activeKeyIndex = React.useMemo(() => ['construction_control',  'operation_effect', 'investment_control'].indexOf(activeKey), [activeKey]);

  return {
    treeData,
    getTreeData,
    onSelect,
    activeTreeData: currentActiveTreeData,
    openKeys,
    makeSetOpenKeys,
    activeKey,
    activeKeyIndex,
    setActiveKey,
    treeDataTypes,
    currentTreeDataType
  }
}
