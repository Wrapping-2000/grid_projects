/* eslint-disable @typescript-eslint/no-unused-expressions */
import React, { useState, useEffect, forwardRef, useImperativeHandle, useMemo } from 'react';
import { generate as sid } from 'shortid';
import { Input, Menu, Checkbox, Card, Tooltip, Spin, Typography } from 'antd';
import _ from 'lodash';
// import {CheckboxChangeEvent} from 'antd/lib/checkbox';
import {
  httpGetAllSourceData,
  httpSearchKeyWords,
  httpGetIndicatorData,
} from '../../../../services/visual';
import HighLight from '../../../../components/highlight_text';
import getHighlight from '../../../../util/get-highlight';
import styles from '../visual-container.less';

const { Search } = Input;
const { SubMenu } = Menu;
const { Title } = Typography;

const InternationalEnergyComponent = forwardRef((props: any, ref): JSX.Element => {
  // 半选
  const [indeterminate, setIndeterminate] = useState<boolean>(false);
  // 选中数据
  const [lastAll, setLastAll] = useState([]);
  // loading
  const [loading, setLoading] = useState<boolean>(false);
  // 内层名称
  const [indicator, setIndicator] = useState<string>();

  // 选择框初始数据
  const [optionList, setOptionList] = useState([]);
  // 选中数据大集合
  const [checkedListAll, setCheckedListAll] = useState([]);
  // 单条id选中数据
  const [checkedList, setCheckedList] = useState(null);
  const [defaultKeys, setDefaultKeys] = useState([]);
  const [searchValue, setSearchValue] = useState('');
  // 列表 数据库 右侧展示
  const { indicatorList, database, JiangsuEconomicsList, setIndicatorList } = props;
  // 选中列表
  const [isKey, setIsKey] = useState('');

  const clickIndicator = (item, n, v) => {
    // 半选
    setIndeterminate(false);

    setIndicator(v.indicator);
    setLoading(true);
    // 下拉框数据
    httpGetAllSourceData({
      type: n.type.replace(/&_/g, '').replace(/_&/g, ''),
      indicator: v.indicator.replace(/&_/g, '').replace(/_&/g, ''),
    })
      .then((res1) => {
        if (res1) {
          const obj = {};
          const checkedMapListNewTwo = res1?.data?.map((items) => ({
            // items,
            checkAll: false,
            regions: items?.names?.map((it) => ({ label: it, value: it, check: false })),
          }));
          setIsKey(`${n?.type}+${v?.indicator}`);
          // 列表选中过滤单条数据
          const pitchOne = checkedListAll.filter((it) => it.isKey === `${n?.type}+${v?.indicator}`);
          const hierarchy = checkedListAll
            .map((itemIs) => itemIs.value.map((it) => it.regions))
            .flat(2)
            .filter((i) => i.check === true);
          const hierarchys = hierarchy.reduce((cur, next) => {
            obj[next.value] ? '' : (obj[next.value] = true && cur.push(next));
            return cur;
          }, []);
          const checkedMapListNewTwoList = checkedMapListNewTwo.map((items: any) => {
            return {
              ...items,
              regions: items?.regions.map((ite) => {
                return {
                  ...ite,
                  check: hierarchys.map((it) => it.value).includes(ite.value),
                };
              }),
            };
          });
          setLastAll(hierarchys);
          // 取单条数据
          setCheckedList(pitchOne[0]?.value || checkedMapListNewTwoList || []);
          setOptionList(checkedMapListNewTwoList);
        }
      })
      .finally(() => {
        setLoading(false);
      });
  };

  // 清空全部
  const onClickAllRef = () => {
    setCheckedList([]);
    setCheckedListAll([]);
  };
  // 删除单条
  const onClickRef = (deleteData) => {
    if (!deleteData) return;
    const newCheckedList = checkedListAll.map((item) => {
      console.log(item, deleteData, 'delete');
      // if (item?.isKey === `${deleteData?.type}+${deleteData?.indicator}`) {
      return {
        ...item,
        value: item.value.map((ite) => {
          if (ite?.period === deleteData?.period) {
            return {
              ...ite,
              regions: ite?.regions.map((it) => {
                if (it.value === deleteData.region) {
                  return {
                    ...it,
                    check: false,
                  };
                }
                return it;
              }),
            };
          }
          return ite;
        }),
      };
      // }
      // return item;
    });
    const pitchOne = newCheckedList.filter(
      (it) => it.isKey === `${deleteData?.type}+${deleteData?.indicator}`,
    );
    if (indicator === deleteData?.indicator) {
      setCheckedList(pitchOne[0]?.value || []);
    }
    setCheckedListAll(newCheckedList);
  };
  // 单个选中
  const onChange = (list, typeOne) => {
    console.log(
      list,
      typeOne.regions.map((item) => item.value),
      lastAll,
    );
    if (!list) return;
    const noList = typeOne.regions
      .map((itema) => {
        if (list.includes(itema.value)) return;
        return itema.value;
      })
      .filter((iteb) => iteb !== undefined);

    setLastAll(lastAll.filter((items) => noList.includes(items.value)));
    const newCheckedList = (
      JSON.stringify(checkedList) !== '[]' ? checkedList : null || optionList
    ).map((i) => {
      // if (i?.period === typeOne) {
      return {
        ...i,
        regions: i.regions.map((c) => ({
          ...c,
          check: list.includes(c.label),
        })),
      };
      // }
      // return i;
    });
    setCheckedList(newCheckedList);
    const pitchAll = _.unionBy([{ isKey, value: newCheckedList }], checkedListAll, 'isKey');

    const pitchAlls = pitchAll.map((item) => {
      return {
        ...item,
        value: item.value.map((ite) => {
          return {
            ...ite,
            regions: ite?.regions.map((it) => {
              if (noList.includes(it.value)) {
                return {
                  ...it,
                  check: false,
                };
              }
              if (list.includes(it.value)) {
                return {
                  ...it,
                  check: true,
                };
              }
              return it;
            }),
          };
        }),
      };
    });
    setCheckedListAll(pitchAlls);
  };
  // 全选
  const onCheckAllChange = (e: CheckboxChangeEvent, typeAll: any) => {
    const newCheckedList = (
      JSON.stringify(checkedList) !== '[]' ? checkedList : null || optionList
    ).map((i) => {
      if (i?.period === typeAll) {
        return {
          ...i,
          checkAll: e.target.checked,
          regions: i.regions.map((c) => ({
            ...c,
            check: e.target.checked,
          })),
        };
      }
      return i;
    });
    setCheckedList(newCheckedList);
    const pitchAll = _.unionBy([{ isKey, value: newCheckedList }], checkedListAll, 'isKey');
    setCheckedListAll(pitchAll);
  };
  // 状态改变
  useEffect(() => {
    const checkedListAlls = checkedListAll.map((item) =>
      item?.value?.map((it) =>
        it?.regions.map((i) => {
          if (i.check) {
            return {
              region: i.value,
              type: item.isKey.split('+')[0],
              indicator: item.isKey.split('+')[1],
              period: it.period,
              source: item.isKey.split('+')[2],
              database,
            };
          }
          return null;
        }),
      ),
    );
    JiangsuEconomicsList(checkedListAlls.flat(2).filter((item) => item !== null));
  }, [checkedListAll]);

  const search = (value, event) => {
    if (event.nativeEvent.type === 'click' && value === '') {
      httpGetIndicatorData(database).then((res) => {
        if (res) {
          const dataList = res.data.map((item) => ({
            type: item.type,
            indicators: item.indicators.map((it) => ({ ...it, id: sid() })),
          }));
          setDefaultKeys([]);
          setIndicatorList(dataList);
        }
      });
    } else {
      httpSearchKeyWords(value).then((res) => {
        if (res?.code === 'SUCCESS') {
          const dataList = res?.data.map((item) => ({
            type: item.type,
            indicators: item.indicators.map((it) => ({
              ...it,
              indicator: it.indicator,
              id: sid(),
            })),
          }));
          console.log(dataList);

          const menuKeyList = dataList.map((item) => item.type);

          setDefaultKeys(menuKeyList);
          setIndicatorList(dataList);
        }
      });
    }
  };

  const clickMenuItem = (item) => {
    setDefaultKeys(item);
  };

  const newIndicatorList = useMemo(() => {
    const list = indicatorList?.map((item) => ({
      ...item,
      formattedTypeData: item.type.replace(/&_/g, '').replace(/_&/g, ''),
      typeHighlight: getHighlight(item.type),
      indicators: item.indicators?.map((it) => ({
        ...it,
        id: sid(),
        formattedIndicatorData: it.indicator.replace(/&_/g, '').replace(/_&/g, ''),
        indicatorHighlight: getHighlight(it.indicator),
      })),
    }));
    return list;
  }, [indicatorList]);
  // 方法传递给父组件
  useImperativeHandle(ref, () => ({
    onClickRef,
    onClickAllRef,
    setSearchValue,
  }));
  return (
    <div className={styles['china-economy-container']}>
      <div className={styles['box-left']}>
        <div className={styles['china-economy-title']}>
          {/* <span style={{f}}>指标列表</span> */}
          <Title level={5}>指标列表</Title>
        </div>
        <div className={styles['china-economy-search']}>
          <Search
            allowClear
            style={{ marginBottom: 8 }}
            onSearch={search}
            value={searchValue}
            onChange={(e) => {
              setSearchValue(e.target.value);
            }}
            placeholder="搜索指标类型或指标名称"
          />
          <div className={styles['china-menu-wrap']}>
            <div className={styles['china-menu-box']}>
              <Menu mode="inline" openKeys={defaultKeys} onOpenChange={clickMenuItem}>
                {newIndicatorList?.map((n) => {
                  const { formattedTypeData, typeHighlight } = n;
                  return (
                    <SubMenu
                      key={n.type}
                      style={{ fontWeight: 800 }}
                      title={<HighLight content={formattedTypeData} keyword={typeHighlight} />}
                    >
                      {n.indicators.map((v: any) => {
                        const { formattedIndicatorData, indicatorHighlight } = v;
                        return (
                          <Menu.Item
                            style={{ fontWeight: 400,paddingTop: 10 }}
                            key={v.indicator + n.type}
                            onClick={(item: any) => {
                              clickIndicator(item, n, v);
                            }}
                          >
                            <Tooltip placement="topLeft" title={v.indicatorTranslation}>
                              <div className={styles['item-div']}>
                                {formattedIndicatorData ? (
                                  <HighLight
                                    content={formattedIndicatorData}
                                    keyword={indicatorHighlight}
                                  />
                                ) : (
                                  v.indicator
                                )}
                              </div>
                            </Tooltip>
                          </Menu.Item>
                        );
                      })}
                    </SubMenu>
                  );
                })}
              </Menu>
            </div>
          </div>
        </div>
      </div>
      <div className={styles['box-right']}>
        <div className={styles['china-economy-title']}>
          {/* <b>指标选项</b> */}
          <Title level={5}>指标选项</Title>
        </div>
        <div className={styles['right-container']}>
          <Spin tip="Loading..." spinning={loading}>
            <div className={styles['index-content']}>
              <>
                {(JSON.stringify(checkedList) !== '[]' ? checkedList : null || optionList) ? (
                  (JSON.stringify(checkedList) !== '[]' ? checkedList : null || optionList)?.map(
                    (item) => (
                      <Card
                        style={{ flex: 1, fontWeight: 500, color: 'rgba(0,0,0,0.65)' }}
                        title={
                          <div
                            style={{
                              display: 'flex',
                              justifyContent: 'space-between',
                              width: '100%',
                              fontSize: 16,
                              alignItems: 'center',
                            }}
                          >
                            {indicator && (
                              <span>{indicator.replace(/&_/g, '').replace(/_&/g, '')}</span>
                            )}
                            <Checkbox
                              indeterminate={indeterminate}
                              style={{color: '#1890FF'}}
                              checked={item?.regions?.every((it) => it.check)}
                              onChange={(e) => onCheckAllChange(e, item.period)}
                              onClick={(e) => {
                                e.stopPropagation();
                              }}
                            >
                              全选
                              </Checkbox>
                          </div>
                        }
                        bordered={false}
                      >
                        <Checkbox.Group
                          options={item.regions}
                          value={item?.regions?.map((it) => it.check && it.label)}
                          onChange={(e) => onChange(e, item)}
                        />
                      </Card>
                    ),
                  )
                ) : (
                  <div style={{ margin: 'auto', marginTop: '50%' }}>请先在左侧指标列表中选择指标</div>
                )}
              </>
            </div>
          </Spin>
        </div>
      </div>
    </div>
  );
});

export default InternationalEnergyComponent;
