// @ts-ignore
/* eslint-disable */
import { request } from 'umi';

/** 登录 GET /api/currentUser */
export async function login(data: {user_name: string, password: string}, options?: { [key: string]: any }) {
  return request<{
    code: string,
    data: Record<string, any>;
  }>('/auth/login', {
    method: 'POST',
    data,
    ...(options || {}),
  });
}

/** 获取当前用户信息 */
export async function queryCurrentUser() {
  return request<{
    code: string,
    data: Record<string, any>;
  }>('/auth/current_user', {
    method: 'GET',
  });
}

/** 登出 GET /api/currentUser */
export async function outLogin(options?: { [key: string]: any }) {
  return request<{
    code: string,
    data: Record<string, any>;
  }>('/auth/logout', {
    method: 'GET',
    ...(options || {}),
  });
}

/** 注册 GET /api/currentUser */
export async function register(options?: { [key: string]: any }) {
  return request<{
    code: string,
    data: Record<string, any>;
  }>('/auth/register', {
    method: 'GET',
    ...(options || {}),
  });
}

/** 项目用到的枚举字段 */
export async function getDicts(options?: { [key: string]: any }) {
  return request<{
    code: string,
    data: API.Dicts;
  }>('/project/aggregation_filed', {
    method: 'GET',
    ...(options || {}),
  });
}

/** 获取项目列表 */
export async function getProjectList(options: { pageSize: number; current: number; [key: string]: any }) {
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

/** 获取项目详情 */
export async function getProjectDetail(wbsCode?: API.Project['wbs_code'], options?: { [key: string]: any }) {
  return request<{
    code: string,
    data: {
      data_source: API.ProjectDetail
      columns: API.ProjectDetail
    };
  }>(`/project/${wbsCode}`, {
    method: 'GET',
    ...(options || {}),
  });
}

/** 更新项目列表 */
export async function putProjectDetail(data?: {
  wbs_code?: API.Project['wbs_code'];
  [key: string]: any ;
}|null) {
  if (!data?.wbs_code) {
    return
  }
  const wbsCode = data.wbs_code;
  delete data.wbs_code;
  return request<{
    code: string,
    data: API.Project;
  }>(`/project/${wbsCode}`, {
    method: 'PUT',
    data
  });
}

/** 删除项目列表（评价也删除） */
export async function deleteProjectDetail(wbsCode?: API.Project['wbs_code'], options?: { [key: string]: any }) {
  return request<{
    code: string,
    data: API.Project;
  }>(`/project/${wbsCode}`, {
    method: 'DELETE',
    ...(options || {}),
  });
}

/** 获取项目指标信息 */ // 废弃
export async function getProjectEvaluateData(options?: {
  wbsCode: API.Project['wbs_code'],
  primaryIndex: HPJ.ProjectEvaluateType,
  [key: string]: any
}) {
  if (!options) return
  const {wbsCode, primaryIndex} = options;
  return request<{
    code: string,
    data: API.Project;
  }>(`/project/${wbsCode}/target/${primaryIndex}`, {
    method: 'GET',
    ...(options || {}),
  });
}

/** 获取项目建设过程评价表格信息 */
export async function getProjectEvaluateConstructionProcess(options?: Record<string, any>) {
  if (!options) return
  const {wbsCode, construction_process_average} = options;
  return request<{
    code: string,
    data: API.Project;
  }>(`/project/target/${wbsCode}/construction_process/${construction_process_average}`, {
    method: 'GET',
  });
}

/** 获取项目运行效果表格信息 */
export async function getProjectEvaluateOperationEffect(options?: Record<string, any>) {
  if (!options) return
  const {wbsCode, operation_effect_type, operation_effect_average, operation_effect_year} = options;

  return request<{
    code: string,
    data: API.Project;
  }>(`/project/target/${wbsCode}/operation_effect/${operation_effect_type}/${operation_effect_average}`, {
    method: 'GET',
    params: {
      year: operation_effect_year
    }
  });
}

/** 获取项目投资管控表格信息 */
export async function getProjectEvaluateFinancialBenefits(options?: Record<string, any>) {
  if (!options) return
  const {wbsCode, financial_benefits_average, financial_benefits_year} = options;
  console.log(options, 'optionsssss')

  return request<{
    code: string,
    data: API.Project;
  }>(`/project/target/${wbsCode}/financial_benefits/${financial_benefits_average}`, {
    method: 'GET',
    params: {
      year: financial_benefits_year
    }
  });
}

/** 获取项目评价下拉年份 */
export async function getProjectEvaluateYears(wbsCode?: string) {
  return request<{
    code: string;
    data: (string)[];
  }>(`/project/target/${wbsCode}/year`, {
    method: 'GET',
  });
}


/** 获取项目评价-运行效果的下拉指标 */
export async function getProjectEvaluateOperationEffectTypes(options?: Record<string, string>) {
  return request<{
    code: string;
    data: {en: string, cn: string}[];
  }>(`/project/target/operation_effect/primary_index`, {
    method: 'GET',
  });
}

/** 获取汇总评价-树状目录 */
export async function getSummaryTree(type: HPJ.SummaryEvaluateType, params?: {search: string}) {
  if (!type) return;
  return request<{
    code: string;
    data: Record<string, any>;
  }>(`/target/list/${type}`, {
    method: 'GET',
    params
  });
}

/** 获取汇总评价-表头类型 */
export async function getSummaryDataType(name: HPJ.SummaryEvaluateType, params?: Record<string, any>) {
  if (!name) return;
  return request<{
    code: string;
    data: Record<string, any>;
  }>(`/target/${name}`, {
    method: 'GET',
    params
  });
}

/** 获取汇总评价-表格数据 */
export async function getSummaryData(params: {
  name: string; // 指标名
  contrast_filed?: string; // 分类、公司、电压等级、操作年
  project_name?: string;
  contrast_value?: string; // （单值）单个柱状图
  target_year?: string; // （连续值）单个柱状图年
} & Record<string, any>, options: Record<string, any>) {
  if (!params?.name) return;
  // TODO: j检查错误
  if (params?.operation_year) {
    params.operation_year = new Date(params?.operation_year).getFullYear() + '';
  }

  return request<{
    code: string;
    data: Record<string, any>;
  }>(`/target/project_list`, {
    method: 'GET',
    params,
  });
}

/** 获取汇总评价-柱状、折线图表数据 */
export async function getSummaryChartsData(filed: string, params?: Record<string, any> & {name: string}) {
  return request<{
    code: string;
    data: Record<string, any>;
  }>(`/target/aggregate/${filed}`, {
    method: 'GET',
    params
  });
}

/** 获取汇总评价-饼图数据 */
export async function getSummaryPieData(params?: {
  name: string;
  contrast_filed?: string,
  contrast_value?: string,
  target_year?: string,
} & Record<string, any>) {
  return request<{
    code: string;
    data: Record<string, any>;
  }>(`/target/statistics`, {
    method: 'GET',
    params
  });
}
