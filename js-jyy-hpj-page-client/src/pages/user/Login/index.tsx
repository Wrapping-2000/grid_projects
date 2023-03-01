import {
  LockOutlined,
  UserOutlined,
} from '@ant-design/icons';
import { Alert, message, Tabs } from 'antd';
import cls from 'classnames';
import React, { useState } from 'react';
import {  ProFormText, LoginForm/* , ProFormCheckbox */ } from '@ant-design/pro-form';
import { useIntl, history, FormattedMessage, useModel } from 'umi';
import { login, getDicts } from '@/services/main';
import localStorage, { keys } from '@/util/localStorage';
import { array2Map } from '@/util/array2Map';

import styles from './index.less';

const LoginMessage: React.FC<{
  content: string;
}> = ({ content }) => (
  <Alert
    style={{
      marginBottom: 24,
    }}
    message={content}
    type="error"
    showIcon
  />
);

const Login: React.FC = () => {
  const [userLoginState, setUserLoginState] = useState<Record<string, any>>({});
  const [type, setType] = useState<string>('account');
  const { setInitialState } = useModel('@@initialState');

  const intl = useIntl();

  const fetchUserInfo = async (data: Record<string, any>) => {
    await setInitialState((s) => ({
      ...s,
      currentUser: data.userInfo,
      dicts: data.dicts
    }) as any);
  };

  const fetchDicts = async (): Promise<API.DictsMap> => {
    const userName = localStorage.getItem(keys.USER_NAME);
    if (userName) {
      try {
        const msg = await getDicts();
        return {
          classification: array2Map(msg?.data?.classification) || {},
          voltage_level: array2Map(msg?.data?.voltage_level) || {},
        };
      } catch (error) {}
    }
    return {
      classification: {},
      voltage_level: {},
    };
  };

  const handleSubmit = async (values: any) => {
    try {
      // 登录
      const msg = await login({ ...values });

      if (msg.code === 'SUCCESS') {
        const defaultLoginSuccessMessage = intl.formatMessage({
          id: 'pages.login.success',
          defaultMessage: '登录成功！',
        });
        message.success(defaultLoginSuccessMessage);
        localStorage.setItem(keys.USER_NAME, values?.user_name);

        // 获取dict
        const dicts = await fetchDicts();

        await fetchUserInfo({userInfo: {name: values.user_name}, dicts});
        /** 此方法会跳转到 redirect 参数所在的位置 */
        if (!history) return;
        const { query } = history.location;
        const { redirect } = query as { redirect: string };
        history.push(redirect || '/');
        return;
      }

      if (msg?.error_message === 'Invalid user_name or password.') {
        message.error('账号密码错误！')
      }
      // 如果失败去设置用户错误信息
      setUserLoginState(msg);
    } catch (error) {
      console.log(error)
    }
  };
  const { status, type: loginType } = userLoginState;

  return (
    <div className={cls([styles.container, 'login-container'])}>
      <img className={styles.logo} src={require('@/assets/logo.png')} alt="" />
      <div className={styles.content}>
        <LoginForm
          className="login-form"
          // logo={<img alt="logo" src="/logo.svg" />}
          title={<h2 className={styles.title}>电网评价诊断智能分析平台</h2> as any}
          subTitle=" "
          initialValues={{
            autoLogin: true,
          }}
          onFinish={async (values) => {
            await handleSubmit(values as any);
          }}
          style={{width: 400}}
        >
          <Tabs className={styles.tabs} activeKey={type} onChange={setType}>
            <Tabs.TabPane
              key="account"
              tab={intl.formatMessage({
                id: 'pages.login.accountLogin.tab',
                defaultMessage: '账户密码登录',
              })}
            />
            <Tabs.TabPane
              key="mobile"
              tab={intl.formatMessage({
                id: 'pages.login.phoneLogin.tab',
                defaultMessage: '手机号登录',
              })}
            />
          </Tabs>

          {status === 'error' && loginType === 'account' && (
            <LoginMessage
              content={intl.formatMessage({
                id: 'pages.login.accountLogin.errorMessage',
                defaultMessage: '账户或密码错误(admin/ant.design)',
              })}
            />
          )}
          {type === 'account' && (
            <>
              <ProFormText
                name="user_name"
                fieldProps={{
                  size: 'large',
                  prefix: <UserOutlined className={styles.prefixIcon} />,
                }}
                placeholder={intl.formatMessage({
                  id: 'pages.login.username.placeholder',
                  defaultMessage: '账号',
                })}
                rules={[
                  {
                    required: true,
                    message: (
                      <FormattedMessage
                        id="pages.login.username.required"
                        defaultMessage="请输入账号!"
                      />
                    ),
                  },
                ]}
              />
              <ProFormText.Password
                name="password"
                fieldProps={{
                  size: 'large',
                  prefix: <LockOutlined className={styles.prefixIcon} />,
                }}
                placeholder={intl.formatMessage({
                  id: 'pages.login.password.placeholder',
                  defaultMessage: '密码',
                })}
                rules={[
                  {
                    required: true,
                    message: (
                      <FormattedMessage
                        id="pages.login.password.required"
                        defaultMessage="请输入密码！"
                      />
                    ),
                  },
                ]}
              />
            </>
          )}
          {/* <div
            style={{
              marginBottom: 24,
            }}
          >
            <ProFormCheckbox noStyle name="autoLogin">
              <FormattedMessage id="pages.login.rememberMe" defaultMessage="记住账号" />
            </ProFormCheckbox>
          </div> */}
        </LoginForm>
      </div>
    </div>
  );
};

export default Login;
