import {  Card } from 'antd';
import React, { useState } from 'react';
import { PageContainer } from '@ant-design/pro-layout';
import ProjectDrawer from '../list/components/ProjectDrawer';
import TreeSelect, { useTreeData } from './components/TreeSelect';
import RightContent, { useContentData } from './components/RightContent';
import styles from './style.less';

const Summary: React.FC = () => {
  // 显示抽屉
  const [showDetail, setShowDetail] = useState<boolean>(false);

  // 当前操作行
  const [currentRow, setCurrentRow] = useState<API.Project>();

  // 左侧树状数据
  const tree = useTreeData();

  // 根据左侧选中内容，生产右侧内容数据
  const contentData = useContentData({
    params: tree.activeTreeData,
    chartsType: tree.currentTreeDataType
  });

  return (
    <PageContainer breadcrumb={false as any}>
      <div className={styles.container}>
        {/* 左边树形选择器 */}
        <Card className={styles['left-content']} bodyStyle={{paddingTop: 8}}>
          <TreeSelect
            {...tree}
          />
        </Card>
        {/* 右侧数据展示区 */}
        <div className={styles['right-content']}>
          <RightContent
            {...contentData}
            activeKey={tree.activeKey}
            chartsType={tree.currentTreeDataType}
            activeTreeData={tree.activeTreeData}
            setShowDetail={setShowDetail}
            setCurrentRow={setCurrentRow}
            currentRow={currentRow}
            currentTreeDataType={tree.currentTreeDataType}
          />
        </div>
      </div>
      {/* 项目详情抽屉 */}
      {
        showDetail && (
          <ProjectDrawer
            visible={showDetail}
            currentRow={currentRow}
            setCurrentRow={setCurrentRow}
            setShowDetail={setShowDetail}
            initTabIndex={tree.activeKeyIndex}
            initEvaluateType={tree.activeTreeData}
          />
        )
      }

    </PageContainer>
  );
};

export default Summary;
