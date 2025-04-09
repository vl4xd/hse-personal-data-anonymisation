import { Typography, Table } from 'antd';

const { Title } = Typography;

function MainPage() {

    const dataSourceLabels = [
        {
          name: 'AGE',
          example: '115 лет и 253 дня',
          about: 'Выделение возраста',
        },
        {
            name: 'AWARD',
            example: 'Герою Советского Союза',
            about: 'Выделение достижения',
          },
          {
            name: 'CITY',
            example: 'Нью-Йорке',
            about: 'Выделение города',
          },
          {
            name: 'COUNTRY',
            example: 'Японии',
            about: 'Выделение страны',
          },
          {
            name: 'CRIME',
            example: 'мошенничестве с криптовалютой',
            about: 'Выделение преступления',
          },
          {
            name: 'DATE',
            example: 'в среду, 20 апреля 2016 года',
            about: 'Выделение даты',
          },
          {
            name: 'DISEASE',
            example: 'пищевым отравлением',
            about: 'Выделение заболевания',
          },
          {
            name: 'DISTRICT',
            example: 'Старого города',
            about: 'Выделение района',
          },
          {
            name: 'EVENT',
            example: 'заступит на свою должность',
            about: 'Выделение события',
          },
          {
            name: 'FACILITY',
            example: 'Исаакиевский собор',
            about: 'Выделение объекта / сооружения',
          },
          {
            name: 'FAMILY',
            example: 'королевской семьей Дании',
            about: 'Выделение рода',
          },
          {
            name: 'IDEOLOGY',
            example: 'национально-патриотическая',
            about: 'Выделение идеалогии',
          },
          {
            name: 'LANGUAGE',
            example: 'русском',
            about: 'Выделение языка',
          },
          {
            name: 'LAW',
            example: 'Договора о коллективной безопасности',
            about: 'Выделение закона',
          },
          {
            name: 'LOCATION',
            example: 'вблизи Дуная',
            about: 'Выделение локации / места',
          },
          {
            name: 'MONEY',
            example: 'около 200 млн руб.',
            about: 'Выделение денежной суммы',
          },
          {
            name: 'NATIONALITY',
            example: 'норвежца',
            about: 'Выделение национальности',
          },
          {
            name: 'NUMBER',
            example: 'около 20',
            about: 'Выделение числа',
          },
          {
            name: 'ORDINAL',
            example: 'второго',
            about: 'Выделение числа',
          },
          {
            name: 'ORGANIZATION',
            example: 'Совет Безопасности ООН',
            about: 'Выделение организации',
          },
          {
            name: 'PENALTY',
            example: 'штраф в размере более 110 тысяч долларов',
            about: 'Выделение штрафа / запрета',
          },
          {
            name: 'PERCENT',
            example: '96 процентов',
            about: 'Выделение процентного соотношения',
          },
          {
            name: 'PERSON',
            example: 'Эндрю Джексона',
            about: 'Выделение персоны / ФИО',
          },
          {
            name: 'PRODUCT',
            example: 'Форда Мустанг',
            about: 'Выделение продукта',
          },
          {
            name: 'PROFESSION',
            example: 'премьер-министра Португалии',
            about: 'Выделение профессии',
          },
          {
            name: 'RELIGION',
            example: 'христиане',
            about: 'Выделение религии',
          },
          {
            name: 'STATE_OR_PROVINCE',
            example: 'ХМАО',
            about: 'Выделение субъекта / области',
          },
          {
            name: 'TIME',
            example: 'около часа ночи',
            about: 'Выделение времени',
          },
          {
            name: 'WORK_OF_ART',
            example: 'Список Шиндлера',
            about: 'Выделение произведения',
          },
      ];
      
      const columnsLabels = [
        {
          title: 'Название класса сущности',
          dataIndex: 'name',
          key: 'name',
        },
        {
            title: 'Описание',
            dataIndex: 'about',
            key: 'about',
          },
        {
          title: 'Пример сущности данного класса',
          dataIndex: 'example',
          key: 'example',
        },
      ];

    const dataSourceAnon = [
        {
          name: 'Без анонимизации',
          about: 'Возвращает текст без анонимизации с выделенными сущностями',
          mask: 'Нет',
          exampleB: 'Леонардо Вильгельм Ди Каприо (род. 11 ноября 1974, Лос-Анджелес, США) — американский актёр и кинопродюсер.',
          exampleA: 'Леонардо Вильгельм Ди Каприо (род. 11 ноября 1974, Лос-Анджелес, США) — американский актёр и кинопродюсер.',
        },
        {
            name: 'Замена на сигнатуру сущности',
            about: 'Возвращает текст с заменой выделенных сущностей на их класс (сигнатуру)',
            mask: 'Нет',
            exampleB: 'Леонардо Вильгельм Ди Каприо (род. 11 ноября 1974, Лос-Анджелес, США) — американский актёр и кинопродюсер.',
            exampleA: '<PERSON> <PERSON> (род. <DATE>, <CITY>, <COUNTRY>) — <NATIONALITY> <PROFESSION> и <PROFESSION>.',
        },
        {
            name: 'Замена на символ',
            about: 'Возвращает текст с заменой выделенных сущностей на заданную маску (символ / строку)',
            mask: 'Да (***)',
            exampleB: 'Леонардо Вильгельм Ди Каприо (род. 11 ноября 1974, Лос-Анджелес, США) — американский актёр и кинопродюсер.',
            exampleA: '*** *** (род. ***, ***, ***) — *** *** и ***.',
        },
    ];

    const columnsAnon = [
        {
            title: 'Название метода',
            dataIndex: 'name',
            key: 'name',
        },
        {
            title: 'Описание',
            dataIndex: 'about',
            key: 'about',
        },
        {
            title: 'Маска',
            dataIndex: 'mask',
            key: 'mask',
        },
        {
            title: 'Пример ДО',
            dataIndex: 'exampleB',
            key: 'exampleB',
        },
        {
            title: 'Пример ПОСЛЕ',
            dataIndex: 'exampleA',
            key: 'exampleA',
        },
    ];

    return (
        <>
            <Title>Главная страница</Title>
            <Title level={2}>Тип анонимизации:</Title>
            <Table dataSource={dataSourceAnon} columns={columnsAnon} />;

            <Title level={2}>Модель SpaCy:</Title>
            <Table dataSource={dataSourceLabels} columns={columnsLabels} />;
            
        </>
    );
};

export default MainPage;