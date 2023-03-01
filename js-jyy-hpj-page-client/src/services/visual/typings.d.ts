declare namespace API {
  // 枚举数组
  type Dicts = {
    classification: string[];
    operation_year: string[];
    voltage_level: string[];
  };

  // 枚举字典Map
  type DictsMap = {
    classification: Record<string, string>;
    operation_year: Record<string, string>;
    voltage_level: Record<string, string>;
  };

  // excel
  type Excel = {
    name: string;
    // file: File;
  }
  // excel列表
  type ExcelList = Excel[];

  // 项目
  type Project = {
    classification: string;
    company_province: string;
    name: string;
    operation_year: number;
    voltage_level: number;
    wbs_code: string;
  };

  // 项目列表
  type ProjectList = Project[];

  // 项目信息表格
  type TableProjectInfoType = Project;

  // 项目详情
  type ProjectDetail = Record<string, any>;

  // 项目详情
  type ProjectDetailList = ProjectDetail[];

  type Category = {
    id?: number;
    name?: string;
  };

  type User = {
    id?: number;
    username?: string;
    firstName?: string;
    lastName?: string;
    email?: string;
    password?: string;
    phone?: string;
    /** User Status */
    userStatus?: number;
  };

  type Tag = {
    id?: number;
    name?: string;
  };

  type Pet = {
    id?: number;
    category?: Category;
    name: string;
    photoUrls: string[];
    tags?: Tag[];
    /** pet status in the store */
    status?: 'available' | 'pending' | 'sold';
  };

  type ApiResponse = {
    code?: number;
    type?: string;
    message?: string;
  };

  type findPetsByStatusParams = {
    /** Status values that need to be considered for filter */
    status: 'available' | 'pending' | 'sold'[];
  };

  type findPetsByTagsParams = {
    /** Tags to filter by */
    tags: string[];
  };

  type getPetByIdParams = {
    /** ID of pet to return */
    petId: number;
  };

  type updatePetWithFormParams = {
    /** ID of pet that needs to be updated */
    petId: number;
  };

  type deletePetParams = {
    api_key?: string;
    /** Pet id to delete */
    petId: number;
  };

  type uploadFileParams = {
    /** ID of pet to update */
    petId: number;
  };

  type getOrderByIdParams = {
    /** ID of pet that needs to be fetched */
    orderId: number;
  };

  type deleteOrderParams = {
    /** ID of the order that needs to be deleted */
    orderId: number;
  };

  type loginUserParams = {
    /** The user name for login */
    username: string;
    /** The password for login in clear text */
    password: string;
  };

  type getUserByNameParams = {
    /** The name that needs to be fetched. Use user1 for testing.  */
    username: string;
  };

  type updateUserParams = {
    /** name that need to be updated */
    username: string;
  };

  type deleteUserParams = {
    /** The name that needs to be deleted */
    username: string;
  };
}
