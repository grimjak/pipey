import { combineReducers } from 'redux';
import { userList } from './users';
import { searchTerm } from '././search';

export default combineReducers({
    userList,
    searchTerm
});