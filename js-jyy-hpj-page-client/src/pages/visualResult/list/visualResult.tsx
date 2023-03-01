import React, { useState, useRef, useEffect } from 'react';
import { useLocation } from 'umi';
import { Button, Breadcrumb } from 'antd';
import { DownloadOutlined } from '@ant-design/icons';
import { PageContainer } from '@ant-design/pro-layout';
import MonthlyContent from '../components/monthly-content';
import { useSelect, SimpleSelect, Select } from '../../../components/select';
import { httpGetAllClassificationData } from '../../../services/visual';
import styles from '../visualResult.less';

export default function (): JSX.Element {
  const yearDataRef = useRef<any>(null);
  const quarterDataRef = useRef<any>(null);
  const monthDataRef = useRef<any>(null);
  const dayDataRef = useRef<any>(null);
  const Location = useLocation();
  // const [activeKey, setActiveKey] = useState();
  const [monthData, setMonthData] = useState([]);
  const typeList = [
    { name: '指标名称', id: 'norm' },
    { name: '时间', id: 'time' },
  ];
  const typeSelect = useSelect({ dataSource: typeList });

  // function tabsCallback(value) {
  //   setActiveKey(value);
  // }
  /* 切换类型 */
  const onTypeSelectChange = (value) => {
    const type = typeList.find((item) => value === item?.name);
    typeSelect.setValue(type);
  };
  console.log(Location.state?.value)
  useEffect(() => {
    httpGetAllClassificationData(Location.state?.value).then((res) => {
      if (res) {
        const allTime = [
          ...new Set(
            res.data
              .flat(2)
              .map((items) => items?.resultList?.map((it) => it.time))
              .flat(2),
          ),
        ];
        const allCountData = res.data.flat(2).map((item) => {
          return {
            ...item,
            resultList: allTime.map((itemc) => {
              const datas = item.resultList.filter((itema) => itema.time === itemc);
              return { time: itemc, value: datas.length > 0 ? datas[0].value : '-' };
            }),
          };
        });
        console.log(allCountData, res.data.flat(2));

        setMonthData([
          {
            period: 'month',
            indicatorDataVoList: allCountData,
          },
        ]);
      }
    });
  }, []);
  const exportFile = async () => {
      monthDataRef.current?.onClickDown();
  };
  const tabBarList = [
    {
      bar: '月度数据',
      flag: !monthData.length,
      content: (
        <MonthlyContent
          ref={monthDataRef}
          dataTable={monthData}
          dateType="month"
          type={typeSelect.value}
        />
      ),
      key: 'month',
    },
  ];

  return (
    <PageContainer
      header={{
        title: false,
        ghost: true,
        breadcrumb: (
          <Breadcrumb>
            <Breadcrumb.Item>
              <a href="/visualContainer">电网评价</a>
            </Breadcrumb.Item>
            <Breadcrumb.Item>评价对比</Breadcrumb.Item>
          </Breadcrumb>
        ),
        extra: [
          <Button
            className="right-title"
            type="primary"
            onClick={exportFile}
            icon={<DownloadOutlined />}
          >
            导出
          </Button>,
        ],
      }}
      className={styles['intelligence-visualization-container']}
    >
      <div className={styles['components-content-container']}>
        <div className={styles['result-tabs']}>
          {/* eslint-disable-next-line react/jsx-no-bind */}
          {/* <Tabs onChange={tabsCallback} activeKey={activeKey}>

          </Tabs> */}
          {tabBarList &&
            tabBarList.map((item) => {
              if (item.flag) {
                return null;
              }

              return (
                // <TabPane key={item.key} >
                <div>{item.content}</div>
                // </TabPane>
              );
            })}
          <SimpleSelect
            className={styles['felids-down']}
            defaultValue={typeList[0].name}
            getPopupContainer={(node) => node.parentNode}
            onChange={onTypeSelectChange}
            style={{ width: 150, marginRight: 10 }}
          >
            {typeList.map((item) => (
              <Select.Option key={item.id} value={item.name}>
                {item.name}
              </Select.Option>
            ))}
          </SimpleSelect>
        </div>
      </div>
    </PageContainer>
  );
}
