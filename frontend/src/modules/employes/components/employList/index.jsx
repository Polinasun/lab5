import React from 'react';
import { Table, Divider, Tag, Icon, notification, Spin } from 'antd';
import {Link} from 'react-router-dom';
const EN_LEV = ['standard', 'Apartmant','Business', 'De luxe', 'President'];
const SPL = [ 'breakfast','lunch', 'dinner']

function getRandomInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
  }

export default class Emps extends React.Component {
    columns = [
        {
            title: 'Имя',
            dataIndex: 'name',
            key: 'name',
        },
        {
            title: 'Фамилия',
            dataIndex: 'surname',
            key: 'age',
        },
        {
            title: 'Номер комнаты',
            dataIndex: 'number_room',
            key: 'address1',
        },
        
        {
            title: 'Класс номера',
            dataIndex: 'room_category',
            key: 'address2',
            render: text => EN_LEV[text],
        },
        {
            title: 'Меню',
            dataIndex: 'menu_category',
            key: 'address3',
            render: text => SPL[text],
        },

        {
            title: 'Action',
            key: 'action',
            dataIndex: "uuid",
            render: (uuid) => (
              <span>
                <Link to={`/emp/patch/${uuid}/`}><Icon type="edit" /></Link>
                <Divider type="vertical" />
                <a href="#" onClick={() => this.props.deleteEMP(uuid)}><Icon type="delete" /></a>
              </span>
            ),
          },
      ];

    componentDidMount(){
        const {fetchEmps, filters} = this.props;
        fetchEmps(filters);
    }

    componentDidUpdate(prevProps){
        const {fetchEmps, filters, deleteHandled} = this.props;
        if(prevProps.filters !== filters) {
            fetchEmps(filters);
        }
        if(this.props.isDeleted == true){
            fetchEmps(filters);
            deleteHandled();
        }
    }

    render(){
        const {errors, emps, isFetching} = this.props;
        if(isFetching) return(<Spin/>);
        if(errors){
            notification.error({message: errors.message});
        }
        return (
            <Table columns={this.columns} dataSource={this.props.emps} />
        )
    }
}
