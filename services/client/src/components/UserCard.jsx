import React from 'react';

const UserCard = (props) => {
    return ( 
        <div className={"card is-clipped "+(props.user.active?"undefined":"has-background-light")} onClick={(event) => {props.userSelected(props.index,props.user)}}>
        <div className="card-image">
            <figure className="image is-4by3">
            <img src={props.user.avatar} alt="Large avatar Placeholder"></img>
            </figure>
        </div>
        <div className="card-content">
            <div className="media">
            <div className="media-content">
                <p className="is-is-6">{props.user.firstname} {props.user.lastname}</p>
                <p className="is-size-6">{props.user.username}</p>
                <p className="is-size-7">{props.user.job_title}</p>
                <p className="is-size-7">{props.user.department}</p>
            </div>
            </div>
        </div>
        </div>
    )
};

export default UserCard;