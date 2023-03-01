/* 常量map */
import  { DEVELOPMENT_URL } from '../../config/constants';

/* 运行时host */
export const serverUrl = IS_DEV ? DEVELOPMENT_URL : (SERVER_URL || '');

export const makeSelectOptions = (map: Record<HPJ.AverageClassification, string>) => Object.entries(map).map(([value, label]) => ({label, value}));

/* 项目-对比均值Map */
export const averageClassificationMap: Record<HPJ.AverageClassification, string> = {
  'classification': '同类均值',
  'company': '同公司均值',
  'operation_year': '同投运年份均值',
  'voltage_level': '同电压等级均值'
}

/* 项目-对比均值Selector options */
export const averageClassificationSelectorOptions = makeSelectOptions(averageClassificationMap);

/* 汇总-对比均值Map */
export const summaryAverageClassificationMap: Record<HPJ.AverageClassification, string> = {
  'classification': '工程分类',
  'company': '所属公司',
  'operation_year': '投运年份',
  'voltage_level': '电压等级'
}

/* 汇总-对比均值Selector options */
export const summaryAverageClassificationSelectorOptions = makeSelectOptions(summaryAverageClassificationMap);


/* 调色盘 */
export const colors = ['#11938C', '#4EB7E9', '#467DD2', '#AC327F', '#DE5353', '#DD8035', '#F5BC44', '#88DF78', '#28D89E'];
