import React from "react";
import { useState } from 'react';
import styles from "./Carta.module.css";
import Diccionario from './Diccionario.jsx';
import { httpRequest } from '../../services/HttpService';

function Carta({ carta, esTurno , actualizar, mano}) {
    const [isHover, setIsHover] = useState(false);

    function jugarCarta() {
        if(carta.cartaNombre === 'lacosa')
            alert(`No puedes jugar la carta ${carta.cartaNombre}`);
        else
        {
            alert(`Jugue la carta ${carta.id} ${carta.cartaNombre}`);
            descartarCarta();
        }

    }

    async function descartarCarta() 
    {
        if(carta.cartaNombre === 'lacosa')
            alert(`No puedes descartar ni jugar la carta ${carta.cartaNombre}`);
        else
        {
            try 
            {
                if (mano.length > 1) // cambiar a 4
                {
                    const playerID = window.sessionStorage.getItem('user_id');
                    /*
                    await httpRequest({
                        method: 'PUT',
                        service: 'carta/descartar/' + playerID + '/' + carta.id,
                    });
                    */
                    actualizar((manoPrevia) => {
                       return manoPrevia.filter(cartaPrevia => cartaPrevia.id !== carta.id);
                    });

                }
                else
                {
                    alert("No puedes descartar la carta, ya que no tienes suficientes cartas en la mano");
                }
            } 
            catch (error) 
            {
                alert(error);
            }
        }

    }

    const cartaState = esTurno ? `${styles.carta} ${styles.cartaTurno}` : styles.carta;

    //const cartaState = esTurno ? `${styles.carta} ${styles.cartaTurno}` : styles.carta;

    return (
        <div 
            className={cartaState} 
            onMouseEnter={() => setIsHover(true)}
            onMouseLeave={() => setIsHover(false)}>
            <img src={Diccionario[carta.cartaNombre]} width={130}/>
            { isHover && esTurno && (
                <div className={styles.botones}>
                    <button className={styles.boton} onClick={jugarCarta}>Jugar</button>
                    <button className={styles.boton} onClick={descartarCarta}>Descartar</button>
                </div>
            )}
        </div>
    );
}

export default Carta;