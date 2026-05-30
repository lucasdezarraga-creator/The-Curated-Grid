import { useState } from 'react'
import { imageMap } from './image_import_helper'
import './carousel.css'

export function Carousel(){
    const [paintingID, setPaintingID] = useState(1);
    const [touchStart, setTouchStart] = useState(null);
    const [touchEnd, setTouchEnd] = useState(null);

    const totalPaintings = 15;
    const minSwipeDistance = 50;

    const onTouchStart = (e) => {
        setTouchEnd(null); // Reset end touch
        setTouchStart(e.targetTouches[0].clientX);
    }

    const onTouchMove = (e) => {
        setTouchEnd(e.targetTouches[0].clientX);
    }

    const onTouchEnd = () => {
        if (!touchStart || !touchEnd) return;
        
        const distance = touchStart - touchEnd;
        const isLeftSwipe = distance > minSwipeDistance;
        const isRightSwipe = distance < -minSwipeDistance;

        if (isLeftSwipe) {
            nextPainting(); // Swiping left pulls in the next image
        } else if (isRightSwipe) {
            prevPainting(); // Swiping right pulls in the previous image
        }
    }

    const nextPainting = () => {
        setPaintingID((prevID) => (prevID >= totalPaintings ? 1 : prevID + 1));
    }

    const prevPainting = () => {
        setPaintingID((prevID) => (prevID <= 1 ? totalPaintings : prevID - 1));
    }

    return(
        <div className = 'Carousel_Wrapper'>
            <button className = 'Nav_Arrow Right_Arrow' onClick = {nextPainting}>→</button>

            <div className = 'PaintingArea' onTouchStart = {onTouchStart} onTouchMove = {onTouchMove} onTouchEnd = {onTouchEnd}>
                <div className = 'Painting'>
                    <img src={`/images/painting-${paintingID}.png`} alt={`Aesthetic ${paintingID}`} />
                </div>
            </div>

            <button className = 'Nav_Arrow Left_Arrow' onClick = {prevPainting}>←</button>

            <div className="Pagination_Dots">
                {[...Array(totalPaintings)].map((_, i) => {
                    const dotID = i + 1;
                    return (
                        <span 
                            key={i} 
                            className={`Dot ${paintingID === dotID ? 'Active_Dot' : ''}`}
                            onClick={() => setPaintingID(dotID)} // Bonus: Makes dots clickable!
                        ></span>
                    );
                })}
            </div>
        </div>
    )
}