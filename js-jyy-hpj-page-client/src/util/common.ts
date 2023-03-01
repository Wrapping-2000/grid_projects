import { generate } from 'shortid';
import download from './download';
import {httpExportDetailVisualExport} from '../services/visual';

/* 为列表成员添加指定属性 */
export const addListItemProp = (list: any, keyValue: Record<string, any>) => {
  if (!list) return list;
  if (list.length === 0) return [...list];
  return list.map((item: any) => (item ? { ...item, ...keyValue } : item));
};

/* 添加key */
export const addListKey = (list: any) => {
  if (!list) return list;
  if (list.length === 0) return [...list];
  return list.map((item: any) => (item ? { ...item, key: generate() } : item));
};

/* 表格表头 */
export const tableHanded = (dataHeadList: any) =>
  dataHeadList?.map(
    // eslint-disable-next-line max-len
    (item: any) =>
      item.indicatorDataVoList.map((it: any) => `${it.indicator}+${it.database}+${it.type}`),
  )[0];
/* 表格内容 */
export const dataFormatter = (dataContent: any[]) => {
  if (!dataContent) return null;
  const arrNew: any = [];
  const list: any = [];
  const order: any = [];
  const nations: any = dataContent?.map(
    // eslint-disable-next-line max-len
    (item) =>
      item?.indicatorDataVoList?.map((it: any) => `${it.indicator}+${it.database}+${it.type}`),
  )[0];
  const dataList = dataContent?.map((item) =>
    item?.indicatorDataVoList?.map((it: any) => it?.resultList?.map((i: any) => i)),
  );
  dataList?.map((nationData) =>
    nationData?.map((it: any, index: number) =>
      it?.map((c: any, ind: any) => arrNew.push({ ...c, name: nations[index], type: ind })),
    ),
  );
  arrNew?.forEach((item: any) => {
    if (order.indexOf(item.type) === -1) {
      list.push({
        order: item.type,
        goodsList: {},
      });
      order.push(item.type);
    }
  });

  list.forEach((item: any) => {
    arrNew.forEach((items: any) => {
      if (item.order === items.type) {
        const leyValue = items.name;
        const { value, time } = items;
        item.goodsList[leyValue] = value;
        item.goodsList.time = time;
      }
    });
  });
  return list.map((item: any) => item.goodsList);
};

/* 表格选取内容 */
export const chooseDataFormatter = (dataContent: any[]) => {
  if (!dataContent) return null;
  const arrNew: any = [];
  const list: any = [];
  const order: any = [];
  console.log(dataContent);
  const nations = dataContent?.map(
    // eslint-disable-next-line max-len
    (item) =>
      item?.indicatorDataVoList?.map((it: any) => `${it?.indicator}+${it?.database}+${it?.type}`),
  )[0];
  const dataList = dataContent?.map((item) =>
    item?.indicatorDataVoList?.map((it: any) => it?.resultList?.map((i: any) => i)),
  );
  dataList?.map((nationData) =>
    nationData?.map((it: any, index: any) =>
      it?.map((c: any, ind: any) => arrNew.push({ ...c, name: nations[index], type: ind })),
    ),
  );
  arrNew?.forEach((item: any) => {
    if (order.indexOf(item.type) === -1) {
      list.push({
        order: item.type,
        resultList: [],
      });
      order.push(item.type);
    }
  });
  list.forEach((item: any) => {
    arrNew.forEach((items: any) => {
      if (item.order === items.type) {
        const leyValue = items.name;
        const { value, time } = items;
        item.resultList.push({ name: leyValue, value });
        item.indicator = time;
      }
    });
  });
  return list;
};
// 频度转换
export const dateCheck = (data: any) => {
  if (data === 'month') {
    return '月度';
  }
  if (data === 'year') {
    return '年度';
  }
  if (data === 'quarter') {
    return '季度';
  }
  if (data === 'day') {
    return '日度';
  }
  return null;
};
// 图表下载
export const chartDown = async (chart: any, downData: any, editableStr: any) => {
  try{
    const baseData = chart.current.getDataURL({
      pixelRatio: 2,
      backgroundColor: 'black',
      excludeComponents: null,
    });
    const params = { base64String: baseData, resultList: downData.filter((item: any) =>  JSON.stringify(item) !== '{}') };

    const blob = await httpExportDetailVisualExport(params);
    const objectUrl = URL.createObjectURL(blob);
    download(objectUrl, `${editableStr}.xlsx`);
  } catch{
    console.error();

  }

};
