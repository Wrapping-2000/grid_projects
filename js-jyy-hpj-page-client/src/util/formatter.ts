import uniqWith from 'lodash/uniqWith';

/* 项目列表formatter */
export const projectListFormatter = (request: (params: any) => Promise<Record<string, any>>) =>
  async (...p: Record<string, any>[]) => {
    // @ts-ignore
    const res = await request(...p).catch(console.error);
    if (!res) return res;
    return ({
      code: res.code,
      data: res.data?.projects,
      total: res.data?.total,
    })
  }

  /* excel列表formatter */
export const excelListFormatter = (request: (params: any) => Promise<Record<string, any>>) =>
  async (...p: Record<string, any>[]) => {
    // @ts-ignore
    const res = await request(...p).catch(console.error);
    if (!res) return res;
    return ({
      code: res.code,
      data: res.data?.excels,
      total: res.data?.total,
    })
  }

/* 汇总树数据 */
const typeMap: Record<string, HPJ.SummaryChartList> = {
  1: [],
  2: ['bar', 'line'],
  3: ['bar', 'line', 'pie']
}

export const summaryTreeFormatter = (data: Record<string, any>): [Record<string, any>[], Record<string, HPJ.SummaryChartList>] | [] => {
  if (!data) return [];

  // 每一个指标显示类型的map
  const map = {} as Record<string, HPJ.SummaryChartList>;

  // 遍历子集
  const result = Object.entries(data)
    .map(([key, children]) => {
      // 还有下级的情况
      const childrenEntries = Object.entries(children);

      const getChildren = (chl: Record<string, any>[] | null) => {
        if (!Array.isArray(chl)) return null;
        return chl.map((n) => {
          const {name, show_type} = n || {};
          if (name) {
            map[name] = typeMap[show_type];
          }
          return ({title: name, key: name})
        });
      }

      if (Array.isArray(childrenEntries)) {
        return {
          key,
          title: key,
          children: childrenEntries.map(([title, chl]) => {
            const c = getChildren(chl as Record<string, any>[] | null);
            // TODO：去重应在服务端
            const uniqChildren = uniqWith(c, (a, b) => {
              return a?.title === b?.title
            })

            return ({
              title,
              key: title,
              children: uniqChildren
            })
          })
        };
      }

      // 没有下级的情况
      return {
        key,
        title: key,
      };
    })
  return [result, map];
}

/* 汇总评价数据 */
export const summaryDataFormatter = (data: Record<string, any>) => {
  if (!data) return null;

  // const dataSource = uniqWith(data?.data_source || [], (a: Record<string, any>, b: Record<string, any>) => {
  //   return a?.wbs_code === b?.wbs_code
  // }).map((item) => ({...item||{}, status: {status_msg: item?.status_msg, status: item?.status}}))
  const dataSource = (data?.data_source || []).map((item: { status_msg: any; status: any; }) => ({...item||{}, status: {status_msg: item?.status_msg, status: item?.status}}))
  return {
    columns: data?.columns,
    dataSource,
    total: data?.total
  }
}

/* 汇总评价图表数据 */
export const summaryChartsDataFormatter = (data: Record<string, any>) => {
  if (!data) return [];
  // 是否连续数据
  const isContinuousValues = !!data?.[0].year;

  // 数据
  const dataSource = isContinuousValues ? (
    data?.map((d: any) => {
      const valuesMap = {};
      (d?.value||[]).forEach((v: Record<string, string>) => valuesMap[v?.name] = v?.value)
      return {
        year: d?.year,
        ...valuesMap
      }
    })
   ) : data/* data?.map((d: any) => d?.value) */;

  // xAxis
  const xAxis = isContinuousValues ? data?.map((d: any) => d?.year) : data?.map((d: any) => d?.name);

  // console.log(data, '汇总评价图表数据')
  return {
    xAxis,
    data: dataSource,
    isContinuousValues
  }
}

/* 汇总饼图表数据 */
export const summaryPieDataFormatter = (data: Record<string, any>) => {
  if (!data) return [];
  // const total = data.reduce((prev: Record<string, any>, next: Record<string, any>) => {
  //   return (prev?.count || 0) + (next?.count || 0)
  // })
  return data.map((item: Record<string, any>) => {
    const {start, end, count} = item || {};
    return {
      ...(item||{}),
      name: `${start} ~ ${end}`,
      value: count
      // value: ((count||0) / total).toFixed(2)
    };
  })
}

/* valueEnum的转换 */
export const valueEnumFormatter = (data: string[]) => {
  if (!data) return [];
  const res: Record<string, string> = {}
  data.forEach((item: string) => {
    res[item] = item;
  })
  return res;
}

