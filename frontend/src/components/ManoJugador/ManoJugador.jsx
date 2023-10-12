import React, { useState } from 'react';
import Carta from '../Carta/Carta.jsx';
import style from './ManoJugador.module.css';
import CustomButton from '../Boton/CustomButton';

function ManoJugador({ cartas, esTurno }) {
  const [cartasMano, setCartasMano] = useState(cartas);

  return (
    <div className={style.ManoJugador}>
      {cartas.map((carta, index) => (
        <div
          key={index}
          style={{ position: 'relative' }}
        >
          <Carta carta={carta} esTurno={esTurno} />
        </div>
      ))}
    </div>
  );
}

export default ManoJugador;
