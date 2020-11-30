import React from 'react';
import {Socket} from '../Socket';

import {User, UserFlags} from '../User';
export function ProfileInfo({user})
{
    const showInterests = user.flags & UserFlags.ShowInterests;
    let interestsList = "Hidden";

    if(showInterests)
    {
        interestsList = user.interests;
        if(interestsList.length <= 0) interestsList = "No interests";
    }

    function onShowInterestsClick(event)
    {
        const checkbox = document.getElementById("show-interests");
        Socket.emit('show interests changed', {
            email: user.email,
            showInterests: checkbox.checked,
        });
    }

    return (
    <div className="profile-info">
        <p>Name: {user.name}</p>
        <p>Email: {user.email}</p>
        <p><br/></p>
        <p>
            Interests:
            { user === User.current && 
                <input 
                    type="checkbox" 
                    name="show-interests" 
                    id="show-interests" 
                    value={showInterests}
                    onClick={onShowInterestsClick} /> 
            }
        </p>
        <p>{interestsList}</p>
        <p>Bio</p>
        <div className="profile-bio">{user.bio}</div>
    </div>
    );
}
