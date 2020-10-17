import React from 'react';
import { useEffect, useState } from 'react';
import axios from 'axios';
import gImg from './images/G.png';

import firebase from 'firebase/app';
import 'firebase/firestore';
import 'firebase/auth';

import { useAuthState } from 'react-firebase-hooks/auth';

firebase.initializeApp({
    apiKey: "AIzaSyCbx4JvFiTp1DWCDH2hyEuhnblsSM0rJI4",
    authDomain: "hackgt7-abs.firebaseapp.com",
    databaseURL: "https://hackgt7-abs.firebaseio.com",
    projectId: "hackgt7-abs",
    storageBucket: "hackgt7-abs.appspot.com",
    messagingSenderId: "894677172810",
    appId: "1:894677172810:web:f42768573a8a2bd7ae9cb3",
})

const auth = firebase.auth();

function SignIn() {
    const signInWithGoogle = () => {
        const provider = new firebase.auth.GoogleAuthProvider();
        auth.signInWithPopup(provider);
    }

    return (
        <div>
            <button onClick={signInWithGoogle}>Sign in with <img className="google-icon" src={gImg}></img></button>
        </div>
    )
}

function SignOut() {
    return auth.currentUser && (
        <button className="nav-button" onClick={() => auth.signOut()}>Sign Out</button>
    )
}

function Authentication(props) {
    const [user] = useAuthState(auth);

    const [isLogged, setIsLogged] = useState(false);
    const [dataSent, setDataSent] = useState(false);

    useEffect(() => {
        async function sendUserData(){
            var data = JSON.stringify({
                "userId": user.uid,
                "userEmail" : user.email,
            });
            var config = {
                method: 'post',
                url: 'http://maelstrom.pythonanywhere.com/login',
                headers: { 
                    'Content-Type': 'application/json'
            },
                data : data
            };
            axios(config)
            .then(function (response) {
                console.log(JSON.stringify(response.data));
            })
            .catch(function (error) {
                console.log(error);
            });
        }

        if (user) {
            !isLogged && setIsLogged(true)
            if(isLogged && !dataSent) { 
                sendUserData();
                setDataSent(true);
            };
            props.setIsLogged(true);
        } else {
            isLogged && setIsLogged(false)
            setDataSent(false);
            props.setIsLogged(false);
        }

    }, [user, isLogged, setIsLogged, dataSent, setDataSent, props])

    return(
        !user ? <div className="login-screen login-bg-image">
            <div className="login-box">
                 <SignIn/>
            </div>
        </div> : <SignOut/>
    )
}
export default Authentication;
