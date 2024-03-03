import React, { useState } from 'react';
import '../CSS/component-1.css'

const MyFirstComponent = () => {
    const [text, setText] = useState('');

    const handleInputChange = (e) => {
        setText(e.target.vslue);
    };
    const handleButtonClick = () => {
        alert('Cliked!');
    };

    return (
        <div id='container-1'>
            <input id='input-1' type='text' value={text} onChange={handleInputChange}/>
            <button id='button-1' onClick={handleButtonClick}>TEST</button>
        </div>
    );
};

export default MyFirstComponent