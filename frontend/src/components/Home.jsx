import React from 'react';
import { useEffect, useState } from 'react';
import axios from 'axios';

import firebase from 'firebase/app';
import 'firebase/firestore';
import 'firebase/auth';

import { useAuthState } from 'react-firebase-hooks/auth';
import { useCollectionsData } from 'react-firebase-hooks/firestore';

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
const firestore = firebase.firestore();

function SignIn() {
    const signInWithGoogle = () => {
        const provider = new firebase.auth.GoogleAuthProvider();
        auth.signInWithPopup(provider);
    }

    return (
        <button onClick={signInWithGoogle}>Sign In</button>
    )
}

function SignOut() {
    return auth.currentUser && (
        <button onClick={() => auth.signOut()}>Sign Out</button>
    )
}

function Home() {
    const [user] = useAuthState(auth);

    const [isLogged, setIsLogged] = useState(false);
    const [userInfo, setUserInfo] = useState([]);

    useEffect(() => {setIsLogged(user != null)})

    const sendUserData = () => {
        var data = JSON.stringify({"userId":"wtf"});
        var config = {
            method: 'post',
            url: 'http://maelstrom.pythonanywhere.com/test',
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

    return(
        <div className="login-screen login-bg-image">
            <div className="login-box">
                {/* <button onClick={() => setIsLogged(!isLogged)}>{isLogged.toString()}</button> */}
                <SignIn/>
                <SignOut/>
            </div>
        </div>
    )
}

export default Home;
