/* eslint-disable @typescript-eslint/no-unused-expressions */
import React, { useState, useEffect, useRef } from 'react';
import { Tabs, Button, notification, Typography } from 'antd';
import { useHistory } from 'umi';
import { generate as sid } from 'shortid';
import { PageContainer } from '@ant-design/pro-layout';
import { httpGetIndicatorData } from '@/services/visual';
import JiangsuEconomyComponent from './components';
import styles from './visual-container.less';

enum DatabaseType {
  internationalEnergy = '绿色清洁',
  chinaEconomy = '灵活智能',
  chinaEnergy = '安全运行',
  jiangsuEconomy = '经济高效',
}

const { TabPane } = Tabs;
const { Title } = Typography;

function IndexSelectionContainer(): JSX.Element {
  const internationalRef = useRef<any>(null);
  const chinaEconomicsRef = useRef<any>(null);
  const chinaEnergyRef = useRef<any>(null);
  const JiangsuEconomicsRef = useRef<any>(null);
  const JiangsuEnergyRef = useRef<any>(null);
  const history = useHistory<any>();
  // 国际数据
  const [international, setInternational] = useState([]);
  // 中国经济
  const [chinaEconomics, setChinaEconomics] = useState([]);

  // 中国能源
  const [chinaEnergy, setChinaEnergy] = useState([]);

  // 江苏经济
  const [JiangsuEconomics, setJiangsuEconomics] = useState([]);

  // // 江苏能源
  // const [JiangsuEnergy, setJiangsuEnergy] = useState([]);

  // 共计
  const [normList, setNormList] = useState([]);
  const [database, setDatabase] = useState(history.location.state?.database);
  const [indicatorList, setIndicatorList] = useState([]);
  // 国际数据
  const internationalList = (list) => {
    setInternational(list.filter((item) => item !== null));
  };
  // 中国经济
  const chinaEconomicsList = (list) => {
    setChinaEconomics(list.filter((item) => item !== null));
  };

  // 中国能源
  const chinaEnergyList = (list) => {
    setChinaEnergy(list.filter((item) => item !== null));
  };
  // 江苏经济
  const JiangsuEconomicsList = (list) => {
    setJiangsuEconomics(list);
  };

  const queryIndex = () => {
    history.push({
      pathname: '/visualResult/list',
      state: { value: normList.map((item) => item.region) },
    });
  };

  useEffect(() => {
    httpGetIndicatorData(DatabaseType.internationalEnergy).then((res) => {
      console.log(res);
      if (res) {
        const dataList = res.data.map((item) => ({
          type: item.type,
          indicators: item.indicators.map((it) => ({ ...it, id: sid() })),
        }));
        setIndicatorList(dataList);
      }
    });
  }, []);

  const openNotificationWithIcon = () => {
    notification.error({
      message: '最多可选15条',
    });
  };
  const debounceSetClientSize = React.useMemo(() => openNotificationWithIcon, []);
  useEffect(() => {
    if (normList.length > 15) {
      debounceSetClientSize();
    }
  }, [debounceSetClientSize, normList]);
  const changeTabs = (key) => {
    if (key === DatabaseType.internationalEnergy) {
      httpGetIndicatorData(DatabaseType.internationalEnergy).then((res) => {
        if (res) {
          const dataList = res.data.map((item) => ({
            type: item.type,
            indicators: item.indicators.map((it) => ({ ...it, id: sid() })),
          }));
          setIndicatorList(dataList);
        }
      });
    }
    if (key === DatabaseType.chinaEconomy) {
      httpGetIndicatorData(DatabaseType.chinaEconomy).then((res) => {
        if (res) {
          const dataList = res.data.map((item) => ({
            type: item.type,
            indicators: item.indicators.map((it) => ({ ...it, id: sid() })),
          }));
          setIndicatorList(dataList);
        }
        console.log(res);
      });
    }
    if (key === DatabaseType.chinaEnergy) {
      httpGetIndicatorData(DatabaseType.chinaEnergy).then((res) => {
        if (res) {
          const dataList = res.data.map((item) => ({
            type: item.type,
            indicators: item.indicators.map((it) => ({ ...it, id: sid() })),
          }));
          setIndicatorList(dataList);
        }
      });
    }
    if (key === DatabaseType.jiangsuEconomy) {
      httpGetIndicatorData(DatabaseType.jiangsuEconomy).then((res) => {
        if (res) {
          const dataList = res.data.map((item) => ({
            type: item.type,
            indicators: item.indicators.map((it) => ({ ...it, id: sid() })),
          }));
          setIndicatorList(dataList);
        }
      });
    }
    // if (key === DatabaseType.jiangsuEnergy) {
    //   // httpGetIndicatorData(DatabaseType.jiangsuEnergy).then((res) => {
    //   //   if (res?.flag) {
    //   //     const dataList = res.data.map((item) => ({
    //   //       type: item.type,
    //   //       indicators: item.indicators.map((it) => ({...it, id: sid()})),
    //   //     }));
    //   //     setIndicatorList(dataList);
    //   //   }
    //   // });
    // }
    setDatabase(key);
    internationalRef.current?.setSearchValue('');
    chinaEconomicsRef.current?.setSearchValue('');
    chinaEnergyRef.current?.setSearchValue('');
    JiangsuEconomicsRef.current?.setSearchValue('');
    JiangsuEnergyRef.current?.setSearchValue('');
  };

  const tabBarList = [
    {
      key: DatabaseType.internationalEnergy,
      component: (
        <JiangsuEconomyComponent
          ref={internationalRef}
          indicatorList={indicatorList}
          database={DatabaseType.internationalEnergy}
          JiangsuEconomicsList={internationalList}
          setIndicatorList={setIndicatorList}
        />
      ),
    },
    {
      key: DatabaseType.chinaEconomy,
      component: (
        <JiangsuEconomyComponent
          ref={chinaEconomicsRef}
          indicatorList={indicatorList}
          database={DatabaseType.chinaEconomy}
          JiangsuEconomicsList={chinaEconomicsList}
          setIndicatorList={setIndicatorList}
        />
      ),
    },
    {
      key: DatabaseType.chinaEnergy,
      component: (
        <JiangsuEconomyComponent
          ref={chinaEnergyRef}
          indicatorList={indicatorList}
          database={DatabaseType.chinaEnergy}
          JiangsuEconomicsList={chinaEnergyList}
          setIndicatorList={setIndicatorList}
        />
      ),
    },
    {
      key: DatabaseType.jiangsuEconomy,
      component: (
        <JiangsuEconomyComponent
          ref={JiangsuEconomicsRef}
          indicatorList={indicatorList}
          database={DatabaseType.jiangsuEconomy}
          JiangsuEconomicsList={JiangsuEconomicsList}
          setIndicatorList={setIndicatorList}
        />
      ),
    },
    // {
    //   key: DatabaseType.jiangsuEnergy,
    //   label: 'economics',
    //   component: (
    //     <JiangsuEconomyComponent
    //       ref={JiangsuEnergyRef}
    //       indicatorList={indicatorList}
    //       database={DatabaseType.jiangsuEnergy}
    //       JiangsuEconomicsList={JiangsuEnergyList}
    //       setIndicatorList={setIndicatorList}
    //     />
    //   ),
    // },
  ];

  // 删除单挑
  const deleteList = (value, type) => {
    if (type === DatabaseType.internationalEnergy) {
      internationalRef.current.onClickRef(value);
    }
    if (type === DatabaseType.chinaEconomy) {
      chinaEconomicsRef.current.onClickRef(value);
    }
    if (type === DatabaseType.chinaEnergy) {
      chinaEnergyRef.current.onClickRef(value);
    }
    if (type === DatabaseType.jiangsuEconomy) {
      JiangsuEconomicsRef.current.onClickRef(value);
    }
    // if (type === DatabaseType.jiangsuEnergy) {
    //   JiangsuEnergyRef.current.onClickRef(value);
    // }
  };
  // 删除所有
  const deleteListAll = () => {
    internationalRef.current?.onClickAllRef();
    chinaEconomicsRef.current?.onClickAllRef();
    chinaEnergyRef.current?.onClickAllRef();
    JiangsuEconomicsRef.current?.onClickAllRef();
    JiangsuEnergyRef.current?.onClickAllRef();
  };
  const rightData = [
    {
      value: international,
      name: DatabaseType.internationalEnergy,
    },
    {
      value: chinaEconomics,
      name: DatabaseType.chinaEconomy,
    },
    {
      value: chinaEnergy,
      name: DatabaseType.chinaEnergy,
    },
    {
      value: JiangsuEconomics,
      name: DatabaseType.jiangsuEconomy,
    },
    // {
    //   value: JiangsuEnergy,
    //   name: DatabaseType.jiangsuEnergy,
    // },
  ];
  const obj = {};
  console.log(rightData);
  const rightDataFormat = rightData.map((item) => {
    return {
      ...item,
      value: item?.value?.reduce((cur, next) => {
        obj[next.region] ? '' : (obj[next.region] = true && cur.push(next));
        return cur;
      }, []),
    };
  });
  useEffect(() => {
    setNormList(rightDataFormat.map((item) => item.value).flat(2));
  }, [international, chinaEconomics, chinaEnergy, JiangsuEconomics]);
  console.log(normList.length)
  return (
    <PageContainer
      header={{
        title: '电网评价',
        ghost: true,
        extra: [
          <Button onClick={queryIndex} type="primary" disabled={normList.length < 1 || normList.length > 15}>
            生成图表
          </Button>,
        ],
      }}
    >
      <div className={styles['index-selection-content']}>
        <div className={styles['index-selection-left']}>
          <Tabs defaultActiveKey={database} onChange={changeTabs}>
            {tabBarList.map((item) => (
              <TabPane
                tab={<span style={{fontSize: 14, fontWeight: 600}}>{item.key}</span>}
                disabled={[DatabaseType.chinaEnergy, DatabaseType.jiangsuEconomy].includes(
                  item.key,
                )}
                key={item.key}
              >
                {item.component}
              </TabPane>
            ))}
          </Tabs>
        </div>
        <div className={styles['index-selection-right']}>
          <div className={styles['selection-title']}>
            {/* <b
              className={styles['selection-b']}
            >{`已选择指标  ${normList.length}条 (最多可选15条)`}</b> */}
            <Title level={5}>{`已选择指标(${normList.length}/15条)`}</Title>
            <Button type="link" disabled={normList.length < 1} style={{ fontSize: 16 }} onClick={() => deleteListAll()}>
              清空
            </Button>
          </div>
          <div className={styles['selection-container']}>
            {rightDataFormat.map((items) =>
              items.value?.map((item) => (
                <div
                  className={styles['selection-box']}
                  key={item?.indicator + item?.region + item?.source}
                >
                  {item?.indicator && (
                    <div className={styles['selection-all']}>
                      <div
                        className={styles['selection-delete']}
                        onKeyPress={undefined}
                        role="button"
                        tabIndex={0}
                        onClick={() => deleteList(item, items.name)}
                      >
                        X
                      </div>
                      <div>{item?.region}</div>
                    </div>
                  )}
                </div>
              )),
            )}
          </div>
        </div>
      </div>
    </PageContainer>
  );
}

export default IndexSelectionContainer;
