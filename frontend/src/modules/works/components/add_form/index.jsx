import React from 'react';
import {BrowserRouter as Router, Switch, Route} from "react-router-dom"
import { Form, Input, Select, Button } from 'antd';
import './add_form.css';
const { Option } = Select;



class AddForm extends React.Component {
    onSubmit = (e) => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            if (!err) {
                this.props.addWork(values);
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
            <h2>Добавить меню</h2>
            <Form.Item>
            {getFieldDecorator('number_room', {
                rules: [{ required: true, message: 'Please input your username!' }],
                })(
                    <Input
                        placeholder="Номер комнаты"/>
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