import { useState } from 'react'
import { imageMap } from './image_import_helper'
import './carousel.css'

export function Carousel(){
    return(
        <div className = 'Carousel_Wrapper'>
            <button className = 'Nav_Arrow Left_Arrow'>→</button>

            <div className = 'PaintingArea'>
                <div className = 'Painting'> Placeholder </div>
            </div>

            <button className = 'Nav_Arrow Right_Arrow'>←</button>

            <div className="Pagination_Dots">
                <span className="Dot Active_Dot"></span>
                {[...Array(14)].map((_, i) => (<span key = {i} className = 'Dot'></span>))}
            </div>
        </div>
    )
}