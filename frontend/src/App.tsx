import './App.css'
import React, {useState} from 'react';
import { Layout, Menu} from 'antd';
import { DownSquareOutlined, HomeOutlined, GithubOutlined } from '@ant-design/icons';
import type { MenuProps } from 'antd';

import MainPage from './assets/components/HomePage';
import ManualAnon from './assets/components/ManualAnon';

type MenuItem = Required<MenuProps>['items'][number];
const items: MenuItem[] = [
  {
    label: 'Главная страница',
    key: 'HomePage',
    icon: <HomeOutlined />,
  },
  {
    label: 'Анонимизировать данные',
    key: 'SubMenu',
    icon: <DownSquareOutlined />,
    children: [
      {
        type: 'group',
        label: 'Ручной ввод',
        children: [
          { label: 'Текстовое поле', key: 'manual-input' },
        ],
      },
      {
        type: 'group',
        label: 'Файл',
        children: [
          { label: '.TXT', key: 'file-txt', disabled: true, },
          { label: '.DOCX', key: 'file-docx', disabled: true, },
          { label: '.PDF', key: 'file-pdf', disabled: true, },
        ],
      },
    ],
  },
  {
    key: 'alipay',
    label: (
      <a href="https://github.com/vl4xd/hse-personal-data-anonymisation" target="_blank" rel="noopener noreferrer">
        Репозиторий проекта
      </a>
    ),
    icon: <GithubOutlined/>
  },
];

const { Header, Content, Footer } = Layout;

const App: React.FC = () => {

  const [current, setCurrent] = useState('HomePage');
  const onClick: MenuProps['onClick'] = (e) => {
    setCurrent(e.key);
  };

  // Функция для рендеринга контента
  const renderContent = () => {
    switch(current) {
      case 'HomePage':
        return <MainPage />;
      case 'manual-input':
        return <ManualAnon />;
      default:
        return <MainPage />;
    }
  };

  return (
    <Layout>
      <Header
        style={{
          position: 'sticky',
          top: 0,
          zIndex: 1,
          width: '100%',
          alignItems: 'center',
          padding: 0,
        }}
      >
        <Menu onClick={onClick} selectedKeys={[current]} mode="horizontal" items={items} />
      </Header>
      
      <Content style={{ 
        padding: '0 48px',
        minHeight: 'calc(100vh - 64px - 70px)', // начальная высота контента: высота экрана - высота хедера - высота футера
        }}
      >
        {renderContent()}
      </Content>
      <Footer style={{ textAlign: 'center' }}>
        ©{new Date().getFullYear()} Created by ...
      </Footer>
    </Layout>
  );
};

export default App;
