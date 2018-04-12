import React from 'react';
import './index.css';
import { Tabs, Tab } from 'react-bootstrap';

import AddQuestions from './AddQuestions';
import CreateTest from './CreateTest';
import Grade from './Grade';

const screens = [
  {'title': 'Add Questions', component: AddQuestions},
  {'title': 'Create Test', component: CreateTest},
  {'title': 'Grade Test', component: Grade},
];

const Screens = () => (
  <Tabs className='myClass' style={{ display: 'flex', flex: 1 }} animation={false} defaultActiveKey={0}>
    {screens.map(({ title, component: Component }, i) => (
      <Tab key={i} eventKey={i} title={title} style={{ diplay: 'flex', flex: 1 }}>
        <Component />
      </Tab>
    ))}
  </Tabs>
);

export default Screens;
