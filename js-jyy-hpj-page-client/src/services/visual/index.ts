// @ts-ignore
/* eslint-disable */
import { request } from 'umi';

/** 登录 GET /api/currentUser */
export async function login(
  data: { user_name: string; password: string },
  options?: { [key: string]: any },
) {
  return request<{
    data: API.CurrentUser;
  }>('/auth/login', {
    method: 'POST',
    data,
    ...(options || {}),
  });
}

/** 获取项目详情 */
export async function httpGetIndicatorData(value: string): Promise<any> {
  // return mock.dataChart;
  return request(`/comment/menu?name=${value}`);
}

/* 专业数据-分类检索 查询地区，频度数据 */
export const httpGetRegionAndPeriodData = (): Promise<any> => {
  return request('/stats/queryRegionAndPeriod', {
    method: 'POST',
  });
};

/* 专业数据-分类检索 查询所有分类数据 */
export async function httpGetAllClassificationData(value: Array<string>): Promise<any> {
  console.log(JSON.stringify(value), value);
  return request(`/comment/green/generate/detail?name_list=${JSON.stringify(value)}`);
}
/* 专业数据-分类检索 查询指标下所有数据来源 */
export const httpGetAllSourceData = (value: { type: string; indicator: string }): Promise<any> => {
  return request(`/comment/power/names?type=${value?.type}&indicator=${value?.indicator}`);
};
/* 专业数据-分类检索 导出详细信息 */
export const httpExportDetailInformation = (): Promise<any> => {
  return request('/stats/complexExport', {
    method: 'POST',
    responseType: 'blob',
  });
};

/* 专业数据-分类检索  查询关键词 */
export const httpSearchKeyWords = (value: any): Promise<any> => {
  return request(`/comment/power/names/search?indicator=${value}`);
};

/* 专业数据-分类检索  指标弹窗 */
export const httpIndicatorModal = (): Promise<any> => {
  return request('/stats/queryDescription', {
    method: 'POST',
  });
};

/* 数据可视化 导出详细信息 */
export const httpExportDetailVisualExport = (params: { base64String: any; resultList: any; }) => {
  return request(`/comment/download`, {
    method: 'POST',
    responseType: 'blob',
    data: params
  });
};

/** 获取项目列表 */
export async function getAllList(options: { pageSize: number; current: number; [key: string]: any }) {
  const {
    operation_year
  } = options;

  const params: Partial<typeof options> = {
    ...options,
  }

  // 处理时间戳
  if (operation_year) {
    params.operation_year = new Date(operation_year).getFullYear()
  }

  return request<{
    code: string,
    data: API.ProjectList;
  }>('/project/list', {
    params,
    method: 'GET',
    // ...(options || {}),
  });
}

/* 数据源 - 获取excel信息 */
export const httpGetExcelInfo = (name:string): Promise<any> => {
    return request(`/excel/get_excel?name=${name}`, {
      method: 'GET',
    });
};

/* 数据源 - 获取excel列表 */
export async function httpGetExcelList(options: { pageSize: number; current: number; [key: string]: any }) {
  const params: Partial<typeof options> = {
    ...options,
  }
  return request<{
    code: string,
    data: API.ExcelList;
  }>('/excel/get_excel_list', {
    params,
    method: 'GET',
    ...(options || {}),
  });
}

/*数据源 - 删除excel表 */
export async function httpDeleteExcel(excelName?: API.Excel['name'], options?: { [key: string]: any }) {
  return request<{
    code: string,
    data: API.Excel;
  }>(`/excel/${excelName}`, {
    method: 'DELETE',
    ...(options || {}),
  });
}

/*数据源 - 保存右侧展示excel修改后的数据 */
export const httpSaveRow = (excelName: string, rowKey: string, newValue: string | undefined): Promise<any> => {
      return request(`/excel/save_row?excelName=${excelName}&rowKey=${rowKey}&newValue=${newValue}`, {
      method: 'POST',
    });
};

/*数据源 - 删除右侧展示excel的某一行 */
export const httpDelRow = (excelName: string, rowKey: string): Promise<any> => {
    return request(`/excel/del_row?excelName=${excelName}&rowKey=${rowKey}`, {
      method: 'DELETE',
    });
};

/*数据源 - 创建新的一行需要的rowKey */
export const httpGetNewRowKey = (excelName: string): Promise<any> => {
    return request(`/excel/del_row?excelName=${excelName}`, {
      method: 'POST',
    });
};
