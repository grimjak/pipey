import React from 'react';
import { shallow, mount } from 'enzyme';
import renderer from 'react-test-renderer';
import { MemoryRouter as Router } from 'react-router-dom';
import FormErrors from '../forms/FormErrors';
import { loginFormRules } from '../forms/form-rules.js';

const loginFormProps = {
    formType: 'login',
    formRules: loginFormRules
}

test('FormErrors (with login form) renders properly', () => {
    const wrapper = shallow(<FormErrors {...loginFormProps} />);
    const ul = wrapper.find('ul');
    expect(ul.length).toBe(1);
    const li = wrapper.find('li');
    expect(li.length).toBe(2);
    expect(li.get(0).props.children).toContain(
        'Username is required');
    expect(li.get(1).props.children).toContain(
        'Password is required');
});

test('FormErrors (with login form) renders a snapshot properly', () => {
    const tree = renderer.create(
        <Router><FormErrors {...loginFormProps} /></Router>
    ).toJSON();
    expect(tree).toMatchSnapshot();
});