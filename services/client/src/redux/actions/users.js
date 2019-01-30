import axios from 'axios';


export function usersHasErrored(bool) {
    return {
        type: 'USERS_HAS_ERRORED',
        hasErrored: bool
    };
}

export function usersIsLoading(bool) {
    return {
        type: 'USERS_IS_LOADING',
        isLoading: bool
    }
}

export function userIsUpdating(bool) {
    return {
        type: 'USER_IS_UPDATING',
        isUpdating: bool
    }
}

export function userIsCreating(bool) {
    return {
        type: 'USER_IS_CREATING',
        isUpdating: bool
    }
}

export function usersFetchDataSuccess(users,append) {
    if(append)
    {
        return { 
            type: 'USERS_FETCH_MORE_DATA_SUCCESS',
            users
        };
    } else 
    {
        return {
            type: 'USERS_FETCH_DATA_SUCCESS',
            users
        };
    }
}

export function userTypesFetchDataSuccess(types) {
    return {
        type: 'USERTYPES_FETCH_DATA_SUCCESS',
        types
    };
}

export function incrementPage() {
    return {
        type: 'INCREMENT_PAGE'
    };
}

export function updateUserStore(index,user) {
    return {
        type: 'UPDATE_USER',
        index: index,
        user: user
    };
}

export function appendToUserStore(user) {
    return {
        type: 'APPEND_TO_USER_STORE',
        user: user
    };
}

export function updateUser(index,user) {
    const options = {
        url: `${process.env.REACT_APP_USERS_SERVICE_URL}/people/people/`+user.id,
        method: 'put',
        headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${window.localStorage.authToken}`
        },
        data: user
    };
    return (dispatch) => {
        dispatch(userIsUpdating(true));
        dispatch(updateUserStore(index,user))
        axios(options)
        .then((res) => {
            dispatch(userIsUpdating(false));
        })
        .catch((err) => dispatch(usersHasErrored(true)));
    }
    
}

export function createUser(user) {
    const options = {
        url: `${process.env.REACT_APP_USERS_SERVICE_URL}/people/people/`,
        method: 'post',
        headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${window.localStorage.authToken}`
        },
        data: user
    };
    return (dispatch) => {
        dispatch(userIsCreating(true));
        dispatch(appendToUserStore(user))
        axios(options)
        .then((res) => {
            dispatch(userIsCreating(false));
        })
        .catch((err) => dispatch(usersHasErrored(true)));
    }
    
}

export function usersFetchData(text,append=false) {
    return (dispatch) => {
        dispatch(usersIsLoading(true));
        const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/people/people`;
        axios.get(url+text)
        .then((res) => {                 
            dispatch(usersIsLoading(false));
            dispatch(usersFetchDataSuccess(res.data,append))  
        })
        .catch((err) => dispatch (usersHasErrored(true)));
    }
}

export function userTypesFetchData() {
    return (dispatch) => {
        dispatch(usersIsLoading(true));
        const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/people/peopletypes`;
        axios.get(url)
        .then((res) => {
            dispatch(usersIsLoading(false));
            dispatch(userTypesFetchDataSuccess(res.data))
        })
        .catch((err) => dispatch (usersHasErrored(true)));
    }
}