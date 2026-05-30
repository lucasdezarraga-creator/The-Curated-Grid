import { useState, useEffect } from 'react'
import { imageMap } from './image_import_helper'
import './carousel.css'

export function Carousel() {
    const [paintingID, setPaintingID] = useState(1);
    const [touchStart, setTouchStart] = useState(null);
    const [touchEnd, setTouchEnd] = useState(null);
    const [paintingsData, setPaintingsData] = useState([]);
    const [showInfo, setShowInfo] = useState(false);

    const totalPaintings = 15;
    const minSwipeDistance = 50;

    useEffect(() => {
        fetch('./data/The_Curated_Grid_painting_data.json')
            .then((response) => response.json())
            .then((data) => setPaintingsData(data))
            .catch((error) => console.error("Error loading gallery metadata:", error));
    }, []);

    useEffect(() => {
        setShowInfo(false);
    }, [paintingID]);

    const onTouchStart = (e) => {
        setTouchEnd(null);
        setTouchStart(e.targetTouches[0].clientX);
    }

    const onTouchMove = (e) => {
        setTouchEnd(e.targetTouches[0].clientX);
    }

    const onTouchEnd = () => {
        if (!touchStart || !touchEnd) return;
        const distance = touchStart - touchEnd;
        if (distance > minSwipeDistance) nextPainting();
        else if (distance < -minSwipeDistance) prevPainting();
    }

    const nextPainting = () => {
        setPaintingID((prevID) => (prevID >= totalPaintings ? 1 : prevID + 1));
    }

    const prevPainting = () => {
        setPaintingID((prevID) => (prevID <= 1 ? totalPaintings : prevID - 1));
    }

    const currentPainting = paintingsData.find(item => item.id === `painting-${paintingID}`);

    return (
        <div className='Carousel_Wrapper'>
            <button className='Nav_Arrow Right_Arrow' onClick={nextPainting}>→</button>

            <div className='PaintingArea' onTouchStart={onTouchStart} onTouchMove={onTouchMove} onTouchEnd={onTouchEnd}>
                <div className='Gallery_Display_Group'>

                    {/* 1. Info box renders first, putting it on the LEFT side on desktop */}
                    {currentPainting && (
                        <div className={`Title_Drawer ${showInfo ? 'expanded' : ''}`}>
                            <div className='Metadata_Header' onClick={() => setShowInfo(!showInfo)}>
                                <div className='Title_Block'>
                                    <h3 className='Title'>{currentPainting.title}</h3>
                                    <span className='Style'>{currentPainting.style}</span>
                                </div>
                                <button className='Info_Toggle_Btn'>
                                    {showInfo ? '✕ Close' : 'ℹ️ Info'}
                                </button>
                            </div>

                            <p className='Prompt'>{currentPainting.prompt}</p>
                        </div>
                    )}

                    {/* 2. The Framed Artwork sits on the right */}
                    <div className='Painting'>
                        <img src={`./images/painting-${paintingID}.png`} alt={`Aesthetic ${paintingID}`} />
                    </div>

                </div>
            </div>

            <button className='Nav_Arrow Left_Arrow' onClick={prevPainting}>←</button>

            <div className="Pagination_Dots">
                {[...Array(totalPaintings)].map((_, i) => {
                    const dotID = i + 1;
                    return (
                        <span
                            key={i}
                            className={`Dot ${paintingID === dotID ? 'Active_Dot' : ''}`}
                            onClick={() => setPaintingID(dotID)}
                        ></span>
                    );
                })}
            </div>
        </div>
    )
}