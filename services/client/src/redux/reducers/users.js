

const initialState = {
    page: 0,
    isLoading: false,
    hasErrored: false,
    fieldsToShow: ['username','title','firstname','lastname','gender','email','active','admin','address'],
    users: [],
    types: []
};

export function userList(state = initialState, action) {
    switch (action.type) {
        case 'INCREMENT_PAGE':
            return Object.assign({}, state, {page: state.page+1});
        case 'USERS_IS_LOADING':
            return Object.assign({}, state,action.isLoading);   
        case 'USERS_HAS_ERRORED':
            return Object.assign({}, state,action.hasErrored);
        case 'USERTYPES_FETCH_DATA_SUCCESS':
            return Object.assign({}, state, {types: action.types});   
        case 'USERS_FETCH_DATA_SUCCESS':
            return Object.assign({}, state, {users: action.users});
        case 'USERS_FETCH_MORE_DATA_SUCCESS':   
            console.log(action)
            return Object.assign({}, state, {users: state.users.concat(action.users)});
        case 'UPDATE_USER':
            const users = state.users
            users[action.index] = action.user
            return Object.assign({}, state, {users: users});
        case 'APPEND_TO_USER_STORE':
            return Object.assign({}, state, {users: state.users.push(action.user)});
        default:
            return state;
    }
}