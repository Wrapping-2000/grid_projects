/* 建设过程、运营效果、投资管控所有下拉选择数据 */
import React from 'react';
import { averageClassificationSelectorOptions,  } from '@/util/constants';
import { getProjectEvaluateOperationEffectTypes } from '@/services/main';
import moment from 'moment';

export type  OptionLabels=
  'construction_process_average'|
  'operation_effect_type'|
  'operation_effect_year'|
  'operation_effect_average'|
  'financial_benefits_year'|
  'financial_benefits_average';

export default (props: {
  wbsCode?: string
}) => {
  //const { wbsCode } = props;
  const [data, setData] = React.useState<
    Record<
      OptionLabels, {
        label: string;
        value: string;
      }|undefined>
    >({
      construction_process_average: averageClassificationSelectorOptions[0],
      operation_effect_type: undefined,
      operation_effect_year: undefined,
      operation_effect_average: averageClassificationSelectorOptions[0],
      financial_benefits_year: undefined,
      financial_benefits_average: averageClassificationSelectorOptions[0],
    });

  const [options, setOptions] = React.useState<
    Record<
      OptionLabels, {
        label: string;
        value: string;
      }[]>
  >({
      construction_process_average: averageClassificationSelectorOptions,
      operation_effect_type: [],
      operation_effect_year: [],
      operation_effect_average: averageClassificationSelectorOptions,
      financial_benefits_year: [],
      financial_benefits_average: averageClassificationSelectorOptions,
    });

  const handleChange = (name: string) => (v: any) => {
    console.log(name, 'handleChange', v)
    // 年份的转一次
    const finalValue = name.endsWith('_year') ? {value: (v || moment()).format('YYYY')} : v;
    setData((d) => {
      return {
        ...d,
        [name]: finalValue
      }
    })
  }

  React.useEffect(() => {
    (async() => {
      // 获取可选年
      Promise.all([/* getProjectEvaluateYears(wbsCode),  */getProjectEvaluateOperationEffectTypes()])
        .then(([typesRes]) => {
          if (typesRes?.code === 'SUCCESS') {
            // const yearsOptions = (yearsRes.data||[]).map(y => ({label: y, value: y}));
            const typesOptions = (typesRes.data||[]).map(t => ({label: t?.cn, value: t?.en}));
            console.log(typesOptions, 'typesOptions')
            setOptions(ops => {
              return {
                ...ops,
                operation_effect_type: typesOptions,
                // operation_effect_year: yearsOptions,
                // financial_benefits_year: yearsOptions,
              }
            })
            setData((currentData: typeof data) => ({
              ...currentData,
              operation_effect_type: typesOptions[0],
              // operation_effect_year: yearsOptions[0],
              // financial_benefits_year: yearsOptions[0],
            }))
          }
        })
        .catch(console.error)
    })();
  }, [])

  return {
    handleChange,
    options,
    values: data,
  }
}
