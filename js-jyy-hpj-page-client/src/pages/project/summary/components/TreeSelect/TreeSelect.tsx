import React from 'react';
import { Input, Menu, Tabs } from 'antd';
const { Search } = Input;
import styles from '../../style.less';


function TreeSelect(props: {
  onSelect: (v: Record<string, any>) => void;
  treeData?: Record<HPJ.SummaryEvaluateType, any>;
  getTreeData: (v: string) => void;
  makeSetOpenKeys: (t: HPJ.SummaryEvaluateType) => (keys: HPJ.SummaryEvaluateType[]) => void;
  openKeys?: Record<HPJ.SummaryEvaluateType, string[]>;
  setActiveKey: (text: HPJ.SummaryEvaluateType) => void;
  activeKey: HPJ.SummaryEvaluateType;
  [key: string]: any;
}) {
  const {onSelect, treeData, getTreeData, openKeys, makeSetOpenKeys, activeKey, setActiveKey} = props;

  // tabs数据
  const tabsData = React.useMemo<{key: HPJ.SummaryEvaluateType, [key: string]: any}[]>(() => ([
     {
      name: '建设管控',
      key: 'construction_control',
    },
    {
      name: '运行效果',
      key: 'operation_effect',
    },
    {
      name: '投资管控',
      key: 'investment_control',
    }
  ]), []);

  const renderItem = (currentLevel: Record<string, any>, level = 0) => {
    if (currentLevel.children) {
      const key = currentLevel.children.reduce((prev: string, next: {key: string}) => `${prev}${next.key},`, '');
      return (
        <Menu.SubMenu key={key} title={currentLevel.title} className={styles[`submenu-lv${level}`]}>
          {currentLevel.children.map((item: Record<string, any>) => renderItem(item, level + 1))}
        </Menu.SubMenu>
      )
    }
    return (
      <Menu.Item key={currentLevel.key} className={styles[`tree-menu`]}>{currentLevel.title}</Menu.Item>
    )
  };

  return (
    <div>
      <Tabs
        onTabClick={(v: string) => setActiveKey(v as HPJ.SummaryEvaluateType)}
        activeKey={activeKey}
      >
        {tabsData?.map((item) => {
          const tabData = treeData?.[item.key];
          return (
            <Tabs.TabPane key={item.key} tab={item.name}>
              <Search allowClear placeholder="搜索指标" onSearch={getTreeData} style={{ marginBottom: 8 }} />
              <Menu
                inlineCollapsed={false}
                mode="inline"
                onSelect={(type: Record<string, any>) => onSelect({
                  key: item.key,
                  type
                })}
                openKeys={openKeys?.[item.key]}
                onOpenChange={(v: string[]) => makeSetOpenKeys(item.key)(v as HPJ.SummaryEvaluateType[])}
              >
                {tabData ? tabData.map((data: Record<string, any>) => renderItem(data)) : null}
              </Menu>
            </Tabs.TabPane>
          )
        })}
      </Tabs>
    </div>
  );
}

export default TreeSelect;
