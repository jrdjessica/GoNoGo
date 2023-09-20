import React from 'react';
import axios from 'axios';

export default function Login() {
    const [signIn, setSignIn] = React.useState({
        email: "",
        password: ""
    })
    const [signUp, setSignUp] = React.useState({
        first_name: "",
        last_name: "",
        email: "",
        password: ""
    })
    function handleSignInInput(e) {
        const { name, value } = e.target;
        setSignIn(prev => ({
            ...prev,
            [name]: value
        }));
    };
    function handleSignUpInput(e) {
        const { name, value } = e.target;
        setSignUp(prev => ({
            ...prev,
            [name]: value
        }));
    }

    async function handleSignUp(e) {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:8000/api/signup/', signUp);
            console.log('Account created:', response);
        } catch (error) {
            console.log('Account creation failed:', error);
        }
    }

    return (
        <>
            <form method="POST">
                <label htmlFor="email">Email:</label>
                <input id="email"
                    name="email"
                    type="email"
                    value={signIn.email}
                    onChange={handleSignInInput}
                    required />
                <label htmlFor="password">Password:</label>
                <input id="password"
                    type="password"
                    name="password"
                    value={signIn.password}
                    onChange={handleSignInInput}
                    minLength={8}
                    placeholder='Mimimum 8 characters'
                    required />
                <button type="submit">Submit</button>
            </form>
            <br></br>

            <form onSubmit={handleSignUp}>
                <label htmlFor="first_name">First Name:</label>
                <input id="first_name"
                    name="first_name"
                    type="text"
                    value={signUp.firstName}
                    onChange={handleSignUpInput}
                    required />
                <label htmlFor="last_name">Last Name:</label>
                <input id="last_name"
                    name="last_name"
                    type="text"
                    value={signUp.lastName}
                    onChange={handleSignUpInput}
                    required />
                <label htmlFor="email">Email:</label>
                <input id="user_email"
                    name="email"
                    type="email"
                    value={signUp.email}
                    onChange={handleSignUpInput}
                    required />
                <label htmlFor="password">Password:</label>
                <input id="user_password"
                    name="password"
                    type="password"
                    minLength={8}
                    value={signUp.password}
                    onChange={handleSignUpInput}
                    placeholder='Mimimum 8 characters'
                    required />
                <button type="submit">Create Account</button>

            </form>

        </>

    )
}
