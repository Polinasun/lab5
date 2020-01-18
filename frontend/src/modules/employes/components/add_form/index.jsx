import React from 'react';
import {BrowserRouter as Router, Switch, Route} from "react-router-dom"
import { Form, Input, Select, Button } from 'antd';
import './add_form.css';
const { Option } = Select;



class AddForm extends React.Component {
    onSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            values.work = Number(values.work);
            if (!err) {
                this.props.addEmps(values);
            }else{
                alert(JSON.stringify(err));
            }
          });
    }
    
    render(){
        const{isFetching, erros} = this.props;

        const { getFieldDecorator } = this.props.form;
        if(isFetching) return(<>Loading...</>);
        return (
        <Form className = 'jojo' onSubmit={this.onSubmit}>
            <h2>Добавить гостя</h2>
            <Form.Item>
            {getFieldDecorator('name', {
                rules: [{ required: true, message: 'Please input your username!' }],
                })(
                    <Input
                        placeholder="Имя"/>
                )
            }
            </Form.Item>

            <Form.Item>
            {getFieldDecorator('surname', {
                rules: [{ required: true, message: 'Please input your username!' }],
                })(
                    <Input
                        placeholder="Фамилия"/>
                )
            }
            </Form.Item>

            <Form.Item>
            {getFieldDecorator('number_room', {

                })(
                    <Input
                        placeholder="Номер комнаты"/>
                )
            }
            </Form.Item>

            <Form.Item>
            {getFieldDecorator('room_category', {
                rules: [{ required: true, message: 'Please input your username!' }],
                })(
                <Select>
                    <Option value="0">standard</Option>
                    <Option value="1">Apartmant</Option>
                    <Option value="2">Business</Option>
                    <Option value="3">De luxe</Option>
                    <Option value="4">President</Option>
                </Select>
                )
            }
            </Form.Item>

            <Form.Item>
            {getFieldDecorator('menu_category', {
                rules: [{ required: true, message: 'Please input your username!' }],
                })(
                <Select>
                    <Option value="0">breakfast</Option>
                    <Option value="1">lunch</Option>
                    <Option value="2">dinner</Option>
                </Select>
                )
            }
            </Form.Item>

            <Form.Item>
                <Button type="primary" htmlType="submit">
                    Добавить
                </Button>
            </Form.Item>
        </Form>
        )
    }
}

export default Form.create()(AddForm);
