import React from 'react';

function SignOut(props) {
    return props.auth.currentUser && (
        <button onClick={() => auth.signOut()}>Sign Out</button>
    )
}

export default SignOut;