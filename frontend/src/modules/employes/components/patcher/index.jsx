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
                this.props.patchEMP(this.props.match.params.uuid, values);
            }else{
                alert(JSON.stringify(err));
            }
          });
    }
    numberValidator(rule, val, callback){
        if(val != '' && isNaN(val)){
            callback("Not a number!");
        }else if(val<1){
            callback("Smaller then 1");
        }else if(val>500){
            callback("Biger then 500");
        } else {
            callback();
        }
    }
    render(){
        const { getFieldDecorator } = this.props.form;
        return (
        <Form onSubmit ={this.onSubmit} className="jojo" >
            <h2>Редактирование</h2>
            <Form.Item>
            {getFieldDecorator('name', {
                rules: [{ required: true, message: 'Please input your username!' }],
                initialValue: this.props.emp.name
                })(
                    <Input
                        placeholder="Имя"/>
                )
            }
            </Form.Item>

            <Form.Item>
            {getFieldDecorator('surname', {
                rules: [{ required: true, message: 'Please input your username!' }],
                initialValue: this.props.emp.surname
                })(
                    <Input
                        placeholder="Фамилия"/>
                )
            }
            </Form.Item>
            

            <Form.Item>
            {getFieldDecorator('number_room', {
                rules: [
                    { required: true, message: 'Please input your number room!' },
                    { validator: this.numberValidator } 
                ],
                initialValue: this.props.emp.number_room
                })(
                    <Input
                        placeholder="Номер комнаты"/>
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
    componentDidUpdate(prevProps){
        console.log(this.props, prevProps);
        if(this.props.isFailed && prevProps.isFailed !== this.props.isFailed) {
            window.alert("400 patch");
        }
        if(this.props.isPatched){
            console.log('isPatched')
            this.props.patchflag();
            this.props.history.goBack();
        }
    }
    componentDidMount(){
        const {getEMP} = this.props;
        getEMP(this.props.match.params.uuid);
    }
    
}

export default Form.create()(PatchForm);