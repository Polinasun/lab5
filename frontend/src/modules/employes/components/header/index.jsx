import React from 'react';
import {PageHeader, Button,Form,Input} from 'antd';

import FilterForm from '../../containers/filterContainer';

export default (props) => (
    <PageHeader
        style={{
        border: '1px solid rgb(235, 237, 240)',
        }}
        title="Гости"
        {...props}
        extra={[
          ]}
    >
      <FilterForm/>
      </PageHeader>
);
