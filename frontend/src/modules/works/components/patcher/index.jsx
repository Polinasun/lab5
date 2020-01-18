import './edit.css';
import React from 'react';
import {BrowserRouter as Router, Switch, Route} from "react-router-dom"
import { Form, Input, Select, Button } from 'antd';
const { Option } = Select;





class PatchForm extends React.Component {
    state={initialValues:{}}

    onSubmit = (e) => {
        e.preventDefault();

        this.props.form.validateFields((err, values) => {
            
            if (!err) {
                console.log(this.props);
                this.props.patchWork(this.props.match.params.uuid, values);
            }else{
                alert(JSON.stringify(err));
            }
          });
    }
    
    
    render(){
        const { getFieldDecorator } = this.props.form;
        return (
        <Form onSubmit ={this.onSubmit} className="jojo" >
            <h2>Редактирование</h2>

            <Form.Item>
            {getFieldDecorator('number_room', {
                rules: [{ required: true, message: 'Please input your username!' }],
                initialValue: this.props.emp.nps_name
                })(
                    <Input
                        placeholder="Номер комнаты"/>
                )
            }
            </Form.Item>


            <Form.Item>
            {getFieldDecorator('menu_category', {
                rules: [{ required: true, message: 'Please input your username!' }],
                initialValue: this.props.emp.english_level
                })(
                <Select>
                    <Option value="">Катег. меню</Option>
                    <Option value="0">breakfast</Option>
                    <Option value="1">lunch</Option>
                    <Option value="2">dinner</Option>
                </Select>
                )
            }
            </Form.Item>

            <Form.Item>
                <Button type="primary" htmlType="submit">
                    Изменить
                </Button>
            </Form.Item>
        </Form> 
        )
    }
    componentDidUpdate(){
        console.log(this.props);
        if(this.props.isPatched){
            console.log('isPatched')
            this.props.patchflag();
            this.props.history.goBack();
        }
    }
    componentDidMount(){
        const {getWork} = this.props;
        getWork(this.props.match.params.uuid);
    }
    
}

export default Form.create()(PatchForm);