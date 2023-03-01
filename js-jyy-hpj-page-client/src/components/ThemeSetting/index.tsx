import React from 'react';
import {message} from 'antd';

type Themes = 'dark'|'light';

function ThemeSetting() {
  const DEFAULT_THEME = 'light';
  const INIT_THEME = localStorage.getItem('site-theme') as Themes;

  const [theme, setTheme] = React.useState<Themes>(INIT_THEME || DEFAULT_THEME); // TODO: 改全局状态

  const updateTheme = (
    dark: boolean,
    color?: string,
    publicPath = '/theme',
    hideMessageLoading?: boolean,
  ) => {
    // ssr
    if (typeof window === 'undefined' || !(window as any).umi_plugin_ant_themeVar) {
      return;
    }

    let hide: any = () => null;
    if (!hideMessageLoading) {
      hide = message.loading('正在加载主题');
    }

    const href = dark ? `${publicPath}/dark` : '';
    // 如果是 dark，并且是 color=daybreak，无需进行拼接
    let colorFileName =
      dark && color ? `-${encodeURIComponent(color)}` : encodeURIComponent(color || '');
    if (color === 'daybreak' && dark) {
      colorFileName = '';
    }

    const dom = document.getElementById('theme-style') as HTMLLinkElement;

    // 如果这两个都是空
    if (!href && !colorFileName) {
      if (dom) {
        dom.remove();
        localStorage.removeItem('site-theme');
        setTheme(DEFAULT_THEME);
      }
      return;
    }

    const url = `${href}${colorFileName || ''}.css`;
    if (dom) {
      dom.onload = () => {
        window.setTimeout(() => {
          hide();
        });
      };
      dom.href = url;
    } else {
      const style = document.createElement('link');
      style.type = 'text/css';
      style.rel = 'stylesheet';
      style.id = 'theme-style';
      style.onload = () => {
        window.setTimeout(() => {
          hide();
        });
      };
      style.href = url;
      if (document.body.append) {
        document.body.append(style);
      console.log('append', style)
      } else {
        document.body.appendChild(style);
      console.log('appendChild', style)
      }
    }

    const targetTheme = dark ? 'dark' : 'light'
    setTheme(targetTheme)
    localStorage.setItem('site-theme', targetTheme);
  };

  const toggleTheme = () => {
    updateTheme(theme === 'light')
  }

  // 初始话是深色，则切换到深色
  React.useEffect(() => {
    if (DEFAULT_THEME === 'dark') {
      updateTheme(true)
    }
  }, [])

  return (
    <a onClick={toggleTheme}>
      切换主题
    </a>
  );
}

export default ThemeSetting;
