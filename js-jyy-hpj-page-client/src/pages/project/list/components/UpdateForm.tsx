import React from 'react';
import { Button, Upload, Form, Modal, message } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import ProForm from '@ant-design/pro-form';
import { serverUrl } from '@/util/constants';
import styles from '../style.less';
import type { UploadChangeParam } from 'antd/lib/upload/interface';

export type FormValueType = {
  target?: string;
  template?: string;
  type?: string;
  time?: string;
  frequency?: string;
} & Partial<API.Project>;

export type UpdateFormProps = {
  updateModalVisible: boolean;
  handleUpdateModalVisible: (v: boolean) => void;
};

const linkStyle: React.CSSProperties = {
  marginLeft: 12, position: 'absolute', left: 86, top: 5, whiteSpace: 'nowrap'
}

const UpdateForm: React.FC<UpdateFormProps> = (props) => {
  // 新增上传
  const addFileProps = {
    name: 'file',
    action:  IS_DEV ? '/devProxy/api/v1/project/new_project' : '/devProxy/api/v1/project/new_project',
    accept: '.xlsx',
    onChange(info: UploadChangeParam) {
      if (info.file.status === 'done') {
        message.success(`上传成功`);
      } else if (info.file.status === 'error') {
        message.error(`上传失败，请参考上传模板填写`);
      }
    },
    maxCount: 1,
    showUploadList: {
      showDownloadIcon: false,
      showRemoveIcon: false,
    },
  };

  // 更新历史
  const updateFileProps = {
    name: 'file',
    action: IS_DEV ? '/devProxy/api/v1/project/history_project' : '/devProxy/api/v1/project/history_project',
    accept: '.xlsx',
    onChange(info: UploadChangeParam) {
      if (info.file.status === 'done') {
        message.success(`上传成功`);
      } else if (info.file.status === 'error') {
        message.error(`上传失败，请参考上传模板填写`);
      }
    },
    maxCount: 1,
    showUploadList: {
      showDownloadIcon: false,
      showRemoveIcon: false,
    },
  };

  return (
    <Modal
      className={styles['update-form']}
      width={508}
      title="更新"
      destroyOnClose
      centered
      open={props.updateModalVisible}
      onVisibleChange={props.handleUpdateModalVisible}
      onCancel={() => props.handleUpdateModalVisible(false)}
      footer={null}
    >
      <Form labelCol={{span: 8}} wrapperCol={{span: 10}}>
        <Form.Item
          name="1"
          label="新增项目"
          required
        >
          <Button.Group>
            <Upload {...addFileProps}>
              <Button icon={<UploadOutlined />}>上传</Button>
            </Upload>
            <a href={`${serverUrl}/template/新增项目模板.xlsx`} style={linkStyle}>下载上传模板</a>
          </Button.Group>
        </Form.Item>
        <ProForm.Item
          label="更新历史项目"
          required
          name="2"
        >
          <Button.Group>
            <Upload
              {...updateFileProps}
            >
              <Button icon={<UploadOutlined />}>上传</Button>
            </Upload>
            <a href={`${serverUrl}/template/更新历史项目模板.xlsx`} style={linkStyle}>下载上传模板</a>
          </Button.Group>
        </ProForm.Item>
      </Form>
    </Modal>
  );
};

export default UpdateForm;
