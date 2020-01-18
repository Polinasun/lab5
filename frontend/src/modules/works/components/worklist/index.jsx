import React from 'react';
import { Table, Divider, Tag, Icon, notification, Spin } from 'antd';
import {Link} from 'react-router-dom';

const EN_LEV = ["breakfast","lunch","dinner"];



export default class Works extends React.Component {
    columns = [
        {
            title: 'Номер комнаты',
            dataIndex: 'number_room',
            key: 'number',
        },
        {
            title: 'Категория меню',
            dataIndex: 'menu_category',
            key: 'address1',
            render: text => EN_LEV[text],
        },

        {
            title: 'Action',
            key: 'action',
            dataIndex: "uuid",
            render: (uuid) => (
              <span>
                <Link to={`/work/patch/${uuid}/`}><Icon type="edit" /></Link>
                <Divider type="vertical" />
                <a href="#" onClick={() => this.props.deleteWork(uuid)}><Icon type="delete" /></a>
              </span>
            ),
          },
      ];

      
    componentDidMount(){
        const {fetchWorks, filters} = this.props;
        fetchWorks(filters);
    }

    componentDidUpdate(prevProps){
        const {fetchWorks, filters, deleteHandled} = this.props;
        if(prevProps.filters !== filters) {
            fetchWorks(filters);
        }
        
        if(this.props.isDeleted == true){
            fetchWorks(filters);
            deleteHandled();
        }
       
    }

    render(){
        const {errors, works, isFetching} = this.props;
        if(isFetching) return(<Spin/>);
        if(errors){
            notification.error({message: errors.message});
        }
        return (
            <Table columns={this.columns} dataSource={this.props.works} />
        )
    }
}

    
