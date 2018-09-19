import React from 'react';

const Form = (props) => {
    return (
        <div>
            <h1 className="title is-1">{props.formType}</h1>
            <hr/><br/>
            <form onSubmit={(event) => props.handleUserFormSubmit(event)}>
                <div className="field">
                    <input
                        name="username"
                        className="input is-medium"
                        type="text"
                        placeholder="Enter username"
                        required
                        value={props.formData.username}
                        onChange={props.handleFormChange}
                    />
                </div>
                <div className="field">
                    <input
                        name="password"
                        className="input is-medium"
                        type="password"
                        placeholder="Enter password"
                        required
                        value={props.formData.password}
                        onChange={props.handleFormChange}
                    />
                </div>
                <input
                    type="submit"
                    className="button is-primary is-medium is-fullwidth"
                    value="Submit"
                />
            </form>
        </div>
    )
};

export default Form;