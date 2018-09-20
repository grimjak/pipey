import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';
import UsersList from '../UsersList';

const users = [
    {
        "username": "tb",
        "firstname": "ted",
        "lastname": "bear",
        "employeenumber": "1",
        "address": "23 blodsfsdf"
    },
    {
        "username": "bh",
        "firstname": "bob",
        "lastname": "holmes",
        "employeenumber": "2",
        "address": "77 verulam road"
    }
];

test('UsersList renders properly', () => {
    const wrapper = shallow(<UsersList users={users}/>);
    const element = wrapper.find('h4');
    expect(element.length).toBe(2);
    expect(element.get(0).props.children[0]).toBe('tb');
});

test('UserList renders a snapshot properly', () => {
    const tree = renderer.create(<UsersList users={users}/>).toJSON();
    expect(tree).toMatchSnapshot();
});