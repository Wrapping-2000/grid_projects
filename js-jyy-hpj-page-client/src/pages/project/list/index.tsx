import { Button, message } from 'antd';
import React, { useState, useRef } from 'react';
import { useModel } from 'umi';
import { PageContainer } from '@ant-design/pro-layout';
import type { ProColumns, ActionType } from '@ant-design/pro-table';
import ProTable from '@ant-design/pro-table';
import UpdateForm from './components/UpdateForm';
import ProjectDrawer from './components/ProjectDrawer';
import Popconfirm from '@/components/Popconfirm';
import { getProjectList, deleteProjectDetail } from '@/services/main';
import { projectListFormatter } from '@/util/formatter';
import getPagination from '@/util/getPagination';
import styles from './style.less';


const TableList: React.FC = () => {
  const { initialState } = useModel('@@initialState');
  const { dicts } = initialState || {};

  const actionRef = useRef<ActionType>();

  /**
   * 上传弹窗
   * */
  const [updateModalVisible, handleUpdateModalVisible] = useState<boolean>(false);

  /**
   * 是否显示抽屉
   * */
  const [showDetail, setShowDrawer] = useState<boolean>(false);

  const setShowDetail = (v: boolean) => {
    setShowDrawer(v);
    // 关闭时刷新
    if (!v) {
      actionRef.current?.reload();
    }
  }

  /**
   * 当前行
   * */
  const [currentRow, setCurrentRow] = useState<API.Project>();


  const columns: ProColumns<API.Project>[] = [
    {
      title: '项目名称',
      dataIndex: 'project_name',
      width: '30%',
      ellipsis: true,
      render: (dom, entity) => {
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
    },
    {
      title: 'WBS编码',
      dataIndex: 'wbs_code',
    },
    {
      title: '电压等级(KV)',
      dataIndex: 'voltage_level',
      valueType: 'select',
      valueEnum: dicts?.voltage_level
    },
    {
      title: '工程分类',
      dataIndex: 'classification',
      hideInForm: true,
      valueType: 'select',
      fieldProps: {
        allowClear: true
      },
      valueEnum: dicts?.classification || {},
      width: '16%',
      ellipsis: true,
    },
    {
      title: '实际投运年',
      dataIndex: 'operation_year',
      // @ts-ignore
      valueType: 'customDateYear',
      // valueEnum: dicts?.operation_year || {},
    },
    {
      title: '所属公司',
      dataIndex: 'company',
      hideInForm: true,
      width: '20%',
      ellipsis: true,
    },
    {
      title: '操作',
      dataIndex: 'option',
      valueType: 'option',
      width: 80,
      render: (_, record) => [
        <Popconfirm
          title="确认删除？"
          desc="将删除该项目的全部信息及项目评价内容"
          key="delete"
          placement="right"
          onConfirm={() => {
            deleteProjectDetail(record.wbs_code)
              .then(r => {
                if (r?.code === 'SUCCESS') {
                  message.success('删除成功！');
                  actionRef.current?.reload();
                }
              })
              .catch(console.error)
              .finally()
          }}
        >
          <a>
            删除
          </a>
        </Popconfirm>,
      ],
    },
  ];

  return (
    <PageContainer className={styles.container} title={false} breadcrumb={false as unknown as any}>
      <ProTable<API.Project, any>
        headerTitle="项目列表"
        actionRef={actionRef}
        rowKey="wbs_code"
        search={{
          className: styles.search,
          span: {
            xs: 24,
            sm: 24,
            md: 12,
            lg: 12,
            xl: 6,
            xxl: 3,
          },
          labelWidth: 90,
          defaultCollapsed: false,
          collapseRender: () => null
        }}
        toolBarRender={() => {
          return (
            [<Button key="update" type="primary" onClick={() => handleUpdateModalVisible(true)}>更新</Button>]
          )
        }}
        options={false}
        // @ts-ignore
        request={projectListFormatter(getProjectList)}
        columns={columns}
        pagination={getPagination()}
      />
      <UpdateForm
        updateModalVisible={updateModalVisible}
        handleUpdateModalVisible={handleUpdateModalVisible}
      />
      {/* 项目详情抽屉 */}
      {
        showDetail && <ProjectDrawer
          visible={showDetail}
          // @ts-ignore
          columns={columns}
          currentRow={currentRow}
          setCurrentRow={setCurrentRow}
          setShowDetail={setShowDetail}
          scroll={{x: 'max-content'}}
        />
      }
    </PageContainer>
  );
};

export default TableList;
