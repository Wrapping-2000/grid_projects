import {Button, message} from 'antd';
import React, {useEffect, useRef, useState} from 'react';
import { PageContainer } from '@ant-design/pro-layout';
import ImportForm from "@/pages/visualContainer/dataSources/components/Import/ImportForm";
import ProTable, {ActionType, EditableFormInstance, EditableProTable, ProColumns} from "@ant-design/pro-table";
import getPagination from "@/util/getPagination";
import styles from "@/pages/visualContainer/dataSources/style.less";
import {excelListFormatter} from "@/util/formatter";
import {
  httpDeleteExcel,
  httpDelRow,
  httpGetExcelInfo,
  httpGetExcelList,
  httpSaveRow
} from "@/services/visual";
import Popconfirm from "@/components/Popconfirm";
import ProForm, {ProFormInstance} from "@ant-design/pro-form";
import {useModel} from "@@/plugin-model/useModel";


type DataSourceType = {
  id: React.Key;
  title?: string;
  dataIndex?: string;
};

const Import: React.FC = () => {
  const { initialState } = useModel('@@initialState');
  // @ts-ignore
  const { dicts } = initialState || {};

  const actionRef = useRef<ActionType>();
  const [importModalVisible, handleImportModalVisible] = useState<boolean>(false);
  const [columns_excel, setColumns] = React.useState<DataSourceType[]>(() => []);
  const [data_excel, setData] = React.useState<DataSourceType[]>(() => []);
  const [maxId, setMaxId] = React.useState<string>();
  const messageRef = useRef(null);
  const formRef = useRef<ProFormInstance<any>>();
  const [editableKeys, setEditableRowKeys] = useState<React.Key[]>(() => []);
  const [position, setPosition] = useState<'top' | 'bottom' | 'hidden'>('bottom');
  const editorFormRef = useRef<EditableFormInstance<DataSourceType>>();



  //excel数据内容
  const dataSource: DataSourceType[] = [];
  //excel表头
  const excelColumn: any[] = [];
  const excelColumnRendering = function (columns: string | any[], data: { [x: string]: any[]; }, total: number) {
    for (let i = 0; i < columns.length-1; i++) {
      let index = "column" + i;
      index.toString();
      let addingCol = {
        dataIndex: index,
        title: columns[i],
      };
      excelColumn.push(addingCol);
    }
    let addingEditCol = {
      dataIndex: "editCol",
      title: "操作",
      valueType: 'option',
      width: 120,
      render: (text: any, record: { id: React.Key; }, _: any, action: { startEditable: (arg0: any) => void; }) => [
        <a
          className={styles.link}
          key="editable"
          onClick={() => {
            action?.startEditable?.(record.id);
          }}
        >
          编辑
        </a>,
      ],
    }

    excelColumn.push(addingEditCol);
    setColumns(excelColumn);
    for (let j = 0; j < total; j++) {
      let addingData = {
        id: data.id[j],
      };
      for (let k = 0; k < columns.length-1; k++) {
        addingData[excelColumn[k].dataIndex] = data[excelColumn[k].title][j];
      }
      dataSource.push(addingData);
    }
    setData(dataSource);
    setMaxId(data.id[total-1]);
    // @ts-ignore

  }

  const columns: ProColumns[] = [
    {
      title: 'excel名称',
      dataIndex: 'excel_name',
      key: 'excel_name',
      ellipsis: true,
      render: (dom, entity) => {
        return (
          <a
            className={styles.link}
            onClick={() => {
              httpGetExcelInfo(entity.excel_name)
                .then(res => {
                  excelColumnRendering(res.data.excel[entity.excel_name].columns, res.data.excel[entity.excel_name].data, res.total);
                  }
                );
              }
            }
          >
            {dom}
          </a>
        );
      },
    },
    {
      title: '操作',
      dataIndex: 'option',
      valueType: 'option',
      width: 80,
      render: (_, record) => [
        <Popconfirm
          title="确认删除？"
          desc="将删除该excel的全部信息!"
          key="delete"
          placement="right"
          onConfirm={() => {
            httpDeleteExcel(record.excel_name)
              .then(res => {
                if (res?.code === 'SUCCESS') {
                  message.success('删除成功！');
                  actionRef.current?.reload();
                }
              })
              .catch(console.error)
              .finally()
            }
          }
        >
          <a className={styles.link}>
            删除
          </a>
        </Popconfirm>,
      ],
    },
  ];

  // 每次导入excel后reload
  useEffect(() => {
    window.addEventListener("click", (e) => {
      if (e.target != messageRef.current) {
        actionRef.current?.reload();
      }
    });
  }, []);

  // @ts-ignore
  // @ts-ignore
  return (
    <ProForm<{
      table: DataSourceType[];
    }>

      formRef={formRef}
      initialValues={{
        table: data_excel,
      }}
      validateTrigger="onBlur"
      submitter={false}
    >
      <PageContainer
        breadcrumb={false as unknown as any}
        header={{
          title: '数据源',
          ghost: true,
          extra: [
            <Button
              type="primary"
              onClick={() => {
                handleImportModalVisible(true);
                // actionRef.current?.reload();
              }}
              // icon={<PlusOutlined/>}
            >
              导入
            </Button>,

          ],
        }}
      >
        <div className={styles.container}>
          {/* 左边项目列表 */}
          <div className={styles['left-content']}>
            <ProTable
              headerTitle={"excel列表"}
              actionRef={actionRef}
              rowKey="excel_name"
              //搜索栏
              search={false}
              //菜单栏
              options={false}
              // @ts-ignore
              request={excelListFormatter(httpGetExcelList)}
              columns={columns}
              pagination={getPagination()}
            />
          </div>
          {/* 右侧数据展示区 */}
          <div className={styles['right-content']}>
            <EditableProTable
              rowKey="id"
              scroll={{
                x: 960,
              }}
              headerTitle="表格内容"
              //name="table"
              editableFormRef={editorFormRef}
              //搜索栏
              search={false}
              //菜单栏
              options={false}
              columns={columns_excel}
              dataSource={data_excel}
              //分页器
              pagination={getPagination()}
              value={data_excel}
              // @ts-ignore
              request={() => {
                return {
                  data: data_excel,//数据源注入
                  success: true,
                }
              }}

              recordCreatorProps={
                position !== 'hidden'
                  ? {
                    position: position as 'bottom',
                    // @ts-ignore
                    record: () => ({id: maxId?.substring(0, maxId?.lastIndexOf("_"))+"_"+String(parseInt(maxId?.substring(maxId?.lastIndexOf("_")+1))+1)}),

                  } : false
              }

              editable={{
                type: 'multiple',
                editableKeys,
                onChange: setEditableRowKeys,
                actionRender: (row, config, defaultDom) => {
                  return [
                    defaultDom.save,
                    defaultDom.delete,
                    defaultDom.cancel,
                  ];
                },
                onSave: async (rowKey, newData, oldData) => {
                  //保存时触发 rowKey是每行数据的id,newData是新填写的数据,oldData是老数据，依据业务需求向后台传参。
                  console.log("点击保存按钮");
                  var excelName = rowKey.toString().substring(0, rowKey.toString().lastIndexOf("_"));
                  let newDataString: string[] = [];

                  for (var i = 0; i < columns_excel.length-1; i++) {
                    // @ts-ignore
                    console.log('excelName：' + excelName,'行key：' + rowKey, '列key：' + columns_excel[i].title, '新值：' + newData[columns_excel[i].dataIndex], '旧值：' + oldData[columns_excel[i].dataIndex]);
                    // @ts-ignore
                    newDataString[i] = newData[columns_excel[i].dataIndex];
                  }
                  JSON.stringify(newDataString)
                  // @ts-ignore
                  httpSaveRow(excelName, rowKey.toString(), JSON.stringify(newDataString));
                  httpGetExcelInfo(excelName)
                    .then(res => {
                        excelColumnRendering(res.data.excel[excelName].columns, res.data.excel[excelName].data, res.total);
                      }
                    );
                },
                onCancel: async (rowKey, data) => {
                  console.log("点击取消按钮");
                  for (var i = 0; i < columns_excel.length-1; i++) {
                    // @ts-ignore
                    // console.log('行值：' + rowKey, '列值：' + columns_excel[i].dataIndex, '值：' + data[columns_excel[i].dataIndex]);
                  }
                },
                onDelete: async (rowKey, data) => {
                  //删除时触发 rowKey是每行数据的id,data是删除的数据，依据业务需求向后台传参。
                  console.log("点击删除按钮");
                  // @ts-ignore
                  console.log('行值：' + rowKey);
                  var excelName = rowKey.toString().substring(0, rowKey.toString().lastIndexOf("_"));
                  httpDelRow(excelName, rowKey.toString());
                  httpGetExcelInfo(excelName)
                    .then(res => {
                        excelColumnRendering(res.data.excel[excelName].columns, res.data.excel[excelName].data, res.total);
                      }
                    );
                },
              }}
            />
          </div>
        </div>
        <ImportForm
          importModalVisible={importModalVisible}
          handleImportModalVisible={handleImportModalVisible}
        />
      </PageContainer>
    </ProForm>
  );
};

export default Import;
