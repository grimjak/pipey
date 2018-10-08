import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer'

import Message from '../Message';

const successRemoveMessage = jest.fn();
const dangerRemoveMessage = jest.fn();


const testDate = [
    {
        messageName: 'Hello, world!',
        messageType: 'success',
        removeMessage: successRemoveMessage,
    },
    {
        messageName: 'Hello, world!',
        messageType: 'danger',
        removeMessage: dangerRemoveMessage, 
    }
]

describe('When given a message', () => {
    testDate.forEach((e1) => {
        const component = <Message {...e1} />;
        it(`${e1.messageType} Message renders properly`, () => {
            const wrapper = shallow(component);
            const element = wrapper.find(`.notification.is-${e1.messageType}`);
            expect(element.length).toBe(1);
            const span = wrapper.find('span');
            expect(span.length).toBe(1);
            expect(span.get(0).props.children).toContain(
                e1.messageName);
            const button = wrapper.find('button');
            expect(button.length).toBe(1);
            expect(e1.removeMessage).toHaveBeenCalledTimes(0);
            button.simulate('click');
            expect(e1.removeMessage).toHaveBeenCalledTimes(1);
        });

        it(`${e1.messageType} Message renders a snapshot properly`, () => {
            const tree = renderer.create(
                <Message {...e1} />
            ).toJSON();
            expect(tree).toMatchSnapshot();
        });
    });
});