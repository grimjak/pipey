import React from 'react';

const AddUser = (props) => {
    return (
        <form onSubmit={(event) => props.addUser(event)}>
            <div className="field">
                <input
                    name="username"
                    className="input is-large"
                    type="text"
                    placeholder="Enter user name"
                    required
                    value={props.username}
                    onChange={props.handleChange}
                />
            </div>
            <div className="field">
                <input
                    name="firstname"
                    className="input is-large"
                    type="text"
                    placeholder="Enter first name"
                    required
                    value={props.firstname}
                    onChange={props.handleChange}
                />
            </div>
            <div className="field">
                <input
                    name="lastname"
                    className="input is-large"
                    type="text"
                    placeholder="Enter a last name"
                    required
                    value={props.lastname}
                    onChange={props.handleChange}
                />
            </div>
            <div className="field">
                <input
                    name="address"
                    className="input is-large"
                    type="text"
                    placeholder="Enter an address"
                    required
                    value={props.address}
                    onChange={props.handleChange}
                />
            </div>  
            <input
                type="submit"
                className="button is-primary is-large is-fullwidth"
                value="Submit"
            />              
        </form>
    )
};

export default AddUser;