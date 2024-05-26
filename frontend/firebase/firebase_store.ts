// firebase.ts
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";
// import { getAnalytics } from "firebase/analytics";

const firebaseConfig = {
  apiKey: "AIzaSyBzRtfPdtSKXKs42bLHQ3FqB3wJnJDbT3Y",
  authDomain: "futurefund-rait.firebaseapp.com",
  projectId: "futurefund-rait",
  storageBucket: "futurefund-rait.appspot.com",
  messagingSenderId: "534393284645",
  appId: "1:534393284645:web:431a98a6a08cf4679077cc",
  measurementId: "G-5YML0Q5NX6"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
// const analytics = getAnalytics(app);
const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();

export { auth, googleProvider };