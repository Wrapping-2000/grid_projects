import React, {useState} from 'react';
import {Button, Form, message, Modal,Upload, UploadFile} from 'antd';
import styles from './style.less';
import { DownloadOutlined } from "@ant-design/icons";
import {UploadChangeParam} from "antd/lib/upload/interface";
export type ImportFormProps = {
  importModalVisible: boolean;
  handleImportModalVisible: (v: boolean) => void;
};
const ImportForm: React.FC<ImportFormProps> = (props) => {
  const [fileList, setFileList] = useState<UploadFile[]>([]);
  const normFile = (e: any) => {
    return e?.fileList;
  };
  const handleFinish = (value: any) => {
    const {file} = value;
    const formData = new FormData();
    file.forEach((item: { originFileObj: string | Blob; }, index: any) => {
      formData.append(`file-${index}`, item.originFileObj);
    })
  }

  return (
    <Modal
      className={styles['update-form']}
      width={508}
      title="导入"
      destroyOnClose={true}
      centered={true}
      open={props.importModalVisible}
      // @ts-ignore
      onVisibleChange={props.handleImportModalVisible}
      onCancel={() => props.handleImportModalVisible(false)}
      footer={null}
    >
      <Form
        onFinish={handleFinish}
        labelCol={{span: 10}}
        wrapperCol={{span: 10}}
        name={"formName"}
        method={"POST"}
      >
        <Form.Item
          label="选择excel文件："
          required={true}
          name="formItemName"
          valuePropName="valuePropName"
	        getValueFromEvent={normFile}
        >
          <Upload
            name={'file'}
            action={`/devProxy/api/v1/excel/save_excel`}
            accept={'application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}
            fileList={fileList}
            method={"POST"}
            maxCount={1}
            onChange={(info: UploadChangeParam) => {
              if (info.file.status == 'uploading') {
                setFileList(info.fileList);
              }
              if (info.file.status == 'done') {
                message.success(`${info.file.name} 文件导入成功！`);
              } else if (info.file.status == 'error') {
                message.error(`${info.file.name} 文件导入失败！`);
              }
              setFileList(info.fileList);
            }
            }
          >
            <Button icon={<DownloadOutlined/>}>导入</Button>
          </Upload>
        </Form.Item>
      </Form>
    </Modal>
  );
};
export default ImportForm;



