import { useState } from "react";
import "./Slider.css";
function Slider({ handleValue }) {
    const [valr, setVal] = useState(50);
    const handleLocalValue = (e) => {
        const newValue = e.target.value;
        setVal(newValue);
        if (handleValue) handleValue(newValue);  // only call if prop was provided
    }
    return (
        <>
            <p>Change tone, 100 % profesional, 0 casual talk </p>
            <input className="slider" type="range" min="0" max="100" value={valr} onChange={handleLocalValue} />

        </>
    );
}

export default Slider;