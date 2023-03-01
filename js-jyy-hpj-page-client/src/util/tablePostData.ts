import { nanoid } from 'nanoid';

// 项目评价-建设过程
export const construction_process = (data: Record<string, any>[]) => {
  if (!data) return data;
  const result = Object.keys(data).map((name) => {
    if (!name) return name;

    // 第二层是数组时作为子表
    if (Array.isArray(data[name])) {
      const d = data[name].map((c: any) => ({...c, key: c?.name, data_raw_string: c?.data_raw ? JSON.stringify(c.data_raw, null, '\t') : c.data_raw}));
      return {
        key: name,
        name,
        children: d,
      }
    }

    // 第二层是对象时作为单行
    return {
      key: name,
      name,
      ...(data||{})
    }
  });

  return result;
}

// 项目评价-运营效果
export const operation_effect = (data: Record<string, any>[]) => {
  if (!data) return data;
  const result = Object.keys(data).map((name) => {
    if (!name) return name;

    // 第二层是数组时作为子表
    if (Array.isArray(data[name])) {
      const d = data[name]
        .map((c: any, i: number) => ({
          ...c,
          key: `${c.name}_${i}`,
          data_raw_string: c?.data_raw ? JSON.stringify(c.data_raw, null, '\t') : c.data_raw,
          hasChartData: c?.value_list?.length || c?.average_list?.length
        }));
      return {
        key: name,
        name,
        children: d,
      }
    }

    // 第二层是对象时作为单行
    return {
      key: name,
      name,
      ...(data[name]||{}),
      hasChartData: data[name]?.value_list?.length || data[name]?.average_list?.length,
      isSingle: true
    }
  });

  return result;
}

// 项目评价-投资管控
export const financial_benefits = (data: Record<string, any>[]) => {
  if (!data) return data;
  const result = Object.keys(data).map((name) => {
    if (!name) return name;

    // 第二层是数组时作为子表
    if (Array.isArray(data[name])) {
      const d = data[name]
        .map((c: any) => ({
          ...c,
          key: c?.name,
          data_raw_string: c?.data_raw ? JSON.stringify(c.data_raw, null, '\t') : c.data_raw,
          hasChartData: c?.value_list?.length || c?.average_list?.length
        }));
      return {
        key: name,
        name,
        children: d,
      }
    }

    // 第二层是对象时作为单行
    return {
      key: nanoid(),
      name,
      ...(data[name]||{}),
      hasChartData: data[name]?.value_list?.length || data[name]?.average_list?.length
    }
  });

  return result;
}
