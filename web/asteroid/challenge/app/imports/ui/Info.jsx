import React, { useState, useEffect, useMemo } from 'react';
import randomColor from 'randomcolor';


export const Info = () => {
  const [what, setWhat] = useState('???');
  const [names, setNames] = useState([]);

  const [selected, setSelected] = useState(null);
  const [data, setData] = useState({});


  useEffect(() => {
    Meteor.call('getPurpose', "learn_more", (err, res) => {
      if (!err) {
        setWhat(res);
      }
    });

    Meteor.call('getAsteroidNames', (err, res) => {
      if (!err) {
        setNames(res);
      }
    });
  }, []);

  useEffect(() => {
    if (!selected) {
      return;
    }

    Meteor.call('getSize', selected, (err, size) => {
      if (!err) {
        Meteor.call('getSpeed', {name: selected}, true, (err, speed) => {
          if (!err) {
            setData({ size, speed });
          }
        });
      }
    });
  }, [selected]);


  const colors = useMemo(() => {
    return names.reduce((acc, obj) => {
      acc[obj.name] = randomColor({luminosity: 'dark'});
      return acc;
    }, {});
  }, [names]);


  return (
    <div>
      <h2>Learn more about our {what}!</h2>
      <div className='urls'>
        {
          selected ? (
            <div>
              <div className='button' onClick={() => {
                setSelected(null);
              }}>
                Back
              </div>

              <div style={{textAlign: "center", color: colors[selected]}}>
                <h2>{selected}</h2>
                <p>Size: {data.size} km</p>
                <p>Speed: {data.speed} m/s</p>
                <p>Description: [TODO]</p>
              </div>
            </div>
          ) : (
            names.map((obj, i) => (
              <div key={`as_${i}`} className='button' style={{color: colors[obj.name]}} onClick={() => {
                setSelected(obj.name);
              }}>{obj.name}</div>
            ))
          )
        }
      </div>
    </div>
  );
};
