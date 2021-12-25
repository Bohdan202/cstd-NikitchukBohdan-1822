import firebase from 'firebase/app';
// require('firebase/database');
require('firebase/auth');

const firebaseConfig = {
    apiKey: "AIzaSyAPYIOlqxXvro99MC2gjEcO_-oF4g5vQKk",
    authDomain: "app72-63cf0.firebaseapp.com",
    databaseURL: "https://app72-63cf0-default-rtdb.europe-west1.firebasedatabase.app",
    projectId: "app72-63cf0",
    storageBucket: "app72-63cf0.appspot.com",
    messagingSenderId: "786370777538",
    appId: "1:786370777538:web:c96774286589f98faa065b"
};

const app = firebase.initializeApp(firebaseConfig);

// export const db = app.database();
// export const namesRef = db.ref('playlist');


// import { getAuth, signInWithPopup, GoogleAuthProvider } from "firebase/auth";

// import { GoogleAuthProvider } from "firebase/auth";
// const provider = new GoogleAuthProvider();

const provider = new firebase.auth.GoogleAuthProvider()
provider.addScope('https://www.googleapis.com/auth/contacts.readonly');

// const provider = new GoogleAuthProvider();
// const auth = getAuth();

// export const googleLogin = (http, cookies, getUserData) => {
//     firebase.auth().signInWithPopup(provider)
//         .then(function (result) {
//             let google_token = result.credential.accessToken;
//             let user = result.user;
             
//             // console.log("google token:", google_token);
//             // console.log("uid:", user.uid);
//             // console.log("refreshToken:", user.refreshToken);
            
//             // console.log("getIdToken:", user.getIdToken());
//             // console.log("getIdTokenResult:", user.getIdTokenResult());

//             // console.log("\nuser_token:", user.toJSON().stsTokenManager.accessToken);

//             console.log("\n\nuser:", user);
//             console.log("\n\nuser_json:", user.toJSON());

//             let uid = user.uid;
//             let refreshToken = user.refreshToken;
//             let token = user.toJSON().stsTokenManager.accessToken;
//             let expiration = user.toJSON().stsTokenManager.expirationTime

//             cookies.set('uid', uid);
//             // cookies.set('refresh', refreshToken);
//             cookies.set('token', token);
//             // cookies.set('expiration', expiration);

//             let isNewUser = result.additionalUserInfo.isNewUser;
//             if (isNewUser) {
//                 user = user.toJSON(); 
//                 let sended_data = {
//                     uid: uid,
//                     name: user.displayName,
//                     email: user.email,
//                     photo: user.photoURL
//                 };
                
//                 http.post('new_user', sended_data, { withCredentials: true })
//                 .catch((err) => {
//                     console.log(err)
//                 })
//             }

//             let sended_data = {
//                 token: token,
//                 googletoken: google_token,
//                 uid: uid
//             };
            
//             http.post('make_session', sended_data, { withCredentials: true })
//             .then(() => {
//                 getUserData()
//             })

//         }).catch(function (error) {
//             // // Handle Errors here.
//             // const errorCode = error.code;
//             // const errorMessage = error.message;
//             // // The email of the user's account used.
//             // const email = error.email;
//             // // The AuthCredential type that was used.
//             // const credential = GoogleAuthProvider.credentialFromError(error);
//             // // ...
//         });
// }

export const googleLogin = () => {
    firebase.auth().signInWithRedirect(provider);
}

export const ifgoogleLogin = (http, cookies, getUserData) => {
    firebase.auth().getRedirectResult()
    .then(function (result) {
        if (result.credential) {
            let google_token = result.credential.accessToken;
            let user = result.user;
                
            console.log("google token:", google_token);

            console.log("\n\nuser:", user);
            console.log("\n\nuser_json:", user.toJSON());

            let uid = user.uid;
            let refreshToken = user.refreshToken;
            let token = user.toJSON().stsTokenManager.accessToken;
            let expiration = user.toJSON().stsTokenManager.expirationTime

            cookies.set('uid', uid);
            // cookies.set('refresh', refreshToken);
            cookies.set('token', token);
            // cookies.set('expiration', expiration);

            let isNewUser = result.additionalUserInfo.isNewUser;
            if (isNewUser) {
                user = user.toJSON(); 
                let sended_data = {
                    uid: uid,
                    name: user.displayName,
                    email: user.email,
                    photo: user.photoURL
                };
                
                http.post('new_user', sended_data, { withCredentials: true })
                .catch((err) => {
                    console.log(err)
                })
            }

            let sended_data = {
                token: token,
                googletoken: google_token,
                uid: uid
            };
            
            http.post('make_session', sended_data, { withCredentials: true })
            .then(() => {
                getUserData()
            })
        }

    }).catch(function (error) {});
}