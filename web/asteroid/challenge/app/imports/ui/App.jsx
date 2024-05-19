import React from 'react';
import { Info } from './Info.jsx';

export const App = () => (
  <div className="wrapper">
    <h1>Welcome to Asteroid™</h1>

    <img src="images/asteroid.png" alt="Asteroid™" className="asteroid-img" />

    <Info />
  </div>
);
